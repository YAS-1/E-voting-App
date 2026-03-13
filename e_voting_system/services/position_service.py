import datetime

from models import Position
from utils.constants import MIN_CANDIDATE_AGE


class PositionService:
    def __init__(self, repository, audit_service):
        self.repository = repository
        self.audit_service = audit_service

    def create_position(
        self,
        title,
        description,
        level,
        max_winners,
        min_candidate_age,
        admin_username
    ):
        if not title:
            return False, "Title cannot be empty.", None

        if level.lower() not in ["national", "regional", "local"]:
            return False, "Invalid level.", None

        try:
            max_winners = int(max_winners)
            if max_winners <= 0:
                return False, "Must be at least 1.", None
        except ValueError:
            return False, "Invalid number.", None

        if str(min_candidate_age).isdigit():
            min_candidate_age = int(min_candidate_age)
        else:
            min_candidate_age = MIN_CANDIDATE_AGE

        position_id = self.repository.next_position_id()

        position = Position(
            id=position_id,
            title=title,
            description=description,
            level=level.capitalize(),
            max_winners=max_winners,
            min_candidate_age=min_candidate_age,
            is_active=True,
            created_at=str(datetime.datetime.now()),
            created_by=admin_username
        )

        self.repository.positions[position_id] = position.to_dict()

        self.audit_service.log(
            "CREATE_POSITION",
            admin_username,
            f"Created position: {title} (ID: {position_id})"
        )

        self.repository.save()
        return True, f"Position '{title}' created! ID: {position_id}", position.to_dict()

    def get_all_positions(self):
        return self.repository.positions

    def get_active_positions(self):
        return {
            pid: position
            for pid, position in self.repository.positions.items()
            if position["is_active"]
        }

    def update_position(
        self,
        position_id,
        admin_username,
        new_title="",
        new_desc="",
        new_level="",
        new_seats=""
    ):
        if not self.repository.positions:
            return False, "No positions found.", None

        if position_id not in self.repository.positions:
            return False, "Position not found.", None

        position = self.repository.positions[position_id]

        if new_title:
            position["title"] = new_title

        if new_desc:
            position["description"] = new_desc

        if new_level and new_level.lower() in ["national", "regional", "local"]:
            position["level"] = new_level.capitalize()

        warning_message = None
        if new_seats:
            try:
                position["max_winners"] = int(new_seats)
            except ValueError:
                warning_message = "Keeping old value."

        self.audit_service.log(
            "UPDATE_POSITION",
            admin_username,
            f"Updated position: {position['title']}"
        )

        self.repository.save()
        return True, "Position updated!", warning_message

    def deactivate_position(self, position_id, admin_username):
        if not self.repository.positions:
            return False, "No positions found."

        if position_id not in self.repository.positions:
            return False, "Position not found."

        for poll in self.repository.polls.values():
            for poll_position in poll.get("positions", []):
                if poll_position["position_id"] == position_id and poll["status"] == "open":
                    return False, f"Cannot delete - in active poll: {poll['title']}"

        self.repository.positions[position_id]["is_active"] = False

        self.audit_service.log(
            "DELETE_POSITION",
            admin_username,
            f"Deactivated position: {self.repository.positions[position_id]['title']}"
        )

        self.repository.save()
        return True, "Position deactivated."