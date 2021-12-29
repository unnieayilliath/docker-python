#import docker
from consolehelper import ConsoleHelper
from globals import Globals
import datetime

from navigationcontroller import NavigationController

class DockerController:
    # -------------------------------------------------------------------------------------------------
    # A class for controlling interactions with the docker sdk
    def __init__(self):
        # initialise a ec2Resource
        self.client = "docker.from_env()"
        # initialise cloud watch controller
    # -------------------------------------------------------------------------------------------------
    # This protected method returns all instances
    def __list_containers(self):
        repeat = True
        while repeat:
            ConsoleHelper.clear()
            self.__print__header()
            #for container in self.client.containers.list():
            #    print(container.id)
            repeat = self.__perform_action()
    # --------------------------------------------------------------------------------------------------
    # This is the main method for this controller
    def load_screen(self):
        self.__list_containers()
    # -------------------------------------------------------------------------------------------------
    # This method prints container instance
    def __print_continer(self, index,id, name, status, image):
            print(f"{index}. {id}\t{name}\t{status}\t{image}\n")
    # ------------------------------------------------------------------------------------------------------------
    # This method prints header row for containers
    def __print__header(self):
        print("\033[4m\tID\tName\tStatus\tImage\033[0m\n")    
     # ------------------------------------------------------------------------------------------------
    # This method allows user to select an action
    def __perform_action(self):
        repeat = True
        # show all actions for this menu
        selectedAction = NavigationController.print_actions()
        if selectedAction is None:
            repeat=False
        else:
            # add the page to the breadcrumb
            ConsoleHelper.append_breadcrumb(selectedAction["name"])
            # clear previous page
            ConsoleHelper.clear()
        try:
            match selectedAction["key"]:
                case "run":
                    self.__run_container()
                case "stop":
                    self.__stop_container()
                case "remove":
                    self.__remove_container()
        except Exception as ex:
            ConsoleHelper.print_error(ex)
            print("Something went wrong! Please check error details above")
        if repeat:
            input("Press any key to continue..")
            # remove the last added item from breadcrumb
            ConsoleHelper.pop_breadcrumb()
        return repeat
