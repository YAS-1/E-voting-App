import datetime

from models import Candidate
from utils.constants import (
    MIN_CANDIDATE_AGE,
    MAX_CANDIDATE_AGE,
    REQUIRED_EDUCATION_LEVELS,
)


class CandidateService:
    def __init__(self, repository, audit_service):
        self.repository = repository
        self.audit_service = audit_service

    def create_candidate(
        self,
        full_name,
        national_id,
        dob_str,
        gender,
        education_choice,
        party,
        manifesto,
        address,
        phone,
        email,
        criminal_record,
        years_experience,
        admin_username
    ):
        if not full_name:
            return False, "Name cannot be empty.", None

        if not national_id:
            return False, "National ID cannot be empty.", None

        for candidate in self.repository.candidates.values():
            if candidate["national_id"] == national_id:
                return False, "A candidate with this National ID already exists.", None

        try:
            dob = datetime.datetime.strptime(dob_str, "%Y-%m-%d")
            age = (datetime.datetime.now() - dob).days // 365
        except ValueError:
            return False, "Invalid date format.", None

        if age < MIN_CANDIDATE_AGE:
            return False, f"Candidate must be at least {MIN_CANDIDATE_AGE} years old. Current age: {age}", None

        if age > MAX_CANDIDATE_AGE:
            return False, f"Candidate must not be older than {MAX_CANDIDATE_AGE}. Current age: {age}", None

        try:
            education_choice = int(education_choice)
            if education_choice < 1 or education_choice > len(REQUIRED_EDUCATION_LEVELS):
                return False, "Invalid choice.", None
            education = REQUIRED_EDUCATION_LEVELS[education_choice - 1]
        except ValueError:
            return False, "Invalid input.", None

        criminal_record = criminal_record.lower()
        if criminal_record == "yes":
            self.audit_service.log(
                "CANDIDATE_REJECTED",
                admin_username,
                f"Candidate {full_name} rejected - criminal record"
            )
            return False, "Candidates with criminal records are not eligible.", None

        try:
            years_experience = int(years_experience)
        except ValueError:
            years_experience = 0

        candidate_id = self.repository.next_candidate_id()

        candidate = Candidate(
            id=candidate_id,
            full_name=full_name,
            national_id=national_id,
            date_of_birth=dob_str,
            age=age,
            gender=gender.upper(),
            education=education,
            party=party,
            manifesto=manifesto,
            address=address,
            phone=phone,
            email=email,
            has_criminal_record=False,
            years_experience=years_experience,
            is_active=True,
            is_approved=True,
            created_at=str(datetime.datetime.now()),
            created_by=admin_username
        )

        self.repository.candidates[candidate_id] = candidate.to_dict()

        self.audit_service.log(
            "CREATE_CANDIDATE",
            admin_username,
            f"Created candidate: {full_name} (ID: {candidate_id})"
        )

        self.repository.save()
        return True, f"Candidate '{full_name}' created successfully! ID: {candidate_id}", candidate.to_dict()

    def get_all_candidates(self):
        return self.repository.candidates

    def update_candidate(
        self,
        candidate_id,
        admin_username,
        new_name="",
        new_party="",
        new_manifesto="",
        new_phone="",
        new_email="",
        new_address="",
        new_exp=""
    ):
        if not self.repository.candidates:
            return False, "No candidates found."

        if candidate_id not in self.repository.candidates:
            return False, "Candidate not found."

        candidate = self.repository.candidates[candidate_id]

        if new_name:
            candidate["full_name"] = new_name
        if new_party:
            candidate["party"] = new_party
        if new_manifesto:
            candidate["manifesto"] = new_manifesto
        if new_phone:
            candidate["phone"] = new_phone
        if new_email:
            candidate["email"] = new_email
        if new_address:
            candidate["address"] = new_address

        warning_message = None
        if new_exp:
            try:
                candidate["years_experience"] = int(new_exp)
            except ValueError:
                warning_message = "Invalid number, keeping old value."

        self.audit_service.log(
            "UPDATE_CANDIDATE",
            admin_username,
            f"Updated candidate: {candidate['full_name']} (ID: {candidate_id})"
        )

        self.repository.save()
        return True, f"Candidate '{candidate['full_name']}' updated successfully!", warning_message

    def deactivate_candidate(self, candidate_id, admin_username):
        if not self.repository.candidates:
            return False, "No candidates found."

        if candidate_id not in self.repository.candidates:
            return False, "Candidate not found."

        for poll in self.repository.polls.values():
            if poll["status"] == "open":
                for position in poll.get("positions", []):
                    if candidate_id in position.get("candidate_ids", []):
                        return False, f"Cannot delete - candidate is in active poll: {poll['title']}"

        deleted_name = self.repository.candidates[candidate_id]["full_name"]
        self.repository.candidates[candidate_id]["is_active"] = False

        self.audit_service.log(
            "DELETE_CANDIDATE",
            admin_username,
            f"Deactivated candidate: {deleted_name} (ID: {candidate_id})"
        )

        self.repository.save()
        return True, f"Candidate '{deleted_name}' has been deactivated."

    def search_by_name(self, term):
        term = term.lower()
        return [
            candidate for candidate in self.repository.candidates.values()
            if term in candidate["full_name"].lower()
        ]

    def search_by_party(self, term):
        term = term.lower()
        return [
            candidate for candidate in self.repository.candidates.values()
            if term in candidate["party"].lower()
        ]

    def search_by_education_choice(self, education_choice):
        try:
            education_choice = int(education_choice)
            education = REQUIRED_EDUCATION_LEVELS[education_choice - 1]
        except (ValueError, IndexError):
            return False, "Invalid choice.", []

        results = [
            candidate for candidate in self.repository.candidates.values()
            if candidate["education"] == education
        ]
        return True, education, results

    def search_by_age_range(self, min_age, max_age):
        try:
            min_age = int(min_age)
            max_age = int(max_age)
        except ValueError:
            return False, "Invalid input.", []

        results = [
            candidate for candidate in self.repository.candidates.values()
            if min_age <= candidate["age"] <= max_age
        ]
        return True, "", results

    def get_education_levels(self):
        return REQUIRED_EDUCATION_LEVELS