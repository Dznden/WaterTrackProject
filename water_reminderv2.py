'''
Details: Test idea for water consumption tracker (2nd idea version)
Created By: Jayden Xinchen Du
Created Date: 14/1/2025
Last updated: 18/1/2025
Version = '1.5'
'''
import datetime as dt
import time as tm 
import re
import schedule # external library
import threading
'''
TO DO LIST:
1. get rid of all symbols for clock 24 hour validate ->dictionary (rn only - but need to rid all symbols)

2. Add validator for number of reminders a day

3. Maybe add calendar module (Not sure yet)

4. Unit needs to change bug for water logging if go back to menu
'''



# need function to edit email message
'''
from time import sleep
from datetime import datetime
from email.message import EmailMessage

email_sender = 'xinchendu17@gmail.com' # my dummy email
email_password = 'zvxw sttx qxzz nujs'
email_receiver = '...' # user must input

def send_email(subject, body):
    """
    Purpose: Send email to user
    Parameters: current_unit
    Returns: daily_goal (str)
    """
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
class Water_container():
    """
    Purpose: Allow user to log water consumption to meet daily goal and show progress left to reach goal
    Parameters: 
    Returns: None
    """
    def __init__(self, goal, unit):
        '''
        Purpose: Creates container capacity (goal)
        '''
        self.capacity = goal
        self.original_capacity = goal
        self.unit = unit
    def drank_water(self, vol_drank):
        self.capacity = self.capacity - vol_drank

    def __str__(self):
        '''
        Purpose: Returns string representation of how much left of daily goal
        '''
        if self.capacity <0:
            return f'You have already exceeded your daily goal by {-(self.capacity)} {self.unit}\n\nYou have drank in total {self.original_capacity -(self.capacity)} {self.unit}'
        return f'You have {self.capacity:.3f} {self.unit} left'
def water_logging(daily_goal, added_object =None): # currently bugged, need to ensure its same object
    """
    Purpose: Allow user to log water consumption to meet daily goal and show progress left to reach goal
    Parameters: 
    Returns: None
    """
    # Unit needs to change bug
    print(f'The daily goal is: {daily_goal}')
    goal_val = float(daily_goal[0])
    goal_unit = daily_goal[1]
    if added_object == None: # If first time logging in water consumption
        goal_left = Water_container(goal_val, goal_unit)
    else:
        goal_left = added_object
    add_water = input(f"Input the amount of water consumed in {goal_unit}: ") # NEED VALIDATE INPUT
    goal_left.drank_water(float(add_water))
    print(goal_left)
    return goal_left

def remove_reminder():
    """
    Purpose: Remove current reminder
    Parameters: 
    Returns: None
    """
    remove_reminder = input("Confirm remove reminder (Y/N): ")
    if remove_reminder =='Y':
        return True

def scheduler_settings(reminder, daily_goal):
    """
    Purpose: Settings for scheduler
    Parameters: 
    Returns: None
    """

    goal_left = None
    num_option = 4
    while True:
        tm.sleep(5)
        print("==================================\n")
        print("1. Remove reminder\n")
        print("2. Change reminder\n")
        print("3. Water loggings\n") 
        print("4. Exit scheduler menu (Go back to main menu)\n")
        print("==================================")
        
        setting_option = input("Choose a choice: ")
        setting_option = choice_validator(setting_option, num_option)
        if setting_option =="1":
            reminder_remove = remove_reminder()
            if reminder_remove ==True:
                scheduler_run(reminder, stop_status = True) # **Need to add message about how scheduler is already removed**
        elif setting_option =="2":
            total_wake_time(daily_goal)
        elif setting_option =="3":
            goal_left = water_logging(daily_goal, goal_left)
        elif setting_option =="4":
            menu(daily_goal)

        
def scheduler_run(reminder, stop_status = False):
    """
    Purpose: Run scheduler in background
    Parameters: 
    Returns: None
    """
    ''' # Pre thread structure
    while True: # Ensure scheduler is constantly running
        schedule.run_pending()
        tm.sleep(1)
        if stop_status == True:
            schedule.cancel_job(reminder)
            print("REMINDER SUCCESSFULLY REMOVED!")
    '''
 # Thread structure
    continue_run = True
    while continue_run==True:
        schedule.run_pending()
        tm.sleep(1)
        if stop_status == True:
            schedule.cancel_job(reminder)
            print("REMINDER SUCCESSFULLY REMOVED!")
            continue_run =False

        
def schedule_offset(time_wakeup, reminder_elapse, reminder_active):
    """
    Purpose: Offset schedule if person awake between two separate days (ensure no schedule error)
    Parameters: 
    Returns: None
    """
    # NEED DEBUG schedulevalue error
    current_time = dt.datetime.now().strftime("%H:%M:%S")
    #print(f'Test current_time = {current_time}')
    current_time = current_time.split(':')
    #time_bedtime = dt.timedelta(hours = int(bedtime[0]), minutes = int(bedtime[1]))
    reminder_active_offset = dt.timedelta(hours = int(current_time[0]), minutes = int(current_time[1]), seconds = int(current_time[2])) - time_wakeup
    print(f'Current time: {current_time}')
    print(f'time_wakeup: {time_wakeup}')

    reminder_active_offset = (reminder_active_offset).total_seconds()
    print(f'reminder active offset: {reminder_active_offset}') 


    offset_time_limit = dt.datetime.now() + dt.timedelta(seconds = reminder_active - reminder_active_offset - 3600)
    print(f'Test time offset: {offset_time_limit}',f'reminder elapse time = {reminder_elapse} s') # working

    reminder = schedule.every(reminder_elapse).seconds.until(offset_time_limit).do(test_function) # not working, schedule.ScheduleValueError: Cannot schedule a job to run until a time in the past

    return reminder

def scheduler(time_bedtime, total_awake, time_wakeup, daily_goal):
    """
    Purpose: Allows user to set schedule for reminder
    Parameters: time_bedtime, total_awake
    Returns: None
    """
    reminder_limit = time_bedtime - dt.timedelta(hours = 1) # Ensure that there are no reminders after 1 hour before bedtime (unhealthy to drink at night)
    print(f'TEST: {reminder_limit}')
    reminder_active = total_awake.total_seconds()
    num_reminder = input("How many times would you like to be reminded to complete your daily goal? ") # NEED VALIDATOR
    reminder_elapse = reminder_active/int(num_reminder) # reminder elapse time

    time_fmt = str(reminder_limit).split(":") # break apart into HH and MM components for limit
    hours = int(time_fmt[0])
    minutes = int(time_fmt[1])
    #print(f'REMINDER ELAPSED: {reminder_elapse}')
    #print(f'TEST REMINDER_LIMIT {time_fmt[0], time_fmt[1]}')
    print(f'time_bedtime = {time_bedtime}', f' time_wakeup = {time_wakeup}')
    if time_bedtime<time_wakeup: # if person awake between 2 different days (but still less than 24 hours), eg. ensure 2am sleep time is not of the past
        print("OFFSET EXECUTED...")
        reminder = schedule_offset(time_wakeup, reminder_elapse, reminder_active)
    else:
        print(f'reminder time elapse = {reminder_elapse} s')
        reminder = schedule.every(reminder_elapse).seconds.until(dt.time(hours, minutes)).do(test_function) # need to later insert email function
    #remove_reminder = input("Remove reminder (Y/N): ") # have menu that asks to get to here at the beginning of function logic

    # To run settings and scheduler simultaneously
    thread1 = threading.Thread(target = scheduler_run, args = (reminder,)) # start run scheduler in the background, needed to remove scheduler at any point in time
    thread1.start()
    thread2 = threading.Thread(target = scheduler_settings, args = (reminder,daily_goal))
    thread2.start()
    #reminder_status = scheduler_settings()
    '''
    if reminder_status == 'True': # indicate manual removal of scheduler
        print("REMOVING REMINDER...")
        scheduler_run(reminder, reminder_status)
    '''
''' # has own custom run function now
    while True: # Ensure scheduler is constantly running
        schedule.run_pending()
        tm.sleep(1)
        #if remove_reminder =='Y':
            #schedule.cancel_job(reminder)
