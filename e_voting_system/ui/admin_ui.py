from ui.console_ui import (
    clear_screen,
    header,
    subheader,
    table_header,
    table_divider,
    status_badge,
    menu_item,
    prompt,
    masked_input,
    error,
    success,
    warning,
    info,
    pause,
    THEME_ADMIN,
    THEME_ADMIN_ACCENT,
    RESET,
    DIM,
    BOLD,
    GREEN,
    YELLOW,
    RED
)


class AdminUI:
    def __init__(
        self,
        voter_service,
        candidate_service,
        station_service,
        position_service,
        poll_service,
        admin_service,
        repository,
        audit_service,
        results_service
    ):
        self.voter_service = voter_service
        self.candidate_service = candidate_service
        self.station_service = station_service
        self.position_service = position_service
        self.poll_service = poll_service
        self.admin_service = admin_service
        self.repository = repository
        self.audit_service = audit_service
        self.results_service = results_service


    def show_dashboard(self, current_user):
        while True:
            clear_screen()
            header("ADMIN DASHBOARD", THEME_ADMIN)
            print(
                f"  {THEME_ADMIN}  ● {RESET}{BOLD}{current_user['full_name']}{RESET}  "
                f"{DIM}│  Role: {current_user['role']}{RESET}"
            )

            subheader("Candidate Management", THEME_ADMIN_ACCENT)
            menu_item(1, "Create Candidate", THEME_ADMIN)
            menu_item(2, "View All Candidates", THEME_ADMIN)
            menu_item(3, "Update Candidate", THEME_ADMIN)
            menu_item(4, "Delete Candidate", THEME_ADMIN)
            menu_item(5, "Search Candidates", THEME_ADMIN)

            subheader("Voting Station Management", THEME_ADMIN_ACCENT)
            menu_item(6, "Create Voting Station", THEME_ADMIN)
            menu_item(7, "View All Stations", THEME_ADMIN)
            menu_item(8, "Update Station", THEME_ADMIN)
            menu_item(9, "Delete Station", THEME_ADMIN)

            subheader("Polls & Positions", THEME_ADMIN_ACCENT)
            menu_item(10, "Create Position", THEME_ADMIN)
            menu_item(11, "View Positions", THEME_ADMIN)
            menu_item(12, "Update Position", THEME_ADMIN)
            menu_item(13, "Delete Position", THEME_ADMIN)
            menu_item(14, "Create Poll", THEME_ADMIN)
            menu_item(15, "View All Polls", THEME_ADMIN)
            menu_item(16, "Update Poll", THEME_ADMIN)
            menu_item(17, "Delete Poll", THEME_ADMIN)
            menu_item(18, "Open/Close Poll", THEME_ADMIN)
            menu_item(19, "Assign Candidates to Poll", THEME_ADMIN)

            subheader("Voter Management", THEME_ADMIN_ACCENT)
            menu_item(20, "View All Voters", THEME_ADMIN)
            menu_item(21, "Verify Voter", THEME_ADMIN)
            menu_item(22, "Deactivate Voter", THEME_ADMIN)
            menu_item(23, "Search Voters", THEME_ADMIN)

            subheader("Results & Reports", THEME_ADMIN_ACCENT)
            menu_item(27, "View Poll Results", THEME_ADMIN)
            menu_item(28, "View Detailed Statistics", THEME_ADMIN)
            menu_item(29, "View Audit Log", THEME_ADMIN)
            menu_item(30, "Station-wise Results", THEME_ADMIN)

            subheader("System", THEME_ADMIN_ACCENT)
            menu_item(31, "Save Data", THEME_ADMIN)
            menu_item(32, "Logout", THEME_ADMIN)

            choice = prompt("\nEnter choice: ")

            if choice == "1":
                self.create_candidate(current_user["username"])
            elif choice == "2":
                self.view_all_candidates()
            elif choice == "3":
                self.update_candidate(current_user["username"])
            elif choice == "4":
                self.deactivate_candidate(current_user["username"])
            elif choice == "5":
                self.search_candidates()
            elif choice == "6":
                self.create_station(current_user["username"])
            elif choice == "7":
                self.view_all_stations()
            elif choice == "8":
                self.update_station(current_user["username"])
            elif choice == "9":
                self.deactivate_station(current_user["username"])
            elif choice == "10":
                self.create_position(current_user["username"])
            elif choice == "11":
                self.view_positions()
            elif choice == "12":
                self.update_position(current_user["username"])
            elif choice == "13":
                self.deactivate_position(current_user["username"])
            elif choice == "14":
                self.create_poll(current_user["username"])
            elif choice == "15":
                self.view_all_polls()
            elif choice == "16":
                self.update_poll(current_user["username"])
            elif choice == "17":
                self.delete_poll(current_user["username"])
            elif choice == "18":
                self.toggle_poll_status(current_user["username"])
            elif choice == "19":
                self.assign_candidates_to_poll(current_user["username"])
            elif choice == "20":
                self.view_all_voters()
            elif choice == "21":
                self.verify_voter(current_user["username"])
            elif choice == "22":
                self.deactivate_voter(current_user["username"])
            elif choice == "23":
                self.search_voters()
            elif choice == "24":
                self.create_admin_account(current_user)
            elif choice == "25":
                self.view_admins()
            elif choice == "26":
                self.deactivate_admin(current_user)
            elif choice == "27":
                self.view_poll_results()
            elif choice == "28":
                self.view_detailed_statistics()
            elif choice == "29":
                self.view_audit_log()
            elif choice == "30":
                self.view_station_wise_results()
            elif choice == "31":
                self.repository.save()
                print()
                success("Data saved successfully.")
                pause()
            elif choice == "32":
                print()
                info("Logging out...")
                pause()
                break
            elif choice in [str(i) for i in range(1, 32)]:
                print()
                info("That section migration comes next.")
                pause()
            else:
                print()
                error("Invalid choice.")
                pause()

    def create_candidate(self, admin_username):
        clear_screen()
        header("CREATE CANDIDATE", THEME_ADMIN)
        print()

        full_name = prompt("Full Name: ")
        national_id = prompt("National ID Number: ")
        dob_str = prompt("Date of Birth (YYYY-MM-DD): ")
        gender = prompt("Gender (M/F/Other): ").upper()

        subheader("Education Level", THEME_ADMIN_ACCENT)
        education_levels = self.candidate_service.get_education_levels()
        for i, level in enumerate(education_levels, start=1):
            menu_item(i, level, THEME_ADMIN)
        education_choice = prompt("\nSelect education level: ")

        party = prompt("Political Party: ")
        manifesto = prompt("Manifesto Summary: ")
        address = prompt("Residential Address: ")
        phone = prompt("Phone Number: ")
        email = prompt("Email Address: ")
        criminal_record = prompt("Any criminal record? (yes/no): ").lower()
        years_experience = prompt("Years of Leadership Experience: ")

        ok, message, _candidate = self.candidate_service.create_candidate(
            full_name=full_name,
            national_id=national_id,
            dob_str=dob_str,
            gender=gender,
            education_choice=education_choice,
            party=party,
            manifesto=manifesto,
            address=address,
            phone=phone,
            email=email,
            criminal_record=criminal_record,
            years_experience=years_experience,
            admin_username=admin_username
        )

        print()
        if ok:
            success(message)
        else:
            error(message)
        pause()

    def view_all_candidates(self):
        clear_screen()
        header("ALL CANDIDATES", THEME_ADMIN)

        candidates = self.candidate_service.get_all_candidates()
        if not candidates:
            print()
            info("No candidates registered.")
            pause()
            return

        print()
        table_header(
            f"{'ID':<5} {'Name':<25} {'Party':<18} {'Age':<5} {'Approved':<10} {'Active':<8}",
            THEME_ADMIN
        )
        table_divider(78, THEME_ADMIN)

        for candidate in candidates.values():
            approved = status_badge("Yes", True) if candidate["is_approved"] else status_badge("No", False)
            active = status_badge("Yes", True) if candidate["is_active"] else status_badge("No", False)

            print(
                f"  {candidate['id']:<5} "
                f"{candidate['full_name']:<25} "
                f"{candidate['party']:<18} "
                f"{candidate['age']:<5} "
                f"{approved:<19} "
                f"{active}"
            )

        pause()

    def update_candidate(self, admin_username):
        clear_screen()
        header("UPDATE CANDIDATE", THEME_ADMIN)

        candidates = self.candidate_service.get_all_candidates()
        if not candidates:
            print()
            info("No candidates found.")
            pause()
            return

        print()
        try:
            candidate_id = int(prompt("Enter Candidate ID to update: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if candidate_id not in candidates:
            error("Candidate not found.")
            pause()
            return

        candidate = candidates[candidate_id]

        print(f"\n  {DIM}Leave any field blank to keep the current value.{RESET}")
        new_name = prompt(f"Full Name [{candidate['full_name']}]: ")
        new_party = prompt(f"Political Party [{candidate['party']}]: ")
        new_manifesto = prompt(f"Manifesto [{candidate['manifesto']}]: ")
        new_phone = prompt(f"Phone [{candidate['phone']}]: ")
        new_email = prompt(f"Email [{candidate['email']}]: ")
        new_address = prompt(f"Address [{candidate['address']}]: ")
        new_exp = prompt(f"Years Experience [{candidate['years_experience']}]: ")

        ok, message, warning_message = self.candidate_service.update_candidate(
            candidate_id=candidate_id,
            admin_username=admin_username,
            new_name=new_name,
            new_party=new_party,
            new_manifesto=new_manifesto,
            new_phone=new_phone,
            new_email=new_email,
            new_address=new_address,
            new_exp=new_exp
        )

        print()
        if ok:
            success(message)
            if warning_message:
                warning(warning_message)
        else:
            error(message)

        pause()

    def deactivate_candidate(self, admin_username):
        clear_screen()
        header("DELETE CANDIDATE", THEME_ADMIN)

        candidates = self.candidate_service.get_all_candidates()
        if not candidates:
            print()
            info("No candidates found.")
            pause()
            return

        print()
        try:
            candidate_id = int(prompt("Enter Candidate ID to delete: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if candidate_id not in candidates:
            error("Candidate not found.")
            pause()
            return

        confirm = prompt(f"Deactivate '{candidates[candidate_id]['full_name']}'? (yes/no): ").lower()
        if confirm == "yes":
            ok, message = self.candidate_service.deactivate_candidate(candidate_id, admin_username)
            print()

            if ok:
                success(message)
            else:
                error(message)

        pause()

    def search_candidates(self):
        clear_screen()
        header("SEARCH CANDIDATES", THEME_ADMIN)
        subheader("Search by", THEME_ADMIN_ACCENT)

        menu_item(1, "Name", THEME_ADMIN)
        menu_item(2, "Party", THEME_ADMIN)
        menu_item(3, "Education Level", THEME_ADMIN)
        menu_item(4, "Age Range", THEME_ADMIN)

        choice = prompt("\nChoice: ")
        results = []

        if choice == "1":
            term = prompt("Name: ")
            results = self.candidate_service.search_by_name(term)
        elif choice == "2":
            term = prompt("Party: ")
            results = self.candidate_service.search_by_party(term)
        elif choice == "3":
            print()
            for i, level in enumerate(self.candidate_service.get_education_levels(), start=1):
                menu_item(i, level, THEME_ADMIN)
            edu_choice = prompt("\nSelect education level: ")

            ok, message, results = self.candidate_service.search_by_education_choice(edu_choice)
            if not ok:
                print()
                error(message)
                pause()
                return
        elif choice == "4":
            min_age = prompt("Minimum Age: ")
            max_age = prompt("Maximum Age: ")

            ok, message, results = self.candidate_service.search_by_age_range(min_age, max_age)
            if not ok:
                print()
                error(message)
                pause()
                return
        else:
            error("Invalid choice.")
            pause()
            return

        if not results:
            print()
            info("No candidates found.")
        else:
            print(f"\n  {BOLD}Found {len(results)} candidate(s):{RESET}")
            for candidate in results:
                active = status_badge("Active", True) if candidate["is_active"] else status_badge("Inactive", False)
                print(
                    f"  {THEME_ADMIN}ID:{RESET} {candidate['id']}  "
                    f"{DIM}│{RESET}  {candidate['full_name']}  "
                    f"{DIM}│  Party:{RESET} {candidate['party']}  "
                    f"{DIM}│{RESET}  {active}"
                )

        pause()

    def create_station(self, admin_username):
        clear_screen()
        header("CREATE VOTING STATION", THEME_ADMIN)
        print()

        name = prompt("Station Name: ")
        location = prompt("Location/Address: ")
        region = prompt("Region/District: ")
        capacity = prompt("Voter Capacity: ")
        supervisor = prompt("Station Supervisor Name: ")
        contact = prompt("Contact Phone: ")
        opening_time = prompt("Opening Time (e.g. 08:00): ")
        closing_time = prompt("Closing Time (e.g. 17:00): ")

        ok, message, _station = self.station_service.create_station(
            name=name,
            location=location,
            region=region,
            capacity=capacity,
            supervisor=supervisor,
            contact=contact,
            opening_time=opening_time,
            closing_time=closing_time,
            admin_username=admin_username
        )

        print()
        if ok:
            success(message)
        else:
            error(message)
        pause()

    def view_all_stations(self):
        clear_screen()
        header("ALL VOTING STATIONS", THEME_ADMIN)

        stations = self.station_service.get_all_stations()
        if not stations:
            print()
            info("No voting stations found.")
            pause()
            return

        print()
        table_header(
            f"{'ID':<5} {'Name':<25} {'Location':<25} {'Region':<15} {'Cap.':<8} {'Reg.':<8} {'Status':<10}",
            THEME_ADMIN
        )
        table_divider(96, THEME_ADMIN)

        for sid, station in stations.items():
            reg_count = self.station_service.get_station_registration_count(sid)
            status = status_badge("Active", True) if station["is_active"] else status_badge("Inactive", False)
            print(
                f"  {station['id']:<5} "
                f"{station['name']:<25} "
                f"{station['location']:<25} "
                f"{station['region']:<15} "
                f"{station['capacity']:<8} "
                f"{reg_count:<8} "
                f"{status}"
            )

        print(f"\n  {DIM}Total Stations: {len(stations)}{RESET}")
        pause()

    def update_station(self, admin_username):
        clear_screen()
        header("UPDATE VOTING STATION", THEME_ADMIN)

        stations = self.station_service.get_all_stations()
        if not stations:
            print()
            info("No stations found.")
            pause()
            return

        print()
        for sid, station in stations.items():
            print(f"  {THEME_ADMIN}{station['id']}.{RESET} {station['name']} {DIM}- {station['location']}{RESET}")

        try:
            station_id = int(prompt("\nEnter Station ID to update: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if station_id not in stations:
            error("Station not found.")
            pause()
            return

        station = stations[station_id]

        print(f"\n  {BOLD}Updating: {station['name']}{RESET}")
        info("Press Enter to keep current value\n")

        new_name = prompt(f"Name [{station['name']}]: ")
        new_location = prompt(f"Location [{station['location']}]: ")
        new_region = prompt(f"Region [{station['region']}]: ")
        new_capacity = prompt(f"Capacity [{station['capacity']}]: ")
        new_supervisor = prompt(f"Supervisor [{station['supervisor']}]: ")
        new_contact = prompt(f"Contact [{station['contact']}]: ")

        ok, message, warning_message = self.station_service.update_station(
            station_id=station_id,
            admin_username=admin_username,
            new_name=new_name,
            new_location=new_location,
            new_region=new_region,
            new_capacity=new_capacity,
            new_supervisor=new_supervisor,
            new_contact=new_contact
        )

        print()
        if ok:
            success(message)
            if warning_message:
                warning(warning_message)
        else:
            error(message)

        pause()

    def deactivate_station(self, admin_username):
        clear_screen()
        header("DELETE VOTING STATION", THEME_ADMIN)

        stations = self.station_service.get_all_stations()
        if not stations:
            print()
            info("No stations found.")
            pause()
            return

        print()
        for sid, station in stations.items():
            status = status_badge("Active", True) if station["is_active"] else status_badge("Inactive", False)
            print(
                f"  {THEME_ADMIN}{station['id']}.{RESET} "
                f"{station['name']} {DIM}({station['location']}){RESET} {status}"
            )

        try:
            station_id = int(prompt("\nEnter Station ID to delete: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if station_id not in stations:
            error("Station not found.")
            pause()
            return

        voter_count = self.station_service.get_station_voter_count(station_id)
        if voter_count > 0:
            warning(f"{voter_count} voters are registered at this station.")
            if prompt("Proceed with deactivation? (yes/no): ").lower() != "yes":
                info("Cancelled.")
                pause()
                return

        if prompt(f"Confirm deactivation of '{stations[station_id]['name']}'? (yes/no): ").lower() == "yes":
            ok, message = self.station_service.deactivate_station(station_id, admin_username)
            print()

            if ok:
                success(message)
            else:
                error(message)
        else:
            info("Cancelled.")

        pause()

    def create_position(self, admin_username):
        clear_screen()
        header("CREATE POSITION", THEME_ADMIN)
        print()

        title = prompt("Position Title (e.g. President, Governor, Senator): ")
        description = prompt("Description: ")
        level = prompt("Level (National/Regional/Local): ")
        max_winners = prompt("Number of winners/seats: ")
        min_candidate_age = prompt("Minimum candidate age [25]: ")

        ok, message, _position = self.position_service.create_position(
            title=title,
            description=description,
            level=level,
            max_winners=max_winners,
            min_candidate_age=min_candidate_age,
            admin_username=admin_username
        )

        print()
        if ok:
            success(message)
        else:
            error(message)
        pause()

    def view_positions(self):
        clear_screen()
        header("ALL POSITIONS", THEME_ADMIN)

        positions = self.position_service.get_all_positions()
        if not positions:
            print()
            info("No positions found.")
            pause()
            return

        print()
        table_header(
            f"{'ID':<5} {'Title':<25} {'Level':<12} {'Seats':<8} {'Min Age':<10} {'Status':<10}",
            THEME_ADMIN
        )
        table_divider(70, THEME_ADMIN)

        for position in positions.values():
            status = status_badge("Active", True) if position["is_active"] else status_badge("Inactive", False)
            print(
                f"  {position['id']:<5} "
                f"{position['title']:<25} "
                f"{position['level']:<12} "
                f"{position['max_winners']:<8} "
                f"{position['min_candidate_age']:<10} "
                f"{status}"
            )

        print(f"\n  {DIM}Total Positions: {len(positions)}{RESET}")
        pause()

    def update_position(self, admin_username):
        clear_screen()
        header("UPDATE POSITION", THEME_ADMIN)

        positions = self.position_service.get_all_positions()
        if not positions:
            print()
            info("No positions found.")
            pause()
            return

        print()
        for pid, position in positions.items():
            print(f"  {THEME_ADMIN}{position['id']}.{RESET} {position['title']} {DIM}({position['level']}){RESET}")

        try:
            position_id = int(prompt("\nEnter Position ID to update: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if position_id not in positions:
            error("Position not found.")
            pause()
            return

        position = positions[position_id]

        print(f"\n  {BOLD}Updating: {position['title']}{RESET}")
        info("Press Enter to keep current value\n")

        new_title = prompt(f"Title [{position['title']}]: ")
        new_desc = prompt(f"Description [{position['description'][:50]}]: ")
        new_level = prompt(f"Level [{position['level']}]: ")
        new_seats = prompt(f"Seats [{position['max_winners']}]: ")

        ok, message, warning_message = self.position_service.update_position(
            position_id=position_id,
            admin_username=admin_username,
            new_title=new_title,
            new_desc=new_desc,
            new_level=new_level,
            new_seats=new_seats
        )

        print()
        if ok:
            success(message)
            if warning_message:
                warning(warning_message)
        else:
            error(message)

        pause()

    def deactivate_position(self, admin_username):
        clear_screen()
        header("DELETE POSITION", THEME_ADMIN)

        positions = self.position_service.get_all_positions()
        if not positions:
            print()
            info("No positions found.")
            pause()
            return

        print()
        for pid, position in positions.items():
            print(f"  {THEME_ADMIN}{position['id']}.{RESET} {position['title']} {DIM}({position['level']}){RESET}")

        try:
            position_id = int(prompt("\nEnter Position ID to delete: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if position_id not in positions:
            error("Position not found.")
            pause()
            return

        if prompt(f"Confirm deactivation of '{positions[position_id]['title']}'? (yes/no): ").lower() == "yes":
            ok, message = self.position_service.deactivate_position(position_id, admin_username)
            print()

            if ok:
                success(message)
            else:
                error(message)

        pause()

    def create_poll(self, admin_username):
        clear_screen()
        header("CREATE POLL", THEME_ADMIN)

        title = prompt("Poll / Election Title: ")
        description = prompt("Description: ")
        election_type = prompt("Election Type (General/By-election/Primary/Referendum): ")
        start_date = prompt("Start Date (YYYY-MM-DD): ")
        end_date = prompt("End Date (YYYY-MM-DD): ")

        active_positions = self.poll_service.get_active_positions()
        if not active_positions:
            print()
            info("No active positions. Create positions first.")
            pause()
            return

        subheader("Available Positions", THEME_ADMIN_ACCENT)
        for pid, position in active_positions.items():
            print(f"    {THEME_ADMIN}{position['id']}.{RESET} {position['title']} {DIM}({position['level']}){RESET}")

        try:
            selected_position_ids = [
                int(x.strip())
                for x in prompt("\nEnter Position IDs to include (comma-separated): ").split(",")
                if x.strip()
            ]
        except ValueError:
            error("Invalid input.")
            pause()
            return

        active_stations = self.poll_service.get_active_stations()
        if not active_stations:
            print()
            info("No active voting stations. Create stations first.")
            pause()
            return

        subheader("Available Voting Stations", THEME_ADMIN_ACCENT)
        for sid, station in active_stations.items():
            print(f"    {THEME_ADMIN}{station['id']}.{RESET} {station['name']} {DIM}({station['location']}){RESET}")

        use_all = prompt("\nUse all active stations? (yes/no): ").lower() == "yes"
        selected_station_ids = []

        if not use_all:
            try:
                selected_station_ids = [
                    int(x.strip())
                    for x in prompt("Enter Station IDs (comma-separated): ").split(",")
                    if x.strip()
                ]
            except ValueError:
                error("Invalid input.")
                pause()
                return

        ok, message, _poll = self.poll_service.create_poll(
            title=title,
            description=description,
            election_type=election_type,
            start_date=start_date,
            end_date=end_date,
            selected_position_ids=selected_position_ids,
            use_all_active_stations=use_all,
            selected_station_ids=selected_station_ids,
            admin_username=admin_username
        )

        print()
        if ok:
            success(message)
            warning("Status: DRAFT - Assign candidates and then open the poll.")
        else:
            error(message)
        pause()

    def view_all_polls(self):
        clear_screen()
        header("ALL POLLS / ELECTIONS", THEME_ADMIN)

        polls = self.poll_service.get_all_polls()
        if not polls:
            print()
            info("No polls found.")
            pause()
            return

        candidates = self.candidate_service.get_all_candidates()

        for poll in polls.values():
            status_color = GREEN if poll["status"] == "open" else (YELLOW if poll["status"] == "draft" else RED)
            print(f"\n  {BOLD}{THEME_ADMIN}Poll #{poll['id']}: {poll['title']}{RESET}")
            print(f"  {DIM}Type:{RESET} {poll['election_type']}  {DIM}│  Status:{RESET} {status_color}{BOLD}{poll['status'].upper()}{RESET}")
            print(f"  {DIM}Period:{RESET} {poll['start_date']} to {poll['end_date']}  {DIM}│  Votes:{RESET} {poll['total_votes_cast']}")

            for pos in poll["positions"]:
                candidate_names = [
                    candidates[cid]["full_name"]
                    for cid in pos["candidate_ids"]
                    if cid in candidates
                ]
                candidate_display = ", ".join(candidate_names) if candidate_names else f"{DIM}None assigned{RESET}"
                print(f"    {THEME_ADMIN_ACCENT}▸{RESET} {pos['position_title']}: {candidate_display}")

        print(f"\n  {DIM}Total Polls: {len(polls)}{RESET}")
        pause()

    def update_poll(self, admin_username):
        clear_screen()
        header("UPDATE POLL", THEME_ADMIN)

        polls = self.poll_service.get_all_polls()
        if not polls:
            print()
            info("No polls found.")
            pause()
            return

        print()
        for pid, poll in polls.items():
            status_color = GREEN if poll["status"] == "open" else (YELLOW if poll["status"] == "draft" else RED)
            print(f"  {THEME_ADMIN}{poll['id']}.{RESET} {poll['title']} {status_color}({poll['status']}){RESET}")

        try:
            poll_id = int(prompt("\nEnter Poll ID to update: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if poll_id not in polls:
            error("Poll not found.")
            pause()
            return

        poll = polls[poll_id]

        print(f"\n  {BOLD}Updating: {poll['title']}{RESET}")
        info("Press Enter to keep current value\n")

        new_title = prompt(f"Title [{poll['title']}]: ")
        new_desc = prompt(f"Description [{poll['description'][:50]}]: ")
        new_type = prompt(f"Election Type [{poll['election_type']}]: ")
        new_start = prompt(f"Start Date [{poll['start_date']}]: ")
        new_end = prompt(f"End Date [{poll['end_date']}]: ")

        ok, message, warning_message = self.poll_service.update_poll(
            poll_id=poll_id,
            admin_username=admin_username,
            new_title=new_title,
            new_desc=new_desc,
            new_type=new_type,
            new_start=new_start,
            new_end=new_end
        )

        print()
        if ok:
            success(message)
            if warning_message:
                warning(warning_message)
        else:
            error(message)

        pause()

    def delete_poll(self, admin_username):
        clear_screen()
        header("DELETE POLL", THEME_ADMIN)

        polls = self.poll_service.get_all_polls()
        if not polls:
            print()
            info("No polls found.")
            pause()
            return

        print()
        for pid, poll in polls.items():
            print(f"  {THEME_ADMIN}{poll['id']}.{RESET} {poll['title']} {DIM}({poll['status']}){RESET}")

        try:
            poll_id = int(prompt("\nEnter Poll ID to delete: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if poll_id not in polls:
            error("Poll not found.")
            pause()
            return

        if prompt(f"Confirm deletion of '{polls[poll_id]['title']}'? (yes/no): ").lower() == "yes":
            ok, message, warning_message = self.poll_service.delete_poll(poll_id, admin_username)
            print()

            if warning_message:
                warning(warning_message)

            if ok:
                success(message)
            else:
                error(message)

        pause()

    def toggle_poll_status(self, admin_username):
        clear_screen()
        header("OPEN / CLOSE POLL", THEME_ADMIN)

        polls = self.poll_service.get_all_polls()
        if not polls:
            print()
            info("No polls found.")
            pause()
            return

        print()
        for pid, poll in polls.items():
            status_color = GREEN if poll["status"] == "open" else (YELLOW if poll["status"] == "draft" else RED)
            print(f"  {THEME_ADMIN}{poll['id']}.{RESET} {poll['title']}  {status_color}{BOLD}{poll['status'].upper()}{RESET}")

        try:
            poll_id = int(prompt("\nEnter Poll ID: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if poll_id not in polls:
            error("Poll not found.")
            pause()
            return

        poll = polls[poll_id]

        if poll["status"] == "draft":
            confirm = prompt(f"Open poll '{poll['title']}'? Voting will begin. (yes/no): ").lower()
            if confirm != "yes":
                pause()
                return
        elif poll["status"] == "open":
            confirm = prompt(f"Close poll '{poll['title']}'? No more votes accepted. (yes/no): ").lower()
            if confirm != "yes":
                pause()
                return
        elif poll["status"] == "closed":
            info("This poll is already closed.")
            confirm = prompt("Reopen it? (yes/no): ").lower()
            if confirm != "yes":
                pause()
                return

        ok, message, _action = self.poll_service.toggle_poll_status(poll_id, admin_username)
        print()

        if ok:
            success(message)
        else:
            error(message)

        pause()

    def assign_candidates_to_poll(self, admin_username):
        clear_screen()
        header("ASSIGN CANDIDATES TO POLL", THEME_ADMIN)

        polls = self.poll_service.get_all_polls()
        candidates = self.candidate_service.get_all_candidates()

        if not polls:
            print()
            info("No polls found.")
            pause()
            return

        if not candidates:
            print()
            info("No candidates found.")
            pause()
            return

        print()
        for pid, poll in polls.items():
            print(f"  {THEME_ADMIN}{poll['id']}.{RESET} {poll['title']} {DIM}({poll['status']}){RESET}")

        try:
            poll_id = int(prompt("\nEnter Poll ID: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if poll_id not in polls:
            error("Poll not found.")
            pause()
            return

        poll = polls[poll_id]
        assignments = {}

        for pos in poll["positions"]:
            print()
            subheader(f"Position: {pos['position_title']}", THEME_ADMIN_ACCENT)

            eligible = self.poll_service.get_eligible_candidates_for_position(pos["position_id"])
            if not eligible:
                warning("No eligible active/approved candidates for this position.")
                continue

            for cid, candidate in eligible.items():
                print(
                    f"  {THEME_ADMIN}{candidate['id']}.{RESET} {candidate['full_name']} "
                    f"{DIM}│ {candidate['party']} │ Age: {candidate['age']}{RESET}"
                )

            print(f"  {DIM}Max winners/seats: {pos['max_winners']}{RESET}")

            raw = prompt("Enter Candidate IDs to assign (comma-separated, blank = none): ").strip()
            if not raw:
                assignments[pos["position_id"]] = []
                continue

            try:
                selected_ids = [int(x.strip()) for x in raw.split(",") if x.strip()]
            except ValueError:
                warning("Invalid input for this position. Skipping.")
                continue

            assignments[pos["position_id"]] = selected_ids

        ok, message = self.poll_service.assign_candidates_to_poll(
            poll_id=poll_id,
            assignments=assignments,
            admin_username=admin_username
        )

        print()
        if ok:
            success(message)
        else:
            error(message)

        pause()

    def view_all_voters(self):
        clear_screen()
        header("ALL REGISTERED VOTERS", THEME_ADMIN)

        voters = self.voter_service.get_all_voters()
        if not voters:
            print()
            info("No voters registered.")
            pause()
            return

        print()
        table_header(
            f"{'ID':<5} {'Name':<25} {'Card Number':<15} {'Stn':<6} {'Verified':<10} {'Active':<8}",
            THEME_ADMIN
        )
        table_divider(70, THEME_ADMIN)

        for voter in voters.values():
            verified = status_badge("Yes", True) if voter["is_verified"] else status_badge("No", False)
            active = status_badge("Yes", True) if voter["is_active"] else status_badge("No", False)

            print(
                f"  {voter['id']:<5} "
                f"{voter['full_name']:<25} "
                f"{voter['voter_card_number']:<15} "
                f"{voter['station_id']:<6} "
                f"{verified:<19} "
                f"{active}"
            )

        verified_count = sum(1 for voter in voters.values() if voter["is_verified"])
        unverified_count = sum(1 for voter in voters.values() if not voter["is_verified"])

        print(f"\n  {DIM}Total: {len(voters)}  │  Verified: {verified_count}  │  Unverified: {unverified_count}{RESET}")
        pause()

    def verify_voter(self, admin_username):
        clear_screen()
        header("VERIFY VOTER", THEME_ADMIN)

        unverified = self.voter_service.get_unverified_voters()
        if not unverified:
            print()
            info("No unverified voters.")
            pause()
            return

        subheader("Unverified Voters", THEME_ADMIN_ACCENT)
        for voter in unverified.values():
            print(
                f"  {THEME_ADMIN}{voter['id']}.{RESET} {voter['full_name']} "
                f"{DIM}│ NID: {voter['national_id']} │ Card: {voter['voter_card_number']}{RESET}"
            )

        print()
        menu_item(1, "Verify a single voter", THEME_ADMIN)
        menu_item(2, "Verify all pending voters", THEME_ADMIN)

        choice = prompt("\nChoice: ")

        if choice == "1":
            try:
                voter_id = int(prompt("Enter Voter ID: "))
            except ValueError:
                error("Invalid input.")
                pause()
                return

            ok, message = self.voter_service.verify_voter(voter_id, admin_username)
            print()

            if ok:
                success(message)
            else:
                if message in ["No unverified voters.", "Already verified."]:
                    info(message)
                else:
                    error(message)

        elif choice == "2":
            ok, message, _count = self.voter_service.verify_all_voters(admin_username)
            print()

            if ok:
                success(message)
            else:
                info(message)
        else:
            error("Invalid choice.")

        pause()

    def deactivate_voter(self, admin_username):
        clear_screen()
        header("DEACTIVATE VOTER", THEME_ADMIN)

        voters = self.voter_service.get_all_voters()
        if not voters:
            print()
            info("No voters found.")
            pause()
            return

        print()
        try:
            voter_id = int(prompt("Enter Voter ID to deactivate: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if voter_id not in voters:
            error("Voter not found.")
            pause()
            return

        if not voters[voter_id]["is_active"]:
            info("Already deactivated.")
            pause()
            return

        confirm = prompt(f"Deactivate '{voters[voter_id]['full_name']}'? (yes/no): ").lower()
        if confirm == "yes":
            ok, message = self.voter_service.deactivate_voter(voter_id, admin_username)
            print()

            if ok:
                success(message)
            else:
                error(message)

        pause()

    def search_voters(self):
        clear_screen()
        header("SEARCH VOTERS", THEME_ADMIN)
        subheader("Search by", THEME_ADMIN_ACCENT)

        menu_item(1, "Name", THEME_ADMIN)
        menu_item(2, "Voter Card Number", THEME_ADMIN)
        menu_item(3, "National ID", THEME_ADMIN)
        menu_item(4, "Station", THEME_ADMIN)

        choice = prompt("\nChoice: ")
        results = []

        if choice == "1":
            term = prompt("Name: ").lower()
            results = self.voter_service.search_by_name(term)
        elif choice == "2":
            term = prompt("Card Number: ")
            results = self.voter_service.search_by_card_number(term)
        elif choice == "3":
            term = prompt("National ID: ")
            results = self.voter_service.search_by_national_id(term)
        elif choice == "4":
            try:
                station_id = int(prompt("Station ID: "))
            except ValueError:
                error("Invalid input.")
                pause()
                return
            results = self.voter_service.search_by_station(station_id)
        else:
            error("Invalid choice.")
            pause()
            return

        if not results:
            print()
            info("No voters found.")
        else:
            print(f"\n  {BOLD}Found {len(results)} voter(s):{RESET}")
            for voter in results:
                verified = status_badge("Verified", True) if voter["is_verified"] else status_badge("Unverified", False)
                print(
                    f"  {THEME_ADMIN}ID:{RESET} {voter['id']}  "
                    f"{DIM}│{RESET}  {voter['full_name']}  "
                    f"{DIM}│  Card:{RESET} {voter['voter_card_number']}  "
                    f"{DIM}│{RESET}  {verified}"
                )

        pause()

    def create_admin_account(self, current_user):
        clear_screen()
        header("CREATE ADMIN ACCOUNT", THEME_ADMIN)

        if current_user["role"] != "super_admin":
            print()
            error("Only super admins can create admin accounts.")
            pause()
            return

        print()
        username = prompt("Username: ")
        full_name = prompt("Full Name: ")
        email = prompt("Email: ")
        password = masked_input("Password: ").strip()

        subheader("Available Roles", THEME_ADMIN_ACCENT)
        menu_item(1, f"super_admin {DIM}─ Full access{RESET}", THEME_ADMIN)
        menu_item(2, f"election_officer {DIM}─ Manage polls and candidates{RESET}", THEME_ADMIN)
        menu_item(3, f"station_manager {DIM}─ Manage stations and verify voters{RESET}", THEME_ADMIN)
        menu_item(4, f"auditor {DIM}─ Read-only access{RESET}", THEME_ADMIN)

        role_choice = prompt("\nSelect role (1-4): ")

        ok, message, _admin = self.admin_service.create_admin(
            current_user=current_user,
            username=username,
            full_name=full_name,
            email=email,
            password=password,
            role_choice=role_choice
        )

        print()
        if ok:
            success(message)
        else:
            error(message)

        pause()

    def view_admins(self):
        clear_screen()
        header("ALL ADMIN ACCOUNTS", THEME_ADMIN)

        admins = self.admin_service.get_all_admins()
        print()
        table_header(
            f"{'ID':<5} {'Username':<20} {'Full Name':<25} {'Role':<20} {'Active':<8}",
            THEME_ADMIN
        )
        table_divider(78, THEME_ADMIN)

        for admin in admins.values():
            active = status_badge("Yes", True) if admin["is_active"] else status_badge("No", False)
            print(
                f"  {admin['id']:<5} "
                f"{admin['username']:<20} "
                f"{admin['full_name']:<25} "
                f"{admin['role']:<20} "
                f"{active}"
            )

        print(f"\n  {DIM}Total Admins: {len(admins)}{RESET}")
        pause()

    def deactivate_admin(self, current_user):
        clear_screen()
        header("DEACTIVATE ADMIN", THEME_ADMIN)

        if current_user["role"] != "super_admin":
            print()
            error("Only super admins can deactivate admins.")
            pause()
            return

        admins = self.admin_service.get_all_admins()
        print()
        for admin in admins.values():
            active = status_badge("Active", True) if admin["is_active"] else status_badge("Inactive", False)
            print(
                f"  {THEME_ADMIN}{admin['id']}.{RESET} "
                f"{admin['username']} {DIM}({admin['role']}){RESET} {active}"
            )

        try:
            admin_id = int(prompt("\nEnter Admin ID to deactivate: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if prompt(f"Deactivate '{admins.get(admin_id, {}).get('username', 'this admin')}'? (yes/no): ").lower() == "yes":
            ok, message = self.admin_service.deactivate_admin(current_user, admin_id)
            print()

            if ok:
                success(message)
            else:
                error(message)
        pause()

    def view_poll_results(self):
        clear_screen()
        header("POLL RESULTS", THEME_ADMIN)

        polls = self.results_service.get_all_polls()
        if not polls:
            print()
            info("No polls found.")
            pause()
            return

        print()
        for pid, poll in polls.items():
            sc = GREEN if poll["status"] == "open" else (YELLOW if poll["status"] == "draft" else RED)
            print(f"  {THEME_ADMIN}{poll['id']}.{RESET} {poll['title']} {sc}({poll['status']}){RESET}")

        try:
            poll_id = int(prompt("\nEnter Poll ID: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        ok, message, data = self.results_service.get_poll_results(poll_id)
        if not ok:
            error(message)
            pause()
            return

        poll = data["poll"]
        print()
        header(f"RESULTS: {poll['title']}", THEME_ADMIN)
        sc = GREEN if poll["status"] == "open" else RED
        print(f"  {DIM}Status:{RESET} {sc}{BOLD}{poll['status'].upper()}{RESET}  {DIM}│  Votes:{RESET} {BOLD}{poll['total_votes_cast']}{RESET}")

        turnout = data["turnout"]
        tc = GREEN if turnout > 50 else (YELLOW if turnout > 25 else RED)
        print(f"  {DIM}Eligible:{RESET} {data['total_eligible']}  {DIM}│  Turnout:{RESET} {tc}{BOLD}{turnout:.1f}%{RESET}")

        for pos in data["positions"]:
            subheader(f"{pos['position_title']} (Seats: {pos['max_winners']})", THEME_ADMIN_ACCENT)

            if not pos["ranked"]:
                info("    No votes recorded for this position.")
            else:
                for item in pos["ranked"]:
                    bl = int(item["percentage"] / 2)
                    bar = f"{THEME_ADMIN}{'█' * bl}{DIM}{'░' * (50 - bl)}{RESET}"
                    winner = f" {GREEN}{BOLD}★ WINNER{RESET}" if item["winner"] else ""
                    print(f"    {BOLD}{item['rank']}. {item['candidate_name']}{RESET} {DIM}({item['party']}){RESET}")
                    print(f"       {bar} {BOLD}{item['count']}{RESET} ({item['percentage']:.1f}%){winner}")

            if pos["abstain_count"] > 0:
                pct = (pos["abstain_count"] / pos["total_pos"] * 100) if pos["total_pos"] > 0 else 0
                print(f"    {DIM}Abstained: {pos['abstain_count']} ({pct:.1f}%){RESET}")

        pause()

    def view_detailed_statistics(self):
        clear_screen()
        header("DETAILED STATISTICS", THEME_ADMIN)

        stats = self.results_service.get_detailed_statistics()

        subheader("SYSTEM OVERVIEW", THEME_ADMIN_ACCENT)
        print(f"  {DIM}Candidates:{RESET} {stats['total_candidates']}  {DIM}│  Active:{RESET} {stats['active_candidates']}")
        print(f"  {DIM}Voters:{RESET} {stats['total_voters']}  {DIM}│  Verified:{RESET} {stats['verified_voters']}  {DIM}│  Active:{RESET} {stats['active_voters']}")
        print(f"  {DIM}Stations:{RESET} {stats['total_stations']}  {DIM}│  Active:{RESET} {stats['active_stations']}")
        print(f"  {DIM}Polls:{RESET} {stats['total_polls']}  {DIM}│  Open:{RESET} {stats['open_polls']}  {DIM}│  Closed:{RESET} {stats['closed_polls']}  {DIM}│  Draft:{RESET} {stats['draft_polls']}")
        print(f"  {DIM}Vote Records:{RESET} {stats['total_votes']}  {DIM}│  Voting Sessions:{RESET} {stats['votes_cast_sessions']}")

        subheader("CANDIDATES PER PARTY", THEME_ADMIN_ACCENT)
        if not stats["party_counts"]:
            info("No party data.")
        else:
            for party, count in stats["party_counts"].items():
                print(f"    {party}: {BOLD}{count}{RESET}")

        subheader("VOTERS PER STATION", THEME_ADMIN_ACCENT)
        if not stats["station_counts"]:
            info("No station data.")
        else:
            for station, count in stats["station_counts"].items():
                print(f"    {station}: {BOLD}{count}{RESET}")

        subheader("EDUCATION LEVEL DISTRIBUTION", THEME_ADMIN_ACCENT)
        if not stats["education_counts"]:
            info("No education data.")
        else:
            for edu, count in stats["education_counts"].items():
                print(f"    {edu}: {BOLD}{count}{RESET}")

        pause()

    def view_audit_log(self):
        clear_screen()
        header("AUDIT LOG", THEME_ADMIN)

        entries = self.audit_service.get_all_entries()
        if not entries:
            print()
            info("No audit records.")
            pause()
            return

        print(f"\n  {DIM}Total Records: {len(entries)}{RESET}")
        subheader("Filter", THEME_ADMIN_ACCENT)
        menu_item(1, "Last 20 entries", THEME_ADMIN)
        menu_item(2, "All entries", THEME_ADMIN)
        menu_item(3, "Filter by action type", THEME_ADMIN)
        menu_item(4, "Filter by user", THEME_ADMIN)

        choice = prompt("\nChoice: ")
        filtered = entries

        if choice == "1":
            filtered = self.audit_service.get_last_entries(20)
        elif choice == "3":
            action_types = self.audit_service.get_action_types()
            for i, at in enumerate(action_types, 1):
                print(f"    {THEME_ADMIN}{i}.{RESET} {at}")
            try:
                at_choice = int(prompt("Select action type: "))
                filtered = self.audit_service.filter_by_action(action_types[at_choice - 1])
            except (ValueError, IndexError):
                error("Invalid choice.")
                pause()
                return
        elif choice == "4":
            uf = prompt("Enter username/card number: ")
            filtered = self.audit_service.filter_by_user(uf)

        print()
        table_header(f"{'Timestamp':<22} {'Action':<25} {'User':<20} {'Details'}", THEME_ADMIN)
        table_divider(100, THEME_ADMIN)

        for entry in filtered:
            ac = GREEN if "CREATE" in entry["action"] or entry["action"] == "LOGIN" else (
                RED if "DELETE" in entry["action"] or "DEACTIVATE" in entry["action"] else (
                    YELLOW if "UPDATE" in entry["action"] else RESET
                )
            )
            print(
                f"  {DIM}{entry['timestamp'][:19]}{RESET}  "
                f"{ac}{entry['action']:<25}{RESET} "
                f"{entry['user']:<20} "
                f"{DIM}{entry['details'][:50]}{RESET}"
            )

        pause()

    def view_station_wise_results(self):
        clear_screen()
        header("STATION-WISE RESULTS", THEME_ADMIN)

        polls = self.results_service.get_all_polls()
        if not polls:
            print()
            info("No polls found.")
            pause()
            return

        print()
        for pid, poll in polls.items():
            sc = GREEN if poll["status"] == "open" else (YELLOW if poll["status"] == "draft" else RED)
            print(f"  {THEME_ADMIN}{poll['id']}.{RESET} {poll['title']} {sc}({poll['status']}){RESET}")

        try:
            poll_id = int(prompt("\nEnter Poll ID: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        ok, message, data = self.results_service.get_station_wise_results(poll_id)
        if not ok:
            error(message)
            pause()
            return

        poll = data["poll"]
        print()
        header(f"STATION RESULTS: {poll['title']}", THEME_ADMIN)

        for station in data["stations"]:
            subheader(f"{station['station_name']} ({station['location']})", THEME_ADMIN_ACCENT)
            tc = GREEN if station["turnout"] > 50 else (YELLOW if station["turnout"] > 25 else RED)
            print(
                f"  {DIM}Registered:{RESET} {station['registered']}  "
                f"{DIM}│  Voted:{RESET} {station['voted']}  "
                f"{DIM}│  Turnout:{RESET} {tc}{BOLD}{station['turnout']:.1f}%{RESET}"
            )

            for pos in station["positions"]:
                print(f"    {THEME_ADMIN_ACCENT}▸{RESET} {pos['position_title']}:")
                for item in pos["ranked"]:
                    print(
                        f"      {item['candidate_name']} {DIM}({item['party']}){RESET}: "
                        f"{BOLD}{item['count']}{RESET} ({item['percentage']:.1f}%)"
                    )
                if pos["abstain_count"] > 0:
                    pct = (pos["abstain_count"] / pos["total"] * 100) if pos["total"] > 0 else 0
                    print(f"      {DIM}Abstained: {pos['abstain_count']} ({pct:.1f}%){RESET}")

        pause()