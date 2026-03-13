import datetime
import hashlib


class VotingService:
    def __init__(self, repository, audit_service):
        self.repository = repository
        self.audit_service = audit_service

    def get_open_polls(self):
        return {
            pid: poll
            for pid, poll in self.repository.polls.items()
            if poll["status"] == "open"
        }

    def get_available_polls_for_voter(self, voter):
        open_polls = self.get_open_polls()

        available_polls = {}
        for pid, poll in open_polls.items():
            if (
                pid not in voter.get("has_voted_in", [])
                and voter["station_id"] in poll["station_ids"]
            ):
                available_polls[pid] = poll

        return available_polls

    def get_poll_candidates(self, poll):
        candidates_by_position = {}

        for pos in poll.get("positions", []):
            candidates_by_position[pos["position_id"]] = [
                self.repository.candidates[cid]
                for cid in pos.get("candidate_ids", [])
                if cid in self.repository.candidates
            ]

        return candidates_by_position

    def cast_vote(self, voter, poll_id, selections):
        available_polls = self.get_available_polls_for_voter(voter)

        if not available_polls:
            return False, "No available polls to vote in.", None

        if poll_id not in available_polls:
            return False, "Invalid poll selection.", None

        poll = available_polls[poll_id]
        my_votes = []

        for pos in poll["positions"]:
            position_id = pos["position_id"]
            selected_candidate_id = selections.get(position_id)

            valid_candidate_ids = pos.get("candidate_ids", [])

            if selected_candidate_id is None:
                my_votes.append({
                    "position_id": position_id,
                    "position_title": pos["position_title"],
                    "candidate_id": None,
                    "candidate_name": None,
                    "abstained": True
                })
                continue

            if selected_candidate_id not in valid_candidate_ids:
                my_votes.append({
                    "position_id": position_id,
                    "position_title": pos["position_title"],
                    "candidate_id": None,
                    "candidate_name": None,
                    "abstained": True
                })
                continue

            candidate = self.repository.candidates.get(selected_candidate_id)
            candidate_name = candidate["full_name"] if candidate else "Unknown"

            my_votes.append({
                "position_id": position_id,
                "position_title": pos["position_title"],
                "candidate_id": selected_candidate_id,
                "candidate_name": candidate_name,
                "abstained": False
            })

        vote_timestamp = str(datetime.datetime.now())
        vote_hash = hashlib.sha256(
            f"{voter['id']}{poll_id}{vote_timestamp}".encode()
        ).hexdigest()[:16]

        for mv in my_votes:
            self.repository.votes.append({
                "vote_id": vote_hash + str(mv["position_id"]),
                "poll_id": poll_id,
                "position_id": mv["position_id"],
                "candidate_id": mv["candidate_id"],
                "voter_id": voter["id"],
                "station_id": voter["station_id"],
                "timestamp": vote_timestamp,
                "abstained": mv["abstained"]
            })

        voter["has_voted_in"].append(poll_id)

        for vid, stored_voter in self.repository.voters.items():
            if stored_voter["id"] == voter["id"]:
                stored_voter["has_voted_in"].append(poll_id)
                break

        self.repository.polls[poll_id]["total_votes_cast"] += 1

        self.audit_service.log(
            "CAST_VOTE",
            voter["voter_card_number"],
            f"Voted in poll: {poll['title']} (Hash: {vote_hash})"
        )

        self.repository.save()

        return True, "Your vote has been recorded successfully!", {
            "vote_reference": vote_hash,
            "poll": poll,
            "votes": my_votes
        }

    def get_voting_history(self, voter):
        voted_polls = voter.get("has_voted_in", [])
        history = []

        for pid in voted_polls:
            if pid not in self.repository.polls:
                continue

            poll = self.repository.polls[pid]
            vote_records = [
                v for v in self.repository.votes
                if v["poll_id"] == pid and v["voter_id"] == voter["id"]
            ]

            formatted_votes = []
            for vr in vote_records:
                pos_title = next(
                    (
                        pos["position_title"]
                        for pos in poll.get("positions", [])
                        if pos["position_id"] == vr["position_id"]
                    ),
                    "Unknown"
                )

                if vr["abstained"]:
                    candidate_name = None
                else:
                    candidate_name = self.repository.candidates.get(
                        vr["candidate_id"], {}
                    ).get("full_name", "Unknown")

                formatted_votes.append({
                    "position_title": pos_title,
                    "abstained": vr["abstained"],
                    "candidate_name": candidate_name
                })

            history.append({
                "poll_id": pid,
                "poll_title": poll["title"],
                "election_type": poll["election_type"],
                "status": poll["status"],
                "votes": formatted_votes
            })

        return history

    def get_closed_poll_results(self):
        closed_polls = {
            pid: poll
            for pid, poll in self.repository.polls.items()
            if poll["status"] == "closed"
        }

        results = []

        for pid, poll in closed_polls.items():
            poll_result = {
                "poll_id": pid,
                "title": poll["title"],
                "election_type": poll["election_type"],
                "total_votes_cast": poll["total_votes_cast"],
                "positions": []
            }

            for pos in poll["positions"]:
                vote_counts = {}
                abstain_count = 0

                for vote in self.repository.votes:
                    if vote["poll_id"] == pid and vote["position_id"] == pos["position_id"]:
                        if vote["abstained"]:
                            abstain_count += 1
                        else:
                            vote_counts[vote["candidate_id"]] = vote_counts.get(vote["candidate_id"], 0) + 1

                total = sum(vote_counts.values()) + abstain_count

                ranked_candidates = []
                for rank, (cid, count) in enumerate(
                    sorted(vote_counts.items(), key=lambda x: x[1], reverse=True),
                    start=1
                ):
                    candidate = self.repository.candidates.get(cid, {})
                    percentage = (count / total * 100) if total > 0 else 0

                    ranked_candidates.append({
                        "rank": rank,
                        "candidate_name": candidate.get("full_name", "Unknown"),
                        "party": candidate.get("party", ""),
                        "count": count,
                        "percentage": percentage
                    })

                poll_result["positions"].append({
                    "position_title": pos["position_title"],
                    "ranked_candidates": ranked_candidates,
                    "abstain_count": abstain_count,
                    "total": total
                })

            results.append(poll_result)

        return results