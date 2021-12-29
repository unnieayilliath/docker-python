#import docker
from os import path
from consolehelper import ConsoleHelper
from globals import Globals
import datetime
import docker
from navigationcontroller import NavigationController

class DockerController:
    # -------------------------------------------------------------------------------------------------
    # A class for controlling interactions with the docker sdk
    def __init__(self):
        # initialise a ec2Resource
        self.client = docker.from_env()
        # initialise cloud watch controller
    # -------------------------------------------------------------------------------------------------
    # This protected method returns all instances
    def __list_containers(self):
        repeat = True
        while repeat:
            ConsoleHelper.clear()
            self.__print__header()
            index=0
            for container in self.client.containers.list(all=True):
              index+=1
              self.__print_container(index,container)
            repeat = self.__perform_action()
    # --------------------------------------------------------------------------------------------------
    # This is the main method for this controller
    def load_screen(self):
        self.__list_containers()
    # -------------------------------------------------------------------------------------------------
    # This method prints container instance
    def __print_container(self, index,container):
            print(f"{index}. {container.short_id}\t{container.status}\t{container.image}\t{container.name}\n")
    # ------------------------------------------------------------------------------------------------------------
    # This method prints header row for containers
    def __print__header(self):
        print("\033[4m\tID\tStatus\tImage\t\t\t\tName\033[0m\n")    
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
    # ------------------------------------------------------------------------------------------------------------
    # This method runs a container
    def __run_container(self):
        image=ConsoleHelper.get_alphanumeric_input("Please enter the image name (Local or from docker hub):\t")
        print(f"Running container using {image} image in the background....")
        container=self.client.containers.run(image=image,detach=True)
        print(container.logs())
    # ------------------------------------------------------------------------------------------------------------
    # This method shows local images
    def __list_local_images(self):
         print("Local Images")
         print("\033[4m\tId\t\tTag\033[0m\n")
         index=0
         for image in self.client.images.list():
             index+=1
             print(f"{index}. {image.short_id.replace('sha256:','')}\t{image.tags}\n")
         if index==0:
             ConsoleHelper.print_warning("No local images found!\n")
    # ------------------------------------------------------------------------------------------------------------
    # This method stops a container
    def __stop_container(self):
        identifier=ConsoleHelper.get_alphanumeric_input("Please enter the container name or id:\t")
        container=self.client.containers.get(identifier)
        container.stop()
        ConsoleHelper.print_success("The container is stopped!")
    # ------------------------------------------------------------------------------------------------------------
    # This method removes containers which are in "exited" status
    def __remove_container(self):
        confirm=ConsoleHelper.get_yes_no_input("Are you sure to remove all containers? (Y/N):\t")
        if confirm:
            index=0
            for container in self.client.containers.list(filters={"status":"exited"}):
                index+=1
                container.remove(force=True,v=True)
            if index==0:
                ConsoleHelper.print_warning("There are no exited containers to be removed!")
            else:
                ConsoleHelper.print_success(f"{index} container(s) are removed!")
        else:
            ConsoleHelper.print_warning("The container removal aborted!")
    # ------------------------------------------------------------------------------------------------------------
    # This method allows user to create a docker image
    def create_image(self):
        ConsoleHelper.clear()
        imageName=ConsoleHelper.get_alphanumeric_input("Please enter a image name:\t")
        filePath=ConsoleHelper.get_alphanumeric_input("Please enter python file path:\t")
        pythonVersion=ConsoleHelper.get_number_input(1,2,"Which version of python is used\n 1. v2.7 \t 2. v3.10\n")
        if pythonVersion==1:
            pythonVersion="python2"
        else:
            pythonVersion="python"
        contents=f"FROM ubuntu\n"
        contents+=f"RUN apt-get update\n"
        contents+=f"RUN apt-get install -y {pythonVersion}\n"
        contents+=f"ADD {filePath} /home/{filePath}\n"
        contents+=f'CMD ["/home/{filePath}"]\n'
        contents+=f'ENTRYPOINT ["{pythonVersion}"]\n'
        self.__create_dockerfile(contents)
        ConsoleHelper.print_success("Dockerfile is created!\n")
        print("Creating docker image...\n")
        self.client.images.build(path="./",tag=imageName)
        ConsoleHelper.print_success(f"A python app image is created with name {imageName}!\n")
        print("Running a container using the image...")
        container=self.client.containers.run(image=imageName,detach=True)
        print(container.logs())
        input("Press any key to continue..")

    # ------------------------------------------------------------------------------------------------------------
    # This method creates a dockerfile in the current directory
    def __create_dockerfile(self,contents):
        f = open("Dockerfile", "w")
        f.write(contents)
        f.close()
      
