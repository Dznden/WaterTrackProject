'''
Details: Test idea for water consumption tracker (2nd idea version)
Created By: Jayden Xinchen Du
Created Date: 14/1/2025
Last updated: 15/1/2025
Version = '1.1'
'''

def user_goal():
    """
    Purpose: Allows user to choose their own water consumption goal
    Parameters: None
    Returns: daily_goal (str)
    """

    is_float = False
    while is_float == False:
        daily_goal = input("Input your daily water consumption goal (L): ")
        is_float = only_float(daily_goal)
    return daily_goal

def goal_calculate():
    """
    Purpose: Calculate recommended volume of water needed daily as per google recommendations
    Parameters: None
    Returns: daily_goal (str)
    """
    is_float = False
    while is_float == False:
        body_weight = input("Enter your bodyweight (in kg): ")
        is_float = only_float(body_weight)
    daily_goal = float(body_weight) * 0.03
    print(f"Your calculated daily water consumption goal is {daily_goal} L")
    return str(daily_goal)

def only_float(input_to_validate):
    """
    Purpose: Ensure only float are allowed as input, validation
    Parameters: daily_goal
    Returns: is_float (bool)
    """
    try:
        input_to_validate = float(str(input_to_validate))
        is_float = True

    except ValueError:
        is_float = False
    return is_float

def menu():
    """
    Purpose: Display main menu choices
    Parameters: None
    Returns: None
    """
    # need to fix main menu (currently looks ugly)
    show_menu = True
    while show_menu ==True:
        print("==================================\n")
        print("Let's get started! Choose one of the following options: \n")
        print("1. Enter your own daily water consumption goal\n")
        print("2. I'm not sure about my goal, please calculate it for me\n")
        print("3. Terminate program\n") 
        print("==================================")
        # need to validate 1, 2, 3 options
        option = input("Your number choice: ")
        if option == "1":
            daily_goal = user_goal()
        elif option =="2":
            daily_goal = goal_calculate()
        elif option =="3":
            print("Program terminated")
            return None
        return_menu = input("Would you like to return to menu (Y/N): ")
        if return_menu =="Y":
            show_menu = True
        elif return_menu =="N":
            show_menu = False
        # need to validate (Y/N) option input
    print("EXITED MENU SCREEN")
        

menu()


# IDEAS TO DO LIST:
# next idea is to implement times for reminder (choose times)
# ask user for their usual bedtime and wake up time
# if user wants to drink water 1 hour before bed give warning about disrupt sleep
# distribute water across all waking hours - 1
# input bottle volume information
# ask user how often they want to get reminded (to distribute how many reminders a day)
# link to calendars or email (ask to enter user email?)

# scroll wheel gui for volume/bottles
# heat map streak
# sensor on bottle to calculate volume poured (automation)
# simulation of water bottle drained (holding key while drinking)
