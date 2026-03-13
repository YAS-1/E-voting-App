
# handles position details that the application uses
class Position:
    def __init__(
        self,
        id,
        title,
        description,
        level,
        max_winners,
        min_candidate_age,
        is_active=True,
        created_at=None,
        created_by=None
    ):
        self.id = id
        self.title = title
        self.description = description
        self.level = level
        self.max_winners = max_winners
        self.min_candidate_age = min_candidate_age
        self.is_active = is_active
        self.created_at = created_at
        self.created_by = created_by

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "level": self.level,
            "max_winners": self.max_winners,
            "min_candidate_age": self.min_candidate_age,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "created_by": self.created_by,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            level=data["level"],
            max_winners=data["max_winners"],
            min_candidate_age=data["min_candidate_age"],
            is_active=data.get("is_active", True),
            created_at=data.get("created_at"),
            created_by=data.get("created_by"),
        )