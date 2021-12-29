########################################
#     This is the file 'ConsoleHelper.py'    #
########################################
import os
from globals import Globals


class ConsoleHelper:
    _breadcrumb = []
    # This class is used to create a abstraction layer to handle all UI printing and animations
    # ------------------------------------------------------
    # This method prints warning messages with a predefined style.

    @staticmethod
    def print_warning(message):
        print(f"\033[1;33m {message}\u001b[0m\n")
    # ------------------------------------------------------
    # This method prints error messages with a predefined style.

    @staticmethod
    def print_error(message):
        print(f"\033[1;31m {message}\u001b[0m\n")
    # ------------------------------------------------------
    # This method prints success messages with a predefined style.

    @staticmethod
    def print_success(message):
        print(f"\033[1;32m {message}\u001b[0m\n")
    # ------------------------------------------------------
    # This method clears the console.

    @staticmethod
    def clear():
        command = 'clear'
        if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
            command = 'cls'
        os.system(command)
        ConsoleHelper.show_application_title()
        ConsoleHelper.show_logged_user()
        ConsoleHelper.show_breadcrumb(ConsoleHelper._breadcrumb)

    # ------------------------------------------------------
    # This method shows the application title on the top always.
    @staticmethod
    def show_application_title():
        print(f"\033[1;34m###########################################       Assignment 2       ############################################################\u001b[0m")
        print(f"\033[1;34m###########################################       Docker Interact Tool  ############################################################\u001b[0m")
        print(f"\033[1;34m###########################################                          ############################################################\u001b[0m")

    # ------------------------------------------------------
    # This method shows the page title on the top always.
    @staticmethod
    def show_page_title(pageTitle):
        print(f"\033[1;35m #==== {pageTitle} ====#\u001b[0m\n")
    # ------------------------------------------------------
    # This method shows the page title on the top always.

    @staticmethod
    def show_logged_user():
        # get the logged in user from global class
        loggedInUser = Globals._logged_in_User
        if loggedInUser is not None:
            print(f"\033[1;32m Welcome {loggedInUser._username}({'Admin' if loggedInUser._isAdmin else 'Regular'}),\n\t> Select any menu option by entering the number assigned to the menu item.\n \t> Press '0' on any screen to return to previous screen.\u001b[0m\n")
    # ------------------------------------------------------
    # This method shows the page title on the top always.

    @staticmethod
    def show_breadcrumb(breadcrumb):
        print(f"\033[1;35m {' > '.join(breadcrumb)} \u001b[0m\n")
    # ------------------------------------------------------
    # This method gets a proper integer input from the terminal and loops till it is done

    @staticmethod
    def get_number_input(min, max, message):
        validInput = False
        # --  Loop till valid input is entered
        while not validInput:
            try:
                userInput = int(input(message))
                assert min <= userInput <= max
                # Set invalid input to false since the input is now valid
                validInput = True
            except (ValueError, AssertionError) as ex:
                if min != max:
                    ConsoleHelper.print_error(
                        f"Invalid selection. Please enter a number between {min+1 if min==0 else min} and {max}")
                else:
                    ConsoleHelper.print_error(
                        f"Invalid selection.Please enter {max}")
        return userInput
     # ------------------------------------------------------
    # This method gets a proper integer input from the terminal and loops till it is done

    @staticmethod
    def get_yes_no_input(message):
        validInput = False
        # --  Loop till valid input is entered
        while not validInput:
            try:
                userInput = str(input(message))
                assert userInput.lower() == "y" or userInput.lower() == "n"
                # Set invalid input to false since the input is now valid
                validInput = True
            except (ValueError, AssertionError) as ex:
                # show this error when user enters non integers
                ConsoleHelper.print_error(
                    f"Invalid selection. Please enter  Y or N")
        return userInput.lower() == "y"
    # This method gets a proper integer input from the terminal and loops till it is done

    @staticmethod
    def get_alphanumeric_input(message):
        validInput = False
        # --  Loop till valid input is entered
        while not validInput:
            try:
                userInput = str(input(message))
                assert userInput.lower() != ""
                # Set invalid input to false since the input is now valid
                validInput = True
            except (ValueError, AssertionError) as ex:
                # show this error when user enters non integers
                ConsoleHelper.print_error(
                    f"Invalid selection. Please enter alphabets or numeric")
        return userInput

    @staticmethod
    def wait_for_return():
        ConsoleHelper.get_number_input(0, 0, "Please enter '0' to go back\t")

    @staticmethod
    def append_breadcrumb(newpage):
        ConsoleHelper._breadcrumb.append(newpage)

    @staticmethod
    def reset_breadcrumb():
        ConsoleHelper._breadcrumb = ["Home"]

    @staticmethod
    def pop_breadcrumb():
        ConsoleHelper._breadcrumb.pop()