'''
def test_function():
    """
    Purpose: Tests if scheduler is working as intended (Temporary function)
    Parameters: None
    Returns: None
    """
    print("DONE")



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
    return [daily_goal, current_unit]

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
    return [str(daily_goal), current_unit]

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

def total_wake_time(daily_goal):
    """
    Purpose: Calculate total wake time to spread out reminders throughout day
    Parameters: None
    Returns: None
    """
    print("==================================\n")
    print("Lets set a reminder scheduler\n")
    wakeup = input("Enter the time that you wake up (24 hour time): ")
    wakeup = clock_validator(wakeup)
    bedtime = input("Enter your sleep time (24 hour time): ") # need to validate input 
    bedtime = clock_validator(bedtime)
    print("==================================")

    wakeup = wakeup.split(':')
    print(wakeup)
    time_wakeup = dt.timedelta(hours = int(wakeup[0]), minutes = int(wakeup[1]))
    print(time_wakeup)

    bedtime=bedtime.split(':')
    time_bedtime = dt.timedelta(hours = int(bedtime[0]), minutes = int(bedtime[1]))
    print(time_bedtime)
    total_awake = time_bedtime - time_wakeup

    if total_awake.total_seconds()<0: # adding extra day if sleep next day
        total_awake = total_awake + dt.timedelta(days=1)
    print(total_awake)
    total_seconds = total_awake.total_seconds()
    minutes = (total_seconds//60)
    hours = total_seconds//(3600)
    min_remainder=minutes%60
    print(f'Your total wake time is: {int(hours)} h {int(min_remainder)} m')
    print("TESTING SCHEDULER")
    scheduler(time_bedtime, total_awake,time_wakeup, daily_goal)

def choice_validator(choice, num_option):
    """
    Purpose: validates numbered choice
    Parameters: choice (str), num_option (int)
    Returns: choice (str)
    """
    valid_choice = False
    while valid_choice ==False:
        try:
            choice = int(choice)
            if choice>0 and choice<=num_option: # Ensure option chosen is a valid option number
                return str(choice)
            else:
                print("Your choice is not an option, please try again!")
                choice = input("Your number choice: ")
        except ValueError: # If datatype is not an integer
            print("Your choice is not an option, please try again!")
            choice = input("Your number choice: ")

def clock_validator(time):
    """
    Purpose: validates 24 hour time input HH:MM
    Parameters: time (str)
    Returns: None
    """
    print() # test
    valid = False
    while valid ==False:
        if len(time)<6 and (time[2]==':' or (time[1] and len(time)==4)):
            valid =True
        else:
            print("Please ensure that the time is in HH:MM format")
            time = input("Re-enter your time: ")
        time_list = time.split(':')
        try: 
            hours = time_list[0]
            minutes = time_list[1]
            if len(re.findall("-", time))>0 or int(hours)>24 or int(minutes)>60: #ensure no negative symbols at all and correct numbers
                print("The time is in 24 hour format!")
                time = input("Re-enter your time: ")
                valid = False
        except ValueError:
            print("Please ensure that the time is in HH:MM format")
            time = input("Re-enter your time: ")
            valid = False
    return time

def unit_changer_menu(current_unit):
    """
    Purpose: Show menu of all unit changing options
    Parameters: None
    Returns: None
    """
    show_unit_menu = True
    num_option = 4
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
        unit_option = choice_validator(unit_option, num_option)
        if unit_option =="1":
            unit = cust_bottle(current_unit)
            show_unit_menu = False
        elif unit_option =="2":
            if current_unit =='L': # can be edited to be more efficient
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

def menu(daily_goal = None):
    """
    Purpose: Display main menu choices
    Parameters: None
    Returns: None
    """
    # need to fix main menu (currently looks ugly)
    current_unit = "L"
    show_menu = True
    num_option = 4
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
        option = choice_validator(option, num_option)
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
    total_wake_time(daily_goal)
    print("EXITED MENU SCREEN")
#clock_validator("2:70")    
if __name__ =="__main__":
    menu()
    
# total_wake_time()

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

# difficulty = debugging for time
# difficulty with having functions run simultaneously (run scheduler and settings)
