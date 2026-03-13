import datetime

from models import VotingStation


class StationService:
    def __init__(self, repository, audit_service):
        self.repository = repository
        self.audit_service = audit_service

    def create_station(
        self,
        name,
        location,
        region,
        capacity,
        supervisor,
        contact,
        opening_time,
        closing_time,
        admin_username
    ):
        if not name:
            return False, "Name cannot be empty.", None

        if not location:
            return False, "Location cannot be empty.", None

        try:
            capacity = int(capacity)
            if capacity <= 0:
                return False, "Capacity must be positive.", None
        except ValueError:
            return False, "Invalid capacity.", None

        station_id = self.repository.next_station_id()

        station = VotingStation(
            id=station_id,
            name=name,
            location=location,
            region=region,
            capacity=capacity,
            registered_voters=0,
            supervisor=supervisor,
            contact=contact,
            opening_time=opening_time,
            closing_time=closing_time,
            is_active=True,
            created_at=str(datetime.datetime.now()),
            created_by=admin_username
        )

        self.repository.voting_stations[station_id] = station.to_dict()

        self.audit_service.log(
            "CREATE_STATION",
            admin_username,
            f"Created station: {name} (ID: {station_id})"
        )

        self.repository.save()
        return True, f"Voting Station '{name}' created! ID: {station_id}", station.to_dict()

    def get_all_stations(self):
        return self.repository.voting_stations

    def get_station_registration_count(self, station_id):
        return sum(
            1 for voter in self.repository.voters.values()
            if voter["station_id"] == station_id
        )

    def update_station(
        self,
        station_id,
        admin_username,
        new_name="",
        new_location="",
        new_region="",
        new_capacity="",
        new_supervisor="",
        new_contact=""
    ):
        if not self.repository.voting_stations:
            return False, "No stations found.", None

        if station_id not in self.repository.voting_stations:
            return False, "Station not found.", None

        station = self.repository.voting_stations[station_id]

        if new_name:
            station["name"] = new_name
        if new_location:
            station["location"] = new_location
        if new_region:
            station["region"] = new_region
        if new_supervisor:
            station["supervisor"] = new_supervisor
        if new_contact:
            station["contact"] = new_contact

        warning_message = None
        if new_capacity:
            try:
                station["capacity"] = int(new_capacity)
            except ValueError:
                warning_message = "Invalid number, keeping old value."

        self.audit_service.log(
            "UPDATE_STATION",
            admin_username,
            f"Updated station: {station['name']} (ID: {station_id})"
        )

        self.repository.save()
        return True, f"Station '{station['name']}' updated successfully!", warning_message

    def get_station_voter_count(self, station_id):
        return sum(
            1 for voter in self.repository.voters.values()
            if voter["station_id"] == station_id
        )

    def deactivate_station(self, station_id, admin_username):
        if not self.repository.voting_stations:
            return False, "No stations found."

        if station_id not in self.repository.voting_stations:
            return False, "Station not found."

        station_name = self.repository.voting_stations[station_id]["name"]
        self.repository.voting_stations[station_id]["is_active"] = False

        self.audit_service.log(
            "DELETE_STATION",
            admin_username,
            f"Deactivated station: {station_name}"
        )

        self.repository.save()
        return True, f"Station '{station_name}' deactivated."

    def get_active_stations(self):
        return {
            sid: station
            for sid, station in self.repository.voting_stations.items()
            if station["is_active"]
        }