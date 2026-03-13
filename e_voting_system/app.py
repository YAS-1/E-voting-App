import time

from repositories.data_repository import DataRepository
from services.audit_service import AuditService
from services.auth_service import AuthService
from services.voter_service import VoterService
from services.candidate_service import CandidateService
from services.station_service import StationService
from services.position_service import PositionService
from services.poll_service import PollService
from services.voting_service import VotingService
from services.admin_service import AdminService
from services.results_service import ResultsService
from ui.login_ui import LoginUI
from ui.admin_ui import AdminUI
from ui.voter_ui import VoterUI
from ui.console_ui import info, error, pause, THEME_LOGIN, RESET


class App:
    def __init__(self):
        self.repository = DataRepository()
        self.audit_service = AuditService(self.repository)
        self.auth_service = AuthService(self.repository, self.audit_service)
        self.voter_service = VoterService(self.repository, self.audit_service)
        self.candidate_service = CandidateService(self.repository, self.audit_service)
        self.station_service = StationService(self.repository, self.audit_service)
        self.position_service = PositionService(self.repository, self.audit_service)
        self.poll_service = PollService(self.repository, self.audit_service)
        self.voting_service = VotingService(self.repository, self.audit_service)
        self.admin_service = AdminService(self.repository, self.audit_service)
        self.results_service = ResultsService(self.repository)
        


        self.login_ui = LoginUI(self.auth_service, self.voter_service)
        self.admin_ui = AdminUI(self.voter_service, self.candidate_service, self.station_service, self.position_service, self.poll_service, self.admin_service, self.results_service, self.repository, self.audit_service)
        self.voter_ui = VoterUI(self.voting_service, self.voter_service)


        self.current_user = None
        self.current_role = None

    def reset_session(self):
        self.current_user = None
        self.current_role = None

    def run(self):
        print(f"\n  {THEME_LOGIN}Loading E-Voting System...{RESET}")
        self.repository.load()
        time.sleep(1)

        while True:
            choice = self.login_ui.show_main_menu()

            if choice == "1":
                admin = self.login_ui.handle_admin_login()
                if admin:
                    self.current_user = admin
                    self.current_role = "admin"
                    self.admin_ui.show_dashboard(self.current_user)
                    self.reset_session()

            elif choice == "2":
                voter = self.login_ui.handle_voter_login()
                if voter:
                    self.current_user = voter
                    self.current_role = "voter"
                    self.voter_ui.show_dashboard(self.current_user)
                    self.reset_session()

            elif choice == "3":
                self.login_ui.handle_voter_registration()

            elif choice == "4":
                print()
                info("Goodbye!")
                self.repository.save()
                break

            else:
                print()
                error("Invalid choice.")
                pause()