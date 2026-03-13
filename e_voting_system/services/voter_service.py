import datetime

from models import Voter
from utils.constants import MIN_VOTER_AGE
from utils.security import generate_voter_card_number, hash_password


class VoterService:
    def __init__(self, repository, audit_service):
        self.repository = repository
        self.audit_service = audit_service

    def register_voter(
        self,
        full_name,
        national_id,
        dob_str,
        gender,
        address,
        phone,
        email,
        password,
        confirm_password,
        station_choice
    ):
        if not full_name:
            return False, "Name cannot be empty.", None

        if not national_id:
            return False, "National ID cannot be empty.", None

        for voter in self.repository.voters.values():
            if voter["national_id"] == national_id:
                return False, "A voter with this National ID already exists.", None

        try:
            dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d")
            age = (datetime.datetime.now() - dob).days // 365
            if age < MIN_VOTER_AGE:
                return False, f"You must be at least {MIN_VOTER_AGE} years old to register.", None
        except ValueError:
            return False, "Invalid date format.", None

        gender = gender.upper()
        if gender not in ["M", "F", "OTHER"]:
            return False, "Invalid gender selection.", None

        if len(password) < 6:
            return False, "Password must be at least 6 characters.", None

        if password != confirm_password:
            return False, "Passwords do not match.", None

        if not self.repository.voting_stations:
            return False, "No voting stations available. Contact admin.", None

        if (
            station_choice not in self.repository.voting_stations
            or not self.repository.voting_stations[station_choice]["is_active"]
        ):
            return False, "Invalid station selection.", None

        voter_id = self.repository.next_voter_id()
        voter_card = generate_voter_card_number()

        voter = Voter(
            id=voter_id,
            full_name=full_name,
            national_id=national_id,
            date_of_birth=dob_str,
            age=age,
            gender=gender,
            address=address,
            phone=phone,
            email=email,
            password=hash_password(password),
            voter_card_number=voter_card,
            station_id=station_choice,
            is_verified=False,
            is_active=True,
            has_voted_in=[],
            registered_at=str(datetime.datetime.now()),
            role="voter"
        )

        self.repository.voters[voter_id] = voter.to_dict()

        self.audit_service.log(
            "REGISTER",
            full_name,
            f"New voter registered with card: {voter_card}"
        )

        self.repository.save()

        return True, "Registration successful!", voter.to_dict()

    def get_active_stations(self):
        return {
            sid: station
            for sid, station in self.repository.voting_stations.items()
            if station["is_active"]
        }

    def get_all_voters(self):
        return self.repository.voters

    def get_unverified_voters(self):
        return {
            vid: voter
            for vid, voter in self.repository.voters.items()
            if not voter["is_verified"]
        }

    def verify_voter(self, voter_id, admin_username):
        unverified = self.get_unverified_voters()
        if not unverified:
            return False, "No unverified voters."

        if voter_id not in self.repository.voters:
            return False, "Voter not found."

        if self.repository.voters[voter_id]["is_verified"]:
            return False, "Already verified."

        self.repository.voters[voter_id]["is_verified"] = True

        self.audit_service.log(
            "VERIFY_VOTER",
            admin_username,
            f"Verified voter: {self.repository.voters[voter_id]['full_name']}"
        )

        self.repository.save()
        return True, f"Voter '{self.repository.voters[voter_id]['full_name']}' verified!"

    def verify_all_voters(self, admin_username):
        unverified = self.get_unverified_voters()
        if not unverified:
            return False, "No unverified voters.", 0

        count = 0
        for voter_id in unverified:
            self.repository.voters[voter_id]["is_verified"] = True
            count += 1

        self.audit_service.log(
            "VERIFY_ALL_VOTERS",
            admin_username,
            f"Verified {count} voters"
        )

        self.repository.save()
        return True, f"{count} voters verified!", count

    def deactivate_voter(self, voter_id, admin_username):
        if not self.repository.voters:
            return False, "No voters found."

        if voter_id not in self.repository.voters:
            return False, "Voter not found."

        if not self.repository.voters[voter_id]["is_active"]:
            return False, "Already deactivated."

        self.repository.voters[voter_id]["is_active"] = False

        self.audit_service.log(
            "DEACTIVATE_VOTER",
            admin_username,
            f"Deactivated voter: {self.repository.voters[voter_id]['full_name']}"
        )

        self.repository.save()
        return True, "Voter deactivated."

    def search_by_name(self, term):
        term = term.lower()
        return [
            voter for voter in self.repository.voters.values()
            if term in voter["full_name"].lower()
        ]

    def search_by_card_number(self, card_number):
        return [
            voter for voter in self.repository.voters.values()
            if card_number == voter["voter_card_number"]
        ]

    def search_by_national_id(self, national_id):
        return [
            voter for voter in self.repository.voters.values()
            if national_id == voter["national_id"]
        ]

    def search_by_station(self, station_id):
        return [
            voter for voter in self.repository.voters.values()
            if voter["station_id"] == station_id
        ]

    def get_station_name(self, station_id):
        return self.repository.voting_stations.get(station_id, {}).get("name", "Unknown")

    def build_voter_profile(self, voter):
        return {
            "Name": voter["full_name"],
            "National ID": voter["national_id"],
            "Voter Card": voter["voter_card_number"],
            "Date of Birth": voter["date_of_birth"],
            "Age": voter["age"],
            "Gender": voter["gender"],
            "Address": voter["address"],
            "Phone": voter["phone"],
            "Email": voter["email"],
            "Station": self.get_station_name(voter["station_id"]),
            "Verified": voter["is_verified"],
            "Registered": voter["registered_at"],
            "Polls Voted": len(voter.get("has_voted_in", []))
        }

    def change_password(self, current_user, old_password, new_password, confirm_password):
        if hash_password(old_password) != current_user["password"]:
            return False, "Incorrect current password."

        if len(new_password) < 6:
            return False, "Password must be at least 6 characters."

        if new_password != confirm_password:
            return False, "Passwords do not match."

        new_hashed = hash_password(new_password)
        current_user["password"] = new_hashed

        for vid, voter in self.repository.voters.items():
            if voter["id"] == current_user["id"]:
                voter["password"] = new_hashed
                break

        self.audit_service.log(
            "CHANGE_PASSWORD",
            current_user["voter_card_number"],
            "Password changed"
        )

        self.repository.save()
        return True, "Password changed successfully!"