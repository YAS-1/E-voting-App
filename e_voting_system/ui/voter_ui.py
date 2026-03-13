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
    status_badge,
    THEME_VOTER,
    THEME_VOTER_ACCENT,
    RESET,
    DIM,
    BOLD,
    GREEN,
    YELLOW,
    BRIGHT_YELLOW
)


class VoterUI:
    def __init__(self, voting_service, voter_service):
        self.voting_service = voting_service
        self.voter_service = voter_service

    def show_dashboard(self, current_user):
        while True:
            clear_screen()
            header("VOTER DASHBOARD", THEME_VOTER)
            station_name = self.voter_service.get_station_name(current_user["station_id"])
            print(f"  {THEME_VOTER}  ● {RESET}{BOLD}{current_user['full_name']}{RESET}")
            print(f"  {DIM}    Card: {current_user['voter_card_number']}  │  Station: {station_name}{RESET}")
            print()

            menu_item(1, "View Open Polls", THEME_VOTER)
            menu_item(2, "Cast Vote", THEME_VOTER)
            menu_item(3, "View My Voting History", THEME_VOTER)
            menu_item(4, "View Results (Closed Polls)", THEME_VOTER)
            menu_item(5, "View My Profile", THEME_VOTER)
            menu_item(6, "Change Password", THEME_VOTER)
            menu_item(7, "Logout", THEME_VOTER)

            choice = prompt("Enter choice: ")

            if choice == "1":
                self.view_open_polls(current_user)
            elif choice == "2":
                self.cast_vote(current_user)
            elif choice == "3":
                self.view_voting_history(current_user)
            elif choice == "4":
                self.view_closed_poll_results()
            elif choice == "5":
                self.view_my_profile(current_user)
            elif choice == "6":
                self.change_password(current_user)
            elif choice == "7":
                print()
                info("Logging out...")
                pause()
                break
            else:
                error("Invalid choice.")
                pause()

    def view_open_polls(self, current_user):
        clear_screen()
        header("OPEN POLLS", THEME_VOTER)

        open_polls = self.voting_service.get_open_polls()
        if not open_polls:
            print()
            info("No open polls at this time.")
            pause()
            return

        for pid, poll in open_polls.items():
            already_voted = pid in current_user.get("has_voted_in", [])
            voted_label = (
                f" {GREEN}[VOTED]{RESET}"
                if already_voted else
                f" {YELLOW}[NOT YET VOTED]{RESET}"
            )

            print(f"\n  {BOLD}{THEME_VOTER}Poll #{poll['id']}: {poll['title']}{RESET}{voted_label}")
            print(f"  {DIM}Type:{RESET} {poll['election_type']}  {DIM}│  Period:{RESET} {poll['start_date']} to {poll['end_date']}")

            for pos in poll["positions"]:
                print(f"    {THEME_VOTER_ACCENT}▸{RESET} {pos['position_title']}")
                if pos["candidate_ids"]:
                    for cid in pos["candidate_ids"]:
                        if cid in self.voting_service.repository.candidates:
                            candidate = self.voting_service.repository.candidates[cid]
                            print(f"       - {candidate['full_name']} ({candidate['party']})")
                else:
                    print(f"       {DIM}No candidates assigned{RESET}")

        pause()

    def cast_vote(self, current_user):
        clear_screen()
        header("CAST VOTE", THEME_VOTER)

        available_polls = self.voting_service.get_available_polls_for_voter(current_user)
        if not available_polls:
            print()
            info("No available polls to vote in.")
            pause()
            return

        print()
        for pid, poll in available_polls.items():
            print(f"  {THEME_VOTER}{poll['id']}.{RESET} {poll['title']} {DIM}({poll['election_type']}){RESET}")

        try:
            poll_id = int(prompt("\nEnter Poll ID to vote in: "))
        except ValueError:
            error("Invalid input.")
            pause()
            return

        if poll_id not in available_polls:
            error("Invalid poll selection.")
            pause()
            return

        poll = available_polls[poll_id]
        selections = {}

        for pos in poll["positions"]:
            print()
            subheader(f"Position: {pos['position_title']}", THEME_VOTER_ACCENT)

            if not pos["candidate_ids"]:
                warning("No candidates available for this position.")
                selections[pos["position_id"]] = None
                continue

            for cid in pos["candidate_ids"]:
                if cid in self.voting_service.repository.candidates:
                    candidate = self.voting_service.repository.candidates[cid]
                    print(
                        f"  {THEME_VOTER}{candidate['id']}.{RESET} {candidate['full_name']} "
                        f"{DIM}│ {candidate['party']}{RESET}"
                    )

            print(f"  {DIM}Press Enter to abstain for this position.{RESET}")
            raw_choice = prompt("Your choice: ").strip()

            if raw_choice == "":
                selections[pos["position_id"]] = None
                continue

            try:
                selections[pos["position_id"]] = int(raw_choice)
            except ValueError:
                selections[pos["position_id"]] = None

        confirm = prompt("\nSubmit your vote? (yes/no): ").lower()
        if confirm != "yes":
            info("Voting cancelled.")
            pause()
            return

        ok, message, result = self.voting_service.cast_vote(current_user, poll_id, selections)
        print()

        if ok:
            success(message)
            print(f"  {BOLD}Vote Reference:{RESET} {result['vote_reference']}")
        else:
            error(message)

        pause()

    def view_voting_history(self, current_user):
        clear_screen()
        header("MY VOTING HISTORY", THEME_VOTER)

        history = self.voting_service.get_voting_history(current_user)
        if not history:
            print()
            info("You have not voted in any polls yet.")
            pause()
            return

        for item in history:
            print(f"\n  {BOLD}{THEME_VOTER}{item['poll_title']}{RESET}")
            print(f"  {DIM}Type:{RESET} {item['election_type']}  {DIM}│  Status:{RESET} {item['status']}")

            for vote in item["votes"]:
                if vote["abstained"]:
                    choice = f"{YELLOW}ABSTAINED{RESET}"
                else:
                    choice = vote["candidate_name"]
                print(f"    {THEME_VOTER_ACCENT}▸{RESET} {vote['position_title']}: {choice}")

        pause()

    def view_closed_poll_results(self):
        clear_screen()
        header("CLOSED POLL RESULTS", THEME_VOTER)

        results = self.voting_service.get_closed_poll_results()
        if not results:
            print()
            info("No closed polls with results available.")
            pause()
            return

        for poll in results:
            print(f"\n  {BOLD}{THEME_VOTER}{poll['title']}{RESET}")
            print(f"  {DIM}Type:{RESET} {poll['election_type']}  {DIM}│  Total Votes:{RESET} {poll['total_votes_cast']}")

            for pos in poll["positions"]:
                print(f"\n    {THEME_VOTER_ACCENT}▸{RESET} {BOLD}{pos['position_title']}{RESET}")

                if not pos["ranked_candidates"]:
                    print(f"       {DIM}No candidate votes recorded{RESET}")
                else:
                    for candidate in pos["ranked_candidates"]:
                        print(
                            f"       {candidate['rank']}. {candidate['candidate_name']} "
                            f"({candidate['party']}) - {candidate['count']} votes "
                            f"({candidate['percentage']:.1f}%)"
                        )

                print(f"       {DIM}Abstentions:{RESET} {pos['abstain_count']}")

        pause()

    def view_my_profile(self, current_user):
        clear_screen()
        header("MY PROFILE", THEME_VOTER)

        profile = self.voter_service.build_voter_profile(current_user)
        print()

        for label, value in [
            ("Name", profile["Name"]),
            ("National ID", profile["National ID"]),
            ("Voter Card", f"{BRIGHT_YELLOW}{profile['Voter Card']}{RESET}"),
            ("Date of Birth", profile["Date of Birth"]),
            ("Age", profile["Age"]),
            ("Gender", profile["Gender"]),
            ("Address", profile["Address"]),
            ("Phone", profile["Phone"]),
            ("Email", profile["Email"]),
            ("Station", profile["Station"]),
            ("Verified", status_badge("Yes", True) if profile["Verified"] else status_badge("No", False)),
            ("Registered", profile["Registered"]),
            ("Polls Voted", profile["Polls Voted"]),
        ]:
            print(f"  {THEME_VOTER}{label + ':':<16}{RESET} {value}")

        pause()

    def change_password(self, current_user):
        clear_screen()
        header("CHANGE PASSWORD", THEME_VOTER)
        print()

        old_pass = masked_input("Current Password: ").strip()
        new_pass = masked_input("New Password: ").strip()
        confirm_pass = masked_input("Confirm New Password: ").strip()

        ok, message = self.voter_service.change_password(
            current_user=current_user,
            old_password=old_pass,
            new_password=new_pass,
            confirm_password=confirm_pass
        )

        print()
        if ok:
            success(message)
        else:
            error(message)

        pause()