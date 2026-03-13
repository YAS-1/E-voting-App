import datetime

from models import Admin
from utils.security import hash_password


class AdminService:
    ROLE_MAP = {
        "1": "super_admin",
        "2": "election_officer",
        "3": "station_manager",
        "4": "auditor",
    }

    def __init__(self, repository, audit_service):
        self.repository = repository
        self.audit_service = audit_service

    def get_role_map(self):
        return self.ROLE_MAP

    def get_all_admins(self):
        return self.repository.admins

    def create_admin(
        self,
        current_user,
        username,
        full_name,
        email,
        password,
        role_choice
    ):
        if current_user["role"] != "super_admin":
            return False, "Only super admins can create admin accounts.", None

        if not username:
            return False, "Username cannot be empty.", None

        for admin in self.repository.admins.values():
            if admin["username"] == username:
                return False, "Username already exists.", None

        if len(password) < 6:
            return False, "Password must be at least 6 characters.", None

        if role_choice not in self.ROLE_MAP:
            return False, "Invalid role.", None

        role = self.ROLE_MAP[role_choice]
        admin_id = self.repository.next_admin_id()

        admin = Admin(
            id=admin_id,
            username=username,
            password=hash_password(password),
            full_name=full_name,
            email=email,
            role=role,
            created_at=str(datetime.datetime.now()),
            is_active=True
        )

        self.repository.admins[admin_id] = admin.to_dict()

        self.audit_service.log(
            "CREATE_ADMIN",
            current_user["username"],
            f"Created admin: {username} (Role: {role})"
        )

        self.repository.save()
        return True, f"Admin '{username}' created with role: {role}", admin.to_dict()

    def deactivate_admin(self, current_user, admin_id):
        if current_user["role"] != "super_admin":
            return False, "Only super admins can deactivate admins."

        if admin_id not in self.repository.admins:
            return False, "Admin not found."

        if admin_id == current_user["id"]:
            return False, "Cannot deactivate your own account."

        self.repository.admins[admin_id]["is_active"] = False

        self.audit_service.log(
            "DEACTIVATE_ADMIN",
            current_user["username"],
            f"Deactivated admin: {self.repository.admins[admin_id]['username']}"
        )

        self.repository.save()
        return True, "Admin deactivated."