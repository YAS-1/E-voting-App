import datetime

from models import Poll
from utils.constants import MIN_CANDIDATE_AGE


class PollService:
    def __init__(self, repository, audit_service):
        self.repository = repository
        self.audit_service = audit_service

    def create_poll(
        self,
        title,
        description,
        election_type,
        start_date,
        end_date,
        selected_position_ids,
        use_all_active_stations,
        selected_station_ids,
        admin_username
    ):
        if not title:
            return False, "Title cannot be empty.", None

        try:
            sd = datetime.datetime.strptime(start_date, "%Y-%m-%d")
            ed = datetime.datetime.strptime(end_date, "%Y-%m-%d")
            if ed <= sd:
                return False, "End date must be after start date.", None
        except ValueError:
            return False, "Invalid date format.", None

        if not self.repository.positions:
            return False, "No positions available. Create positions first.", None

        active_positions = {
            pid: p for pid, p in self.repository.positions.items()
            if p["is_active"]
        }
        if not active_positions:
            return False, "No active positions.", None

        poll_positions = []
        for spid in selected_position_ids:
            if spid not in active_positions:
                continue
            poll_positions.append({
                "position_id": spid,
                "position_title": self.repository.positions[spid]["title"],
                "candidate_ids": [],
                "max_winners": self.repository.positions[spid]["max_winners"]
            })

        if not poll_positions:
            return False, "No valid positions selected.", None

        if not self.repository.voting_stations:
            return False, "No voting stations. Create stations first.", None

        active_stations = {
            sid: s for sid, s in self.repository.voting_stations.items()
            if s["is_active"]
        }
        if not active_stations:
            return False, "No active voting stations.", None

        if use_all_active_stations:
            final_station_ids = list(active_stations.keys())
        else:
            final_station_ids = [
                sid for sid in selected_station_ids
                if sid in active_stations
            ]

        poll_id = self.repository.next_poll_id()

        poll = Poll(
            id=poll_id,
            title=title,
            description=description,
            election_type=election_type,
            start_date=start_date,
            end_date=end_date,
            positions=poll_positions,
            station_ids=final_station_ids,
            status="draft",
            total_votes_cast=0,
            created_at=str(datetime.datetime.now()),
            created_by=admin_username
        )

        self.repository.polls[poll_id] = poll.to_dict()

        self.audit_service.log(
            "CREATE_POLL",
            admin_username,
            f"Created poll: {title} (ID: {poll_id})"
        )

        self.repository.save()
        return True, f"Poll '{title}' created! ID: {poll_id}", poll.to_dict()

    def get_all_polls(self):
        return self.repository.polls

    def update_poll(
        self,
        poll_id,
        admin_username,
        new_title="",
        new_desc="",
        new_type="",
        new_start="",
        new_end=""
    ):
        if not self.repository.polls:
            return False, "No polls found.", None

        if poll_id not in self.repository.polls:
            return False, "Poll not found.", None

        poll = self.repository.polls[poll_id]

        if poll["status"] == "open":
            return False, "Cannot update an open poll. Close it first.", None

        if poll["status"] == "closed" and poll["total_votes_cast"] > 0:
            return False, "Cannot update a poll with votes.", None

        warning_message = None

        if new_title:
            poll["title"] = new_title

        if new_desc:
            poll["description"] = new_desc

        if new_type:
            poll["election_type"] = new_type

        if new_start:
            try:
                datetime.datetime.strptime(new_start, "%Y-%m-%d")
                poll["start_date"] = new_start
            except ValueError:
                warning_message = "Invalid date, keeping old value."

        if new_end:
            try:
                datetime.datetime.strptime(new_end, "%Y-%m-%d")
                poll["end_date"] = new_end
            except ValueError:
                warning_message = "Invalid date, keeping old value."

        self.audit_service.log(
            "UPDATE_POLL",
            admin_username,
            f"Updated poll: {poll['title']}"
        )

        self.repository.save()
        return True, "Poll updated!", warning_message

    def delete_poll(self, poll_id, admin_username):
        if not self.repository.polls:
            return False, "No polls found.", None

        if poll_id not in self.repository.polls:
            return False, "Poll not found.", None

        poll = self.repository.polls[poll_id]

        if poll["status"] == "open":
            return False, "Cannot delete an open poll. Close it first.", None

        deleted_title = poll["title"]
        warning_message = None
        if poll["total_votes_cast"] > 0:
            warning_message = f"This poll has {poll['total_votes_cast']} votes recorded."

        del self.repository.polls[poll_id]
        self.repository.votes = [
            vote for vote in self.repository.votes
            if vote["poll_id"] != poll_id
        ]

        self.audit_service.log(
            "DELETE_POLL",
            admin_username,
            f"Deleted poll: {deleted_title}"
        )

        self.repository.save()
        return True, f"Poll '{deleted_title}' deleted.", warning_message

    def toggle_poll_status(self, poll_id, admin_username):
        if not self.repository.polls:
            return False, "No polls found.", None

        if poll_id not in self.repository.polls:
            return False, "Poll not found.", None

        poll = self.repository.polls[poll_id]

        if poll["status"] == "draft":
            if not any(pos["candidate_ids"] for pos in poll["positions"]):
                return False, "Cannot open - no candidates assigned.", None

            poll["status"] = "open"
            self.audit_service.log(
                "OPEN_POLL",
                admin_username,
                f"Opened poll: {poll['title']}"
            )
            self.repository.save()
            return True, f"Poll '{poll['title']}' is now OPEN for voting!", "opened"

        if poll["status"] == "open":
            poll["status"] = "closed"
            self.audit_service.log(
                "CLOSE_POLL",
                admin_username,
                f"Closed poll: {poll['title']}"
            )
            self.repository.save()
            return True, f"Poll '{poll['title']}' is now CLOSED.", "closed"

        if poll["status"] == "closed":
            poll["status"] = "open"
            self.audit_service.log(
                "REOPEN_POLL",
                admin_username,
                f"Reopened poll: {poll['title']}"
            )
            self.repository.save()
            return True, "Poll reopened!", "reopened"

        return False, "Invalid poll status.", None

    def get_eligible_candidates_for_position(self, position_id):
        active_candidates = {
            cid: c for cid, c in self.repository.candidates.items()
            if c["is_active"] and c["is_approved"]
        }

        pos_data = self.repository.positions.get(position_id, {})
        min_age = pos_data.get("min_candidate_age", MIN_CANDIDATE_AGE)

        return {
            cid: c for cid, c in active_candidates.items()
            if c["age"] >= min_age
        }

    def assign_candidates_to_poll(self, poll_id, assignments, admin_username):
        if not self.repository.polls:
            return False, "No polls found."

        if not self.repository.candidates:
            return False, "No candidates found."

        if poll_id not in self.repository.polls:
            return False, "Poll not found."

        poll = self.repository.polls[poll_id]

        if poll["status"] == "open":
            return False, "Cannot modify candidates of an open poll."

        for pos in poll["positions"]:
            position_id = pos["position_id"]
            selected_candidate_ids = assignments.get(position_id, None)

            if selected_candidate_ids is None:
                continue

            eligible = self.get_eligible_candidates_for_position(position_id)
            valid_candidate_ids = [
                cid for cid in selected_candidate_ids
                if cid in eligible
            ]
            pos["candidate_ids"] = valid_candidate_ids

        self.audit_service.log(
            "ASSIGN_CANDIDATES",
            admin_username,
            f"Updated candidate assignments for poll: {poll['title']}"
        )

        self.repository.save()
        return True, f"Candidate assignments updated for poll '{poll['title']}'."

    def get_active_positions(self):
        return {
            pid: p for pid, p in self.repository.positions.items()
            if p["is_active"]
        }

    def get_active_stations(self):
        return {
            sid: s for sid, s in self.repository.voting_stations.items()
            if s["is_active"]
        }