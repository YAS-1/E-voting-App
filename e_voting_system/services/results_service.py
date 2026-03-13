class ResultsService:
    def __init__(self, repository):
        self.repository = repository

    def get_all_polls(self):
        return self.repository.polls

    def get_poll_results(self, poll_id):
        if not self.repository.polls:
            return False, "No polls found.", None

        if poll_id not in self.repository.polls:
            return False, "Poll not found.", None

        poll = self.repository.polls[poll_id]

        total_eligible = sum(
            1 for voter in self.repository.voters.values()
            if voter["is_verified"]
            and voter["is_active"]
            and voter["station_id"] in poll["station_ids"]
        )

        turnout = (poll["total_votes_cast"] / total_eligible * 100) if total_eligible > 0 else 0

        positions = []
        for pos in poll["positions"]:
            vote_counts = {}
            abstain_count = 0
            total_pos = 0

            for vote in self.repository.votes:
                if vote["poll_id"] == poll_id and vote["position_id"] == pos["position_id"]:
                    total_pos += 1
                    if vote["abstained"]:
                        abstain_count += 1
                    else:
                        vote_counts[vote["candidate_id"]] = vote_counts.get(vote["candidate_id"], 0) + 1

            ranked = []
            for rank, (cid, count) in enumerate(
                sorted(vote_counts.items(), key=lambda x: x[1], reverse=True),
                start=1
            ):
                cand = self.repository.candidates.get(cid, {})
                pct = (count / total_pos * 100) if total_pos > 0 else 0
                ranked.append({
                    "rank": rank,
                    "candidate_id": cid,
                    "candidate_name": cand.get("full_name", "?"),
                    "party": cand.get("party", "?"),
                    "count": count,
                    "percentage": pct,
                    "winner": rank <= pos["max_winners"]
                })

            positions.append({
                "position_title": pos["position_title"],
                "max_winners": pos["max_winners"],
                "ranked": ranked,
                "abstain_count": abstain_count,
                "total_pos": total_pos
            })

        return True, "", {
            "poll": poll,
            "total_eligible": total_eligible,
            "turnout": turnout,
            "positions": positions
        }

    def get_detailed_statistics(self):
        candidates = self.repository.candidates
        voters = self.repository.voters
        stations = self.repository.voting_stations
        polls = self.repository.polls
        votes = self.repository.votes

        stats = {
            "total_candidates": len(candidates),
            "active_candidates": sum(1 for c in candidates.values() if c["is_active"]),
            "total_voters": len(voters),
            "verified_voters": sum(1 for v in voters.values() if v["is_verified"]),
            "active_voters": sum(1 for v in voters.values() if v["is_active"]),
            "total_stations": len(stations),
            "active_stations": sum(1 for s in stations.values() if s["is_active"]),
            "total_polls": len(polls),
            "open_polls": sum(1 for p in polls.values() if p["status"] == "open"),
            "closed_polls": sum(1 for p in polls.values() if p["status"] == "closed"),
            "draft_polls": sum(1 for p in polls.values() if p["status"] == "draft"),
            "total_votes": len(votes),
            "votes_cast_sessions": len(set((v["poll_id"], v["voter_id"]) for v in votes)),
        }

        party_counts = {}
        for c in candidates.values():
            if c["is_active"]:
                party_counts[c["party"]] = party_counts.get(c["party"], 0) + 1

        station_counts = {}
        for sid, station in stations.items():
            if station["is_active"]:
                station_counts[station["name"]] = sum(
                    1 for v in voters.values()
                    if v["station_id"] == sid
                )

        education_counts = {}
        for c in candidates.values():
            if c["is_active"]:
                education_counts[c["education"]] = education_counts.get(c["education"], 0) + 1

        stats["party_counts"] = party_counts
        stats["station_counts"] = station_counts
        stats["education_counts"] = education_counts
        return stats

    def get_station_wise_results(self, poll_id):
        if not self.repository.polls:
            return False, "No polls found.", None

        if poll_id not in self.repository.polls:
            return False, "Poll not found.", None

        poll = self.repository.polls[poll_id]
        station_results = []

        for sid in poll["station_ids"]:
            if sid not in self.repository.voting_stations:
                continue

            station = self.repository.voting_stations[sid]
            station_votes = [
                v for v in self.repository.votes
                if v["poll_id"] == poll_id and v["station_id"] == sid
            ]

            voters_who_voted = len(set(v["voter_id"] for v in station_votes))
            registered_active_verified = sum(
                1 for v in self.repository.voters.values()
                if v["station_id"] == sid and v["is_verified"] and v["is_active"]
            )
            turnout = (
                voters_who_voted / registered_active_verified * 100
                if registered_active_verified > 0 else 0
            )

            positions = []
            for pos in poll["positions"]:
                pv = [v for v in station_votes if v["position_id"] == pos["position_id"]]
                vc = {}
                ac = 0

                for v in pv:
                    if v["abstained"]:
                        ac += 1
                    else:
                        vc[v["candidate_id"]] = vc.get(v["candidate_id"], 0) + 1

                total = sum(vc.values()) + ac
                ranked = []
                for cid, count in sorted(vc.items(), key=lambda x: x[1], reverse=True):
                    cand = self.repository.candidates.get(cid, {})
                    pct = (count / total * 100) if total > 0 else 0
                    ranked.append({
                        "candidate_name": cand.get("full_name", "?"),
                        "party": cand.get("party", "?"),
                        "count": count,
                        "percentage": pct
                    })

                positions.append({
                    "position_title": pos["position_title"],
                    "ranked": ranked,
                    "abstain_count": ac,
                    "total": total
                })

            station_results.append({
                "station_name": station["name"],
                "location": station["location"],
                "registered": registered_active_verified,
                "voted": voters_who_voted,
                "turnout": turnout,
                "positions": positions
            })

        return True, "", {
            "poll": poll,
            "stations": station_results
        }