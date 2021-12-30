#import docker
from consolehelper import ConsoleHelper
import docker
from navigationcontroller import NavigationController
import os
class DockerController:
    # -------------------------------------------------------------------------------------------------
    # A class for controlling interactions with the docker sdk
    def __init__(self):
        # initialise a docker client
        self.client = docker.from_env()

    # -------------------------------------------------------------------------------------------------
    # This protected method returns all containers
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
            imageName="\t\t\t"
            if len(container.image.tags)>=1:
               imageName=f"{container.image.tags[0]}\t"
            print(f"{index}. {container.short_id}\t{container.status}\t{imageName}\t{container.name}\n")
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
        stream = container.logs(stream =True)
        self.__print_stream(stream)
        ConsoleHelper.print_success("Container run initiated in the background.")
    # ------------------------------------------------------------------------------------------------------------
    # This method stops a container
    def __stop_container(self):
        loop=True
        while loop:
            identifier=ConsoleHelper.get_alphanumeric_input("Please enter the container name or id (Press 0 to cancel the operation):\t")
            if identifier=="0":
                loop=False
            else:
                container=self.client.containers.get(identifier)
                if container.status.lower()=="exited" or container.status.lower()=="created":
                    ConsoleHelper.print_warning("This container is not running currently!")
                else:
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
        imageName=ConsoleHelper.get_alphanumeric_input("Please enter the name for new python app image:\t")
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
        stream = container.logs(stream =True)
        self.__print_stream(stream)
        input("Press any key to continue..")
    # ------------------------------------------------------------------------------------------------------------
    # This method prints the byte stream passed to it
    def __print_stream(self, stream):
        print(f'============= Log starts ============')
        try:
            while True:
                # read next line from stream
                line = next(stream).decode("utf-8")
                print(line)
        except StopIteration:
            print(f'============= Log ends ============')

    # ------------------------------------------------------------------------------------------------------------
    # This method creates a dockerfile in the current directory
    def __create_dockerfile(self,contents):
        f = open("Dockerfile", "w")
        f.write(contents)
        f.close()
    # ------------------------------------------------------------------------------------------------------------
    # This method provisions container group for sample wordsmith docker app https://github.com/dockersamples/k8s-wordsmith-demo 
    def provision_docker_compose_app(self): 
        ConsoleHelper.clear()
        print("Provisioning docker sample 'Wordsmith' app\n")
        # run the docker compose in background
        os.system("docker-compose up -d")
        ConsoleHelper.print_success("Provisioning is completed. Please visit http://localhost:8080/ to see the app working.")
        confirm=ConsoleHelper.get_yes_no_input("Do you want to shutdown the wordsmith app? (Y/N)")
        if confirm:
            print("Shutting down docker sample 'Wordsmith' app\n")
            os.system("docker-compose down")
            ConsoleHelper.print_success("App is shutdown.")
        input("Press any key to continue..")
        

