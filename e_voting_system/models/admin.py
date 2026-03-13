
# handles admin details that the application uses
class Admin:
    def __init__(
        self,
        id,
        username,
        password,
        full_name,
        email,
        role,
        created_at,
        is_active=True
    ):
        self.id = id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.role = role
        self.created_at = created_at
        self.is_active = is_active

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data["id"],
            username=data["username"],
            password=data["password"],
            full_name=data["full_name"],
            email=data["email"],
            role=data["role"],
            created_at=data["created_at"],
            is_active=data.get("is_active", True),
        )