'''
Details: Test idea for water consumption tracker (2nd idea version)
Created By: Jayden Xinchen Du
Created Date: 14/1/2025
Last updated: 15/1/2025
Version = '1.2'
'''
'''
from time import sleep
from datetime import datetime
from email.message import EmailMessage

email_sender = 'xinchendu17@gmail.com' # my dummy email
email_password = 'zvxw sttx qxzz nujs'
email_receiver = '...' # user must input

def send_email(subject, body):
    current_time = datetime.now()

    # Format the timestamp as a string
    timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
    msg = f'Reminder to drink your water, you have {volume_left} {chosen_unit} to drink' 
    subject = 'Water drinking reminder'
    body = f'message: {msg} log time: {timestamp_str}'
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
'''
def user_goal(current_unit):
    """
    Purpose: Allows user to choose their own water consumption goal
    Parameters: current_unit
    Returns: daily_goal (str)
    """

    is_float = False
    while is_float == False:
        daily_goal = input(f"Input your daily water consumption goal {current_unit}: ")
        is_float = only_float(daily_goal)
    return daily_goal

def goal_calculate(current_unit):
    """
    Purpose: Calculate recommended volume of water needed daily as per google recommendations
    Parameters: current_unit
    Returns: daily_goal (str)
    """
    is_float = False
    while is_float == False:
        body_weight = input("Enter your bodyweight (in kg): ")
        is_float = only_float(body_weight)
    if current_unit =="L":
        daily_goal = float(body_weight) * 0.03
    elif current_unit =="mL":
        daily_goal =float(body_weight) * 0.03 * 1000
    elif current_unit[0] == "bottle mL":
        daily_goal =(float(body_weight) * 0.03 * 1000)/current_unit[1]
        current_unit = 'bottles'
    elif current_unit[0]=="bottle L":
        daily_goal = (float(body_weight) * 0.03)/current_unit[1]
        current_unit = 'bottles'

    print(f"Your calculated daily water consumption goal is {daily_goal} {current_unit}")
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

def cust_bottle(current_unit):
    """
    Purpose: Change units of drinking into custom bottle volume
    Parameters: current_unit
    Returns: None
    """
    if current_unit[0] =='bottle L':
        current_unit = 'L'
    elif current_unit[0] =='bottle mL':
        current_unit = 'mL'
    bottle_size = float(input(f"Input your bottle volume in {current_unit}: ")) # need to validate response
    return [f"bottle {current_unit}", bottle_size] # need to see if work


def unit_changer_menu(current_unit):
    """
    Purpose: Show menu of all unit changing options
    Parameters: None
    Returns: None
    """

    show_unit_menu = True
    while show_unit_menu ==True:
        print("==================================\n")
        print(f"Your current unit is: {current_unit}") # maybe change to if statement to fix bottle unit to be more user friendly
        print("Choose one of the following units:\n")
        print("1. Custom bottle size\n")
        print("2. Litres (L)\n")
        print("3. millilitres (mL)\n")
        print("4. Exit unit menu\n") 
        print("==================================")
        unit_option = input("Your number choice: ")
        if unit_option =="1":
            unit = cust_bottle(current_unit)
            show_unit_menu = False
        elif unit_option =="2":
            if current_unit =='L':
                print("You are currently in this unit, please choose a different unit!")
            else: # when unit isn't already L
                unit = 'L'
                show_unit_menu = False
        elif unit_option =="3":
            if current_unit=="mL":
                print("You are currently in this unit, please choose a different unit!")
            else: # when unit isn't already mL
                unit = 'mL'
                show_unit_menu = False
        elif unit_option == "4":
            unit = current_unit
            show_unit_menu = False
    return unit

def menu():
    """
    Purpose: Display main menu choices
    Parameters: None
    Returns: None
    """
    # need to fix main menu (currently looks ugly)
    current_unit = "L"
    show_menu = True
    while show_menu ==True:
        print("==================================\n")
        print("Let's get started! Choose one of the following options: \n")
        print("1. Enter your own daily water consumption goal\n")
        print("2. I'm not sure about my goal, please calculate it for me\n")
        print("3. Change water consumption units\n")
        print("4. Terminate program\n") 
        print("==================================")
        # need to validate 1, 2, 3, 4 options
        option = input("Your number choice: ")
        if option == "1":
            daily_goal = user_goal(current_unit)
        elif option =="2":
            daily_goal = goal_calculate(current_unit)
        elif option =="3":
            current_unit = unit_changer_menu(current_unit)
        elif option =="4":
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

# need to do something about daily goal info
# need validate user input

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
