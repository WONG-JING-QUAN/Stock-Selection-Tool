import functions as fp


def main():
    """
    Main menu for user registration, login, and stock analysis.
    """
    print("************************")
    print("*                      *")
    print("*      Welcome to      *")
    print("* Stock Selection Tool *")
    print("*        System        *")
    print("************************")

    while True:
        print("\nMenu:")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            email = input("Enter your email: ").strip()
            password = input("Enter your password: ").strip()
            if fp.authenticate_user(email, password):
                logged_in_menu(email)
        elif choice == "2":
            email = input("Enter your email: ").strip()
            password = input("Enter your password: ").strip()
            fp.register_user(email, password)
        elif choice == "3":
            print("Thank you for using the Stock Selection Tool. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


def logged_in_menu(email):
    """
    Menu available after the user logs in successfully.
    """
    while True:
        print("\nLogged-In Menu:")
        print("1. Analyze Stock Data")
        print("2. View Saved Data")
        print("3. Logout")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            ticker = input("Enter stock ticker (e.g., 1155.KL): ").strip()
            start_date = input("Enter start date (YYYY-MM-DD): ").strip()
            end_date = input("Enter end date (YYYY-MM-DD): ").strip()

            if not fp.validate_date_format(start_date) or not fp.validate_date_format(end_date):
                print("Invalid date format. Please use YYYY-MM-DD.")
                continue

            data = fp.get_closing_prices(ticker, start_date, end_date)

            if data is None:
                print("Unable to retrieve stock data. Please try again with a different ticker or date range.")
            else:
                analysis = fp.analyze_closing_prices(data)
                if analysis:
                    print("\nStock Analysis Results:")
                    print(f"Average Price: {analysis['Average Price']}")
                    print(f"Percentage Change (%): {analysis['Percentage Change (%)']}")
                    print(f"Highest Price: {analysis['Highest Price']}")
                    print(f"Lowest Price: {analysis['Lowest Price']}")

                    save = input("Do you want to save this analysis? (y/n): ").strip().lower()
                    if save == "y":
                        fp.save_to_csv(analysis, email, ticker)

        elif choice == "2":
            fp.read_from_csv(email)

        elif choice == "3":
            print("Logging out...")
            break

        else:
            print("Invalid choice. Please select 1, 2, or 3.")


if __name__ == "__main__":
    main()
