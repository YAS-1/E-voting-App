from ui.console_ui import (
    clear_screen,
    header,
    subheader,
    menu_item,
    prompt,
    masked_input,
    error,
    success,
    warning,
    info,
    pause,
    THEME_LOGIN,
    THEME_ADMIN,
    THEME_VOTER,
    BRIGHT_BLUE,
    BRIGHT_YELLOW,
    RESET,
    DIM,
    BOLD
)


class LoginUI:
    def __init__(self, auth_service, voter_service):
        self.auth_service = auth_service
        self.voter_service = voter_service

    def show_main_menu(self):
        clear_screen()
        header("E-VOTING SYSTEM", THEME_LOGIN)
        print()
        menu_item(1, "Login as Admin", THEME_LOGIN)
        menu_item(2, "Login as Voter", THEME_LOGIN)
        menu_item(3, "Register as Voter", THEME_LOGIN)
        menu_item(4, "Exit", THEME_LOGIN)
        print()
        return prompt("Enter choice: ")

    def handle_admin_login(self):
        clear_screen()
        header("ADMIN LOGIN", THEME_ADMIN)
        print()

        username = prompt("Username: ")
        password = masked_input("Password: ").strip()

        ok, message, admin = self.auth_service.login_admin(username, password)
        print()

        if ok:
            success(message)
            pause()
            return admin

        error(message)
        pause()
        return None

    def handle_voter_login(self):
        clear_screen()
        header("VOTER LOGIN", THEME_VOTER)
        print()

        voter_card = prompt("Voter Card Number: ")
        password = masked_input("Password: ").strip()

        ok, message, voter = self.auth_service.login_voter(voter_card, password)
        print()

        if ok:
            success(message)
            pause()
            return voter

        if "not been verified" in message:
            warning(message)
            info("Please contact an admin to verify your registration.")
        else:
            error(message)

        pause()
        return None

    def handle_voter_registration(self):
        clear_screen()
        header("VOTER REGISTRATION", THEME_VOTER)
        print()

        full_name = prompt("Full Name: ")
        national_id = prompt("National ID Number: ")
        dob_str = prompt("Date of Birth (YYYY-MM-DD): ")
        gender = prompt("Gender (M/F/Other): ").upper()
        address = prompt("Residential Address: ")
        phone = prompt("Phone Number: ")
        email = prompt("Email Address: ")
        password = masked_input("Create Password: ").strip()
        confirm_password = masked_input("Confirm Password: ").strip()

        active_stations = self.voter_service.get_active_stations()
        if not active_stations:
            error("No voting stations available. Contact admin.")
            pause()
            return None

        subheader("Available Voting Stations", THEME_VOTER)
        for sid, station in active_stations.items():
            print(f"    {BRIGHT_BLUE}{sid}.{RESET} {station['name']} {DIM}- {station['location']}{RESET}")

        try:
            station_choice = int(prompt("\nSelect your voting station ID: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return None

        ok, message, voter = self.voter_service.register_voter(
            full_name=full_name,
            national_id=national_id,
            dob_str=dob_str,
            gender=gender,
            address=address,
            phone=phone,
            email=email,
            password=password,
            confirm_password=confirm_password,
            station_choice=station_choice
        )

        print()

        if not ok:
            error(message)
            pause()
            return None

        success(message)
        print(f"  {BOLD}Your Voter Card Number: {BRIGHT_YELLOW}{voter['voter_card_number']}{RESET}")
        warning("IMPORTANT: Save this number! You need it to login.")
        info("Your registration is pending admin verification.")
        pause()
        return voter