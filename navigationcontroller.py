########################################
#     This is the file 'navigation.py'    #
########################################
import json
from consolehelper import ConsoleHelper
from globals import Globals


class NavigationController:
    # -------------------------------------------------------------------------------------------------
    # A class for showing all the navigation options. This class has methods which will read the menu.json file and display the menu structure
   def __init__(self):
       # load menu from json file
        self.__load_menu_json()
        NavigationController._selectedTopMenu=None
    # ------------------------------------------------------
    # This method loads the menu data from the json file.
   def __load_menu_json(self):
       # Opening menu JSON file
       menuFile = open('menu.json')
       # returns JSON object as # a dictionary
       NavigationController._menuData = json.load(menuFile)
       # Closing file
       menuFile.close()
   # ------------------------------------------------------
   # This method displays menu based on logged in user's role and retrieves user input
   def display_menu(self):
       # show level 1 menu
       ConsoleHelper._breadcrumb=["Home"]
         # if nothing is selected on top menu then show top menu and ask for selection
       NavigationController._selectedTopMenu=self.__print_menu(NavigationController._menuData,1);
       ConsoleHelper.append_breadcrumb(NavigationController._selectedTopMenu['name']);
       # return the selected topmmenu
       return NavigationController._selectedTopMenu
    # ------------------------------------------------------
   # This method prints the menu and returns user selection
   def __print_menu(self,menu,level):
        ConsoleHelper.clear();
        filteredMenu=self.__filter_admin_menu(menu)
        index=0
        for menuItem in filteredMenu:
            index+=1
            print(f"{index}. {menuItem['name']}")
        selectedIndex= ConsoleHelper.get_number_input(0,index,"Please enter your selection \t");
        if selectedIndex==0:
            # user pressed back button, so reload the top menu
            if level==2:
              # user wants to re load top menu
              self._selectedTopMenu=None;
        else:
         # get the menu item which was selected by user
         selectedMenuItem=filteredMenu[selectedIndex-1]
         return selectedMenuItem;
   # ------------------------------------------------------
   # This method filters menu based on user's role
   @staticmethod
   def __filter_admin_menu(menu):
       loggedInUser=Globals._logged_in_User
       if loggedInUser and not loggedInUser._isAdmin:
           # user is not admin, so we need to filter the menu and return
           return list(filter(lambda m: not m["admin"],menu))
       return menu
   # ------------------------------------------------------
   # This method prints all actions available under current selected menu
   @staticmethod
   def print_actions(selectedMenu=None):
       currentSelectedMenu=NavigationController._selectedTopMenu if selectedMenu is None else selectedMenu
       if currentSelectedMenu is None:
           ConsoleHelper.print_warning("No actions available!")
       else:
           # get the actions belonging to top menu
           actions=list(currentSelectedMenu["actions"])
           actions=NavigationController.__filter_admin_menu(actions)
           index=0
           actionString="Please choose an action\n"
           for action in actions:
               index+=1
               actionString+=f"{index}. {action['name']}\t"
           selectedIndex=ConsoleHelper.get_number_input(0,len(actions),f"{actionString}\n")
           if selectedIndex==0:
               return None
           else:
               selectAction=actions[selectedIndex-1]
               return selectAction
               
               
       
       
       
   