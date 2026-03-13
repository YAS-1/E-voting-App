
# handles audit entry details
class AuditEntry:
    def __init__(self, timestamp, action, user, details):
        self.timestamp = timestamp
        self.action = action
        self.user = user
        self.details = details

    def to_dict(self):
        return {
            "timestamp": self.timestamp,
            "action": self.action,
            "user": self.user,
            "details": self.details,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            timestamp=data["timestamp"],
            action=data["action"],
            user=data["user"],
            details=data["details"],
        )