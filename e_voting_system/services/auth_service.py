from utils.security import hash_password


class AuthService:
    def __init__(self, repository, audit_service):
        self.repository = repository
        self.audit_service = audit_service

    def login_admin(self, username, password):
        hashed_password = hash_password(password)

        for admin in self.repository.admins.values():
            if admin["username"] == username and admin["password"] == hashed_password:
                if not admin["is_active"]:
                    self.audit_service.log("LOGIN_FAILED", username, "Account deactivated")
                    return False, "This account has been deactivated.", None

                self.audit_service.log("LOGIN", username, "Admin login successful")
                return True, f"Welcome, {admin['full_name']}!", admin

        self.audit_service.log("LOGIN_FAILED", username, "Invalid admin credentials")
        return False, "Invalid credentials.", None

    def login_voter(self, voter_card_number, password):
        hashed_password = hash_password(password)

        for voter in self.repository.voters.values():
            if (
                voter["voter_card_number"] == voter_card_number
                and voter["password"] == hashed_password
            ):
                if not voter["is_active"]:
                    self.audit_service.log(
                        "LOGIN_FAILED",
                        voter_card_number,
                        "Voter account deactivated"
                    )
                    return False, "This voter account has been deactivated.", None

                if not voter["is_verified"]:
                    self.audit_service.log(
                        "LOGIN_FAILED",
                        voter_card_number,
                        "Voter not verified"
                    )
                    return False, "Your voter registration has not been verified yet.", None

                self.audit_service.log("LOGIN", voter_card_number, "Voter login successful")
                return True, f"Welcome, {voter['full_name']}!", voter

        self.audit_service.log(
            "LOGIN_FAILED",
            voter_card_number,
            "Invalid voter credentials"
        )
        return False, "Invalid voter card number or password.", None