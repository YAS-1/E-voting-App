
# handles poll details that the application uses
class Poll:
    def __init__(
        self,
        id,
        title,
        description,
        election_type,
        start_date,
        end_date,
        positions=None,
        station_ids=None,
        status="draft",
        total_votes_cast=0,
        created_at=None,
        created_by=None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.election_type = election_type
        self.start_date = start_date
        self.end_date = end_date
        self.positions = positions or []
        self.station_ids = station_ids or []
        self.status = status
        self.total_votes_cast = total_votes_cast
        self.created_at = created_at
        self.created_by = created_by

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "election_type": self.election_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "positions": self.positions,
            "station_ids": self.station_ids,
            "status": self.status,
            "total_votes_cast": self.total_votes_cast,
            "created_at": self.created_at,
            "created_by": self.created_by,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            election_type=data["election_type"],
            start_date=data["start_date"],
            end_date=data["end_date"],
            positions=data.get("positions", []),
            station_ids=data.get("station_ids", []),
            status=data.get("status", "draft"),
            total_votes_cast=data.get("total_votes_cast", 0),
            created_at=data.get("created_at"),
            created_by=data.get("created_by"),
        )