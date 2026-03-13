import json
import os
import datetime

from utils.constants import DATA_FILE_PATH
from utils.security import hash_password


class DataRepository:
    def __init__(self):
        self.candidates = {}
        self.candidate_id_counter = 1

        self.voting_stations = {}
        self.station_id_counter = 1

        self.polls = {}
        self.poll_id_counter = 1

        self.positions = {}
        self.position_id_counter = 1

        self.voters = {}
        self.voter_id_counter = 1

        self.admins = {}
        self.admin_id_counter = 1

        self.votes = []
        self.audit_log = []

        self._seed_default_admin()

    def _seed_default_admin(self):
        if not self.admins:
            self.admins[1] = {
                "id": 1,
                "username": "admin",
                "password": hash_password("admin123"),
                "full_name": "System Administrator",
                "email": "admin@evote.com",
                "role": "super_admin",
                "created_at": str(datetime.datetime.now()),
                "is_active": True
            }
            self.admin_id_counter = 2

    def save(self):
        data = {
            "candidates": self.candidates,
            "candidate_id_counter": self.candidate_id_counter,
            "voting_stations": self.voting_stations,
            "station_id_counter": self.station_id_counter,
            "polls": self.polls,
            "poll_id_counter": self.poll_id_counter,
            "positions": self.positions,
            "position_id_counter": self.position_id_counter,
            "voters": self.voters,
            "voter_id_counter": self.voter_id_counter,
            "admins": self.admins,
            "admin_id_counter": self.admin_id_counter,
            "votes": self.votes,
            "audit_log": self.audit_log
        }

        os.makedirs(os.path.dirname(DATA_FILE_PATH), exist_ok=True)
        with open(DATA_FILE_PATH, "w") as file:
            json.dump(data, file, indent=2)

    def load(self):
        if not os.path.exists(DATA_FILE_PATH):
            return

        with open(DATA_FILE_PATH, "r") as file:
            data = json.load(file)

        self.candidates = {int(k): v for k, v in data.get("candidates", {}).items()}
        self.candidate_id_counter = data.get("candidate_id_counter", 1)

        self.voting_stations = {int(k): v for k, v in data.get("voting_stations", {}).items()}
        self.station_id_counter = data.get("station_id_counter", 1)

        self.polls = {int(k): v for k, v in data.get("polls", {}).items()}
        self.poll_id_counter = data.get("poll_id_counter", 1)

        self.positions = {int(k): v for k, v in data.get("positions", {}).items()}
        self.position_id_counter = data.get("position_id_counter", 1)

        self.voters = {int(k): v for k, v in data.get("voters", {}).items()}
        self.voter_id_counter = data.get("voter_id_counter", 1)

        self.admins = {int(k): v for k, v in data.get("admins", {}).items()}
        self.admin_id_counter = data.get("admin_id_counter", 1)

        self.votes = data.get("votes", [])
        self.audit_log = data.get("audit_log", [])

        if not self.admins:
            self._seed_default_admin()

    def next_candidate_id(self):
        current = self.candidate_id_counter
        self.candidate_id_counter += 1
        return current

    def next_station_id(self):
        current = self.station_id_counter
        self.station_id_counter += 1
        return current

    def next_poll_id(self):
        current = self.poll_id_counter
        self.poll_id_counter += 1
        return current

    def next_position_id(self):
        current = self.position_id_counter
        self.position_id_counter += 1
        return current

    def next_voter_id(self):
        current = self.voter_id_counter
        self.voter_id_counter += 1
        return current

    def next_admin_id(self):
        current = self.admin_id_counter
        self.admin_id_counter += 1
        return current