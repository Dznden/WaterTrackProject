'''
Details: Test idea for water consumption tracker (2nd idea version)
Created By: Jayden Xinchen Du
Created Date: 14/1/2025
Version = '1.0'
'''
def user_goal():
    """
    Purpose: Allows user to choose their own water consumption goal
    Parameters: None
    Returns: daily_goal (str)
    """

    is_float = False
    while is_float == False:
        daily_goal = input("Input your daily water consumption goal: ")
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
    show_menu = True
    while show_menu ==True:
        print("==================================")
        print("Let's get started! Choose one of the following options: ")
        print("1. Enter your own daily water consumption goal")
        print("2. I'm not sure about my goal, please calculate it for me")
        print("==================================")
        option = input("")
        if option == "1":
            daily_goal = user_goal()
        elif option =="2":
            daily_goal = goal_calculate()
        return_menu = input("Would you like to return to menu (Y/N): ")
        if return_menu =="Y":
            show_menu = True
        elif return_menu =="N":
            show_menu = False

    print("EXITED MENU SCREEN")
        

menu()

