import datetime

from models import AuditEntry


class AuditService:
    def __init__(self, repository):
        self.repository = repository

    def log(self, action, user, details):
        entry = AuditEntry(
            timestamp=str(datetime.datetime.now()),
            action=action,
            user=user,
            details=details
        )
        self.repository.audit_log.append(entry.to_dict())

    def get_all_entries(self):
        return self.repository.audit_log

    def get_last_entries(self, limit=20):
        return self.repository.audit_log[-limit:]

    def get_action_types(self):
        return sorted(list(set(entry["action"] for entry in self.repository.audit_log)))

    def filter_by_action(self, action):
        return [
            entry for entry in self.repository.audit_log
            if entry["action"] == action
        ]

    def filter_by_user(self, user_fragment):
        return [
            entry for entry in self.repository.audit_log
            if user_fragment.lower() in entry["user"].lower()
        ]