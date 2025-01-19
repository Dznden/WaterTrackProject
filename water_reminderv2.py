'''
Details: Idea for water consumption tracker (2nd idea version), essentially ask user how often they want to get reminded (to distribute how many reminders a day) over their wake up time for scheduled email notifications to drink water
Created By: Jayden Xinchen Du (34954775)
Created Date: 14/1/2025
Last updated: 19/1/2025
Version = '1.9'
'''
import datetime as dt
import time as tm 
import re
import schedule     # external library
import threading
import smtplib
from email.message import EmailMessage

email_sender = 'securebyte1@gmail.com'  # my dummy email
email_password = 'zvxw sttx qxzz nujs'

def send_email(goal_left, chosen_unit, email_receiver, subject = None, body = None): 
    """
    Purpose: Send email to user
    Parameters: goal_left, chosen_unit, email_receiver, subject (optional), body (optional)
    Returns: None
    """
    current_time = dt.datetime.now()
    timestamp_str = current_time.strftime("%Y-%m-%d %H:%M:%S")

    if isinstance(chosen_unit, list):   # bottle unit (checks if list)
        converted_unit = re.search(r'\w+\s*$',chosen_unit[0])   # Last word in first item of list (which is unit)
        converted_unit = converted_unit.group()
        chosen_unit = f'bottles ({chosen_unit[1]} {converted_unit})'

    if body ==None:     # Default email format (without custom change)
        msg = f'Reminder to drink your water, you have {goal_left} {chosen_unit} left to drink' 

    if subject ==None:
        subject = 'Water drinking reminder'

    else:
        msg = []
        for sentence in range(len(body)):
            sentence = f'{sentence}\n'
            msg.append(sentence)
        msg = ''.join(msg)
    
    body = f'Message: {msg}\nLog time: {timestamp_str}'
    
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    try:    # Process to send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_sender, email_password)
            smtp.send_message(em)
            print("Email sent successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")

class Water_container():
    """
    Purpose: Allow user to log water consumption to meet daily goal and show progress left to reach goal
    """
    def __init__(self, goal, unit):
        '''
        Purpose: Creates container capacity (goal)
        '''
        self.capacity = goal
        self.original_capacity = goal
        self.unit = unit

    def drank_water(self, vol_drank):
        '''
        Purpose: Provide how much capacity left until complete goal
        '''
        self.capacity = self.capacity - vol_drank

    def bottle_to_volume(self, volume):
        '''
        Purpose: Convert bottles into its respective volume
        '''
        volume = volume * (self.original_capacity -(self.capacity))
        return volume

    def __str__(self, volume = None, unit = None):
        '''
        Purpose: Returns string representation of how much left of daily goal
        '''      
        total_consumed = self.original_capacity -(self.capacity)
        try:
            if self.capacity <0:    # If exceed daily goal
                return f'You have already exceeded your daily goal by {-(self.capacity):.2f} {self.unit}\nYou have drank in total {total_consumed:.2f} {self.unit}'
            elif self.capacity<0 and re.search('^bottle', self.unit[1][0]):     # If bottle unit and exceed daily goal
                return f'You have already exceeded your daily goal by {-(self.capacity):.2f} {self.unit}\n\nYou have drank in total {total_consumed:.2f} {self.unit}]\nYou have drank an equivalent to {volume} {unit}'
            elif self.capacity>0 and re.search('^bottle', self.unit[1][0]):     # If bottle unit and haven't exceeded goal
                return f'You have {self.capacity:.2f} {self.unit} left\nYou have drank in total {total_consumed:.2f} {self.unit}\nYou have drank an equivalent to {volume} {unit}' 
            else: 
                return f'You have {self.capacity:.2f} {self.unit} left\nYou have drank in total {total_consumed:.2f} {self.unit}'
        except IndexError:  # normal unit (not bottle unit)
            return f'You have {self.capacity:.2f} {self.unit} left\nYou have drank in total {total_consumed:.2f} {self.unit}'

def water_log_validator(water_consumed, goal_unit):
    """
    Purpose: Validate water logging (must be float)
    Parameters: water_consumed, goal_unit
    Returns: water_consumed (str)
    """
    valid = False
    while valid == False:
        try:
            water_consumed = float(water_consumed)
            return str(water_consumed)
        except ValueError:      # If cannot convert into float as not number
            print("Your input is invalid, must be a number!")
            water_consumed = input(f"Input the amount of water consumed in {goal_unit}: ")

def water_logging(daily_goal, added_object =None): 
    """
    Purpose: Allow user to log water consumption to meet daily goal and show progress left to reach goal
    Parameters: daily_goal, added_object (optional)
    Returns: goal_left (obj)
    """
    volume = None
    bottle_unit = re.search('^bottle',daily_goal[1][0])

    if bottle_unit:     # If first word is bottle
        volume = daily_goal[1][1]
        temp_unit = bottle_unit.group()
        print(f'Your daily goal is: {daily_goal[0]} {temp_unit}s')
        goal_unit = f'{temp_unit}s'
    else:
        goal_unit = daily_goal[1]
        print(f'Your daily goal is: {daily_goal}')
    goal_val = float(daily_goal[0])

    if added_object == None:    # If first time logging in water consumption
        goal_left = Water_container(goal_val, goal_unit)
    else:
        goal_left = added_object
    print("NOTE: if you added too much water, enter a negative value to reverse the water added")
    add_water = input(f"Input the amount of water consumed in {goal_unit}: ") 
    add_water = water_log_validator(add_water, goal_unit)
    if volume!=None:    # convert bottles into volume
        converted_unit = re.search(r'\w+\s*$',daily_goal[1][0])     # last word (extracting unit)
        converted_unit = converted_unit.group()
        goal_left.drank_water(float(add_water))
        volume = goal_left.bottle_to_volume(volume)
    else:
        goal_left.drank_water(float(add_water))
    print(goal_left)
    return goal_left

def remove_reminder():
    """
    Purpose: Remove current reminder
    Parameters: None
    Returns: True (bool)
    """
    remove_reminder = input("Confirm remove reminder (Y/N): ") 
    if remove_reminder =='Y':
        return True
    else:
        return False
    
def email_setup(email = None, current_unit = None, daily_goal = None, goal_left = None):
    """
    Purpose: Get user email/change user email
    Parameters: email (optional), current_unit (optional), daily_goal (optional), goal_left (optional)
    Returns: None
    """ 

    if email !=None: # change current email
        choice = input("Are you sure you want to change your email? (Y/N)")
        binary_option_validator(choice)
        if choice in ['y','yes']:
            user_email = input("Input your new email: ")
            user_email = email_validator(user_email)
        elif choice in ['n', 'no']:
            email_settings(daily_goal, current_unit, email, goal_left)
    else:
        user_email = input("Enter your email: ")
        user_email = email_validator(user_email)
        return user_email

def change_email_content(content_type): # havent implemented
    """
    Purpose: Changing email reminder content
    Parameters: content_type
    Returns: input_list (lst)
    """
    input_list = []
    if content_type =='body':
        print("Type your email body content here: ")
        print("To type a new line, just press enter on keyboard")
        print("Indicate the end of your email by typing 'end'")
    elif content_type =="subject":
        print("Type your email subject here: ")
        print("To type a new line, just press enter on keyboard")
        print("Indicate the end of your email by typing 'end'")
    message = None
    while message != 'end':
        message = input("")
        input_list.append(message)
    return input_list

def email_content_settings(daily_goal, current_unit, email, goal_left): # havent implemented
    """
    Purpose: Store information of email body and subject
    Parameters: daily_goal, current_unit, email, goal_left
    Returns: None
    """
    num_option = 3
    while True:
        tm.sleep(5)
        print("==================================\n")
        print("1. Change body\n")
        print("2. Change subject\n") 
        print("3. Exit email content (Go back to email menu)\n")
        print("==================================")
        
        setting_option = input("Choose a choice: ")
        setting_option = choice_validator(setting_option, num_option)
        if setting_option =='1':
            email_body = change_email_content('body')
        elif setting_option =='2':
            email_subject = change_email_content('subject')
        elif setting_option =='3':
            email_settings(daily_goal, current_unit, email, goal_left, email_body, email_subject)

        
def email_settings(daily_goal, current_unit, email, goal_left = None, email_body = None, email_subject = None):
    """
    Purpose: Settings for setting up email
    Parameters: daily_goal, current_unit, email (optional), email_body (optional), email_subject (optional)
    Returns: None
    """
    num_option = 4
    while True:
        tm.sleep(5)
        print("==================================\n")
        print("1. Change email\n")
        print("2. Edit email contents\n") 
        print("3. Enter scheduler settings (water loggings)")
        print("4. Go back to main menu)\n")
        print("==================================")
        
        setting_option = input("Choose a choice: ")
        setting_option = choice_validator(setting_option, num_option)
        if setting_option =="1":
            email = email_setup(email, current_unit, daily_goal, goal_left)
        elif setting_option =="2":
            email_content_settings(daily_goal, current_unit, email, goal_left)
        elif setting_option =="3":
            scheduler_settings(daily_goal, current_unit, email, goal_left)
        elif setting_option =="4":
            menu(daily_goal, current_unit)

def scheduler_settings(daily_goal, current_unit, user_email, goal_left = None):
    """
    Purpose: Settings for scheduler
    Parameters: daily_goal, current_unit, goal_left (optional)
    Returns: None
    """
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
                scheduler_run(stop_status = True)   # Need to add message about how scheduler is already removed - Future me problem if i have time
        elif setting_option =="2": 
            confirmation_change = input("Are you sure you would like to change your schedule? (Y/N): ")
            confirmation_change = binary_option_validator(confirmation_change)  # Validate response
            if confirmation_change in ['yes','y']:
                schedule.clear()
                total_wake_time(daily_goal, current_unit, user_email, goal_left)
            elif confirmation_change in ['no','n']:
                continue

        elif setting_option =="3":
            goal_left = water_logging(daily_goal, goal_left)
        elif setting_option =="4":
            menu(daily_goal, current_unit, goal_left, user_email) 

def scheduler_run(stop_status = False):
    """
    Purpose: Run scheduler in background
    Parameters: stop_status (optional)
    Returns: None
    """

    # Thread structure
    continue_run = True
    while continue_run==True:
        schedule.run_pending()
        tm.sleep(1)
        if stop_status == True:
            schedule.clear()    # Clears all jobs at once (all schedules)
            print("REMINDER SUCCESSFULLY REMOVED!")
            continue_run =False
        
def schedule_offset(time_wakeup, reminder_elapse, reminder_active, time_bedtime, user_email, goal_left, current_unit):
    """
    Purpose: Offset schedule if person awake between two separate days (ensure no schedule error)
    Parameters: time_wakeup, reminder_elapse, reminder_active, time_bedtime, user_email, goal_left, current_email
    Returns: reminder_daily (obj)
    """
    current_time = dt.datetime.now().strftime("%H:%M:%S")
    current_time = current_time.split(':')
    reminder_active_offset = dt.timedelta(hours = int(current_time[0]), minutes = int(current_time[1]), seconds = int(current_time[2])) - time_wakeup
    reminder_active_offset = (reminder_active_offset).total_seconds()

    offset_time_limit = dt.datetime.now() + dt.timedelta(seconds = reminder_active - reminder_active_offset - 3600)

    print(f'Time between reminders: {reminder_elapse} s') # Need to implement CONVERT INTO MINUTES then HOURS (SIMPLIFY NEEDED) - FUTURE ME PROBLEM as well :p
    offset_time = offset_time_limit.time()

    reminder_daily = schedule.every().day.at(f'{offset_time}').do(within_day_scheduler, reminder_elapse, offset_time_limit, user_email, goal_left, current_unit, time_bedtime)
    return reminder_daily

def current_day_schedule(reminder_elapse, time_reminder_limit, goal_left, current_unit, email_receiver):
    """
    Purpose: Current day temporary scheduler if its already past wakeup time (most cases) eg. start scheduler immediately at 11:00 when wakeup is 10:00
    Parameters: time_bedtime, total_awake
    Returns: None
    """
    temp_reminder = schedule.every(reminder_elapse).seconds.until(time_reminder_limit).do(send_email, goal_left, current_unit, email_receiver) # reminder for first day

def scheduler(time_bedtime, total_awake, time_wakeup, daily_goal, current_unit, user_email, goal_left = None):
    """
    Purpose: Allows user to set schedule for reminder
    Parameters: time_bedtime, total_awake, time_wakeup, daily_goal, current_unit, goal_left (optional)
    Returns: None
    """

    reminder_limit = time_bedtime - dt.timedelta(hours = 1)     # Ensure that there are no reminders after 1 hour before bedtime (unhealthy to drink at night)
    reminder_active = total_awake.total_seconds()
    num_reminder = input("How many times would you like to be reminded to complete your daily goal? ")  # NEED to implement validator - future me problem :p
    reminder_elapse = reminder_active/int(num_reminder)     # reminder elapse time

    time_fmt = str(reminder_limit).split(":")   # Break apart into HH and MM components for time limit
    hours = int(time_fmt[0])
    minutes = int(time_fmt[1])
    time_reminder_limit = dt.time(hours, minutes)

    print(f'\nTime of bedtime = {time_bedtime}\nTime of wakeup = {time_wakeup}\n')
    print(f'Time between reminders = {reminder_elapse} s')
    if time_bedtime<time_wakeup:    # Situation if person awake between 2 different days (but still less than 24 hours), eg. ensure 2am sleep time is not of the past otherwise schedule error
        reminder_daily= schedule_offset(time_wakeup, reminder_elapse, reminder_active, goal_left, current_unit)
    
    else:   # Within same day sleep and wake up (normal person situation)
        current_time = dt.datetime.now().strftime("%H:%M:%S")
        current_time = current_time.split(':')
        current_time_delta = dt.timedelta(hours = int(current_time[0]), minutes = int(current_time[1]), seconds = int(current_time[2]))
        current_time_sec = current_time_delta.total_seconds()

        if current_time_sec>reminder_limit.total_seconds():     # If scheduler stop is of the past eg. meant to stop at 23:00 but currently 23:30
            reminder_daily = schedule.every().day.at(f'{reminder_limit}').do(within_day_scheduler, reminder_elapse, time_reminder_limit, user_email, goal_left, current_unit, time_bedtime)
            if current_time_sec>time_wakeup.total_seconds():    # Start temporary reminder (for the current day), as past wakeup time
                current_day_schedule(reminder_elapse, time_reminder_limit, goal_left, current_unit, user_email)

        else:
            reminder_daily = schedule.every().day.at(f'{reminder_limit}').do(within_day_scheduler, reminder_elapse, time_reminder_limit, user_email, goal_left, current_unit) # reminder for days imposed after first day
            if current_time_sec>time_wakeup.total_seconds():    # Start temporary reminder (for the current day)
                current_day_schedule(reminder_elapse, time_reminder_limit, goal_left, current_unit, user_email)
              
    # To run scheduler settings and scheduler (notifications) simultaneously in background
    scheduler_run_thread = threading.Thread(target = scheduler_run, args = (reminder_daily,)) 
    scheduler_run_thread.start()
    scheduler_setting_thread = threading.Thread(target = scheduler_settings, args = (daily_goal, current_unit, user_email)) 
    scheduler_setting_thread.start()
  
def within_day_scheduler(reminder_elapse, time_reminder_limit, user_email, goal_left, current_unit, time_bedtime = None):
    """
    Purpose: Schedules reminder within the same day
    Parameters: reminder_elapse, time_reminder_limit, user_email, goal_left, current_unit, time_bedtime (optional)
    Returns: None
    """
    if time_bedtime!=None:  # Situation where scheduler stops in the past, eg. meant to stop 23:00 when it is currently 23:30 which is not yet bedtime of 24:00
        print("The scheduler would've stopped 1 hour before bedtime for maximum health benefits.\nHowever as this is of the past, it will now stop at exactly bedtime")
        reminder = schedule.every(reminder_elapse).seconds.until(time_bedtime).do(send_email, goal_left, current_unit, user_email) 
    else:
        reminder = schedule.every(reminder_elapse).seconds.until(time_reminder_limit).do(send_email, goal_left, current_unit, user_email)

def test_function():    # Just here for testing notifications purposes
    """
    Purpose: Tests if scheduler is working as intended (Temporary function)
    Parameters: None
    Returns: None
    """
    print('DONE')

def email_validator(email_input): 
    """
    Purpose: Ensure valid email input in correct email format
    Parameters: email_input
    Returns: email_input (str)
    """
    pattern = r"[a-zA-Z0-9]+@[a-zA-Z]+\.(com|edu|net)"
    valid_email = False
    while valid_email == False:
        if (re.search(pattern, email_input)):
            print("Email added!")
            valid_email = True
        else:
            print("Invalid email, please try again!")
            email_input = input("Enter your email: ")
    return email_input

def user_goal(current_unit):
    """
    Purpose: Allows user to choose their own water consumption goal
    Parameters: current_unit
    Returns: goal_info (lst)
    """
    pattern = r"bottle\b"

    temp_unit = current_unit
    if re.search(pattern, current_unit[0]):     # If unit is bottle, extract the actual unit out of it for print display
        temp_unit = re.search(r"^\w+", current_unit[0])
        temp_unit = temp_unit.group()
    is_float = False
    while is_float == False:
        daily_goal = input(f"Input your daily water consumption goal ({temp_unit}): ")
        is_float = only_float(daily_goal)
    goal_info = [daily_goal, current_unit]
    return goal_info

def goal_calculate(current_unit):
    """
    Purpose: Calculate recommended volume of water needed daily as per google recommendations
    Parameters: current_unit
    Returns: goal_unit (lst)
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
    goal_unit = [str(daily_goal), current_unit]
    return goal_unit

def only_float(input_to_validate):
    """
    Purpose: Ensure only float are allowed as input, validation
    Parameters: input_to_validate
    Returns: is_float (bool)
    """
    try:
        input_to_validate = float(str(input_to_validate))
        is_float = True
    except ValueError:  # When input cannot convert into float, not a number
        is_float = False
    return is_float

def binary_option_validator(response):
    """
    Purpose: Validates Y/N response
    Parameters: response
    Returns: response (str)
    """
    valid = False
    try:
        response = response.lower()
    except Exception as e:
        print("Your response must be Y/N!")
        print(e)
        response = input("Would you like to return to menu (Y/N): ").lower()
    valid_response = ['y','n','yes', 'no']
    while valid == False:
        if response in valid_response:
            valid = True
        else:
            print("Your response must be Y/N!")
            response = input("Would you like to return to menu (Y/N): ").lower()
    return response

def cust_bottle(current_unit):
    """
    Purpose: Change units of drinking into custom bottle volume
    Parameters: current_unit
    Returns: bottle_info (lst)
    """
    if current_unit[0] =='bottle L':
        current_unit = 'L'
    elif current_unit[0] =='bottle mL':
        current_unit = 'mL'
    bottle_size = float(input(f"Input your bottle volume in {current_unit}: ")) # Need to validate response - future me problem :p
    bottle_info = [f"bottle {current_unit}", bottle_size] 
    return bottle_info

def total_wake_time(daily_goal, current_unit, user_email, goal_left  = None):
    """
    Purpose: Calculate total wake time to spread out reminders throughout day
    Parameters: daily_goal, current_unit
    Returns: None
    """
    print("==================================\n")
    print("Lets set a reminder scheduler\n")
    wakeup = input("Enter the time that you wake up (24 hour time): ")
    wakeup = clock_validator(wakeup)
    bedtime = input("Enter your sleep time (24 hour time): ")
    bedtime = clock_validator(bedtime)
    print("==================================")

    wakeup = wakeup.split(':')
    time_wakeup = dt.timedelta(hours = int(wakeup[0]), minutes = int(wakeup[1]))
    bedtime=bedtime.split(':')
    time_bedtime = dt.timedelta(hours = int(bedtime[0]), minutes = int(bedtime[1]))

    total_awake = time_bedtime - time_wakeup

    if total_awake.total_seconds()<0:   # adding extra day if sleep next day, eg. 10am - 2am where 2am is next day
        total_awake = total_awake + dt.timedelta(days=1)

    # Converting wake up duration for readability 
    total_seconds = total_awake.total_seconds()
    minutes = (total_seconds//60)
    hours = total_seconds//(3600)
    min_remainder=minutes%60
    print(f'Your total wake time is: {int(hours)} h {int(min_remainder)} m')

    if goal_left == None:   # If no goal_left (no water logged) then automatically same as the goal itself
        goal_left = daily_goal[0]

    scheduler(time_bedtime, total_awake,time_wakeup, daily_goal, current_unit, user_email, goal_left)

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
            if choice>0 and choice<=num_option:     # Ensure option chosen is a valid option number
                return str(choice)
            else:
                print("Your choice is not an option, please try again!")
                choice = input("Your number choice: ")
        except ValueError:  # If datatype is not an integer
            print("Your choice is not an option, please try again!")
            choice = input("Your number choice: ")

def clock_validator(time):
    """
    Purpose: validates 24 hour time input HH:MM
    Parameters: time 
    Returns: time (str)
    """

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
            if len(re.findall("-", time))>0 or int(hours)>24 or int(minutes)>60:    # Ensure no negative symbols at all and correct numbers - need to implement for all symbols - FUTURE ME PROBLEM :p
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
    Parameters: current_unit
    Returns: unit (str)
    """
    # Entire function can be edited to be more efficient - future me problem :p
    show_unit_menu = True
    num_option = 4
    while show_unit_menu ==True:
        print("==================================\n")
        print(f"Your current unit is: {current_unit}") # Change bottle unit look more user friendly - Future me problem :p
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
            if current_unit =='L': 
                print("You are currently in this unit, please choose a different unit!")
            else:   # when unit isn't already L
                unit = 'L'
                show_unit_menu = False
        elif unit_option =="3":
            if current_unit=="mL":
                print("You are currently in this unit, please choose a different unit!")
            else:   # when unit isn't already mL
                unit = 'mL'
                show_unit_menu = False
        elif unit_option == "4":
            unit = current_unit
            show_unit_menu = False
    return unit

def menu(daily_goal = None, current_unit = None, goal_left = None, user_email = None):
    """
    Purpose: Display main menu choices
    Parameters: daily_goal (optional), current_unit (optional)
    Returns: None
    """
    # need to fix main menu (currently looks ugly) - future me probleme :p
    if current_unit ==None:     # first time viewing menu has litres (L) default unit
        current_unit = "L"
    show_menu = True
    num_option = 4
    while show_menu ==True:
        print("==================================\n")
        print(f"Your current unit is: {current_unit}")
        print("Let's get started! Choose one of the following options: \n")
        print("1. Enter your own daily water consumption goal\n")
        print("2. I'm not sure about my goal, please calculate it for me\n")
        print("3. Change water consumption units\n")
        print("4. Terminate program\n") 
        print("==================================")
    
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
        return_menu = binary_option_validator(return_menu)  # Validate response
        if return_menu in ['yes','y']:
            show_menu = True
        elif return_menu in ['no','n']:
            show_menu = False

    if daily_goal!=None and user_email == None:
        user_email = email_setup()
        total_wake_time(daily_goal, current_unit, user_email, goal_left)

    elif daily_goal==None:
        print("\nYou must input your daily water consumption goal!\n")
        menu(daily_goal, current_unit, goal_left)
    else:   # Ensure user has entered a goal before scheduling reminders
        scheduler_settings(daily_goal, current_unit, user_email, goal_left)

if __name__ =="__main__":
    menu()


'''
Main difficulty:
Main difficulty was that I haven't coded in a while and the time constraints as I am working more in the holidays along with summer unit. Hence, I haven't implemented all my ideas including email settings to customise email heading and body messages (although written, havent tested for bugs and haven't connected functions to program)
Discovering new modules eg. schedule for notifications, thread for multithreading, datetime, smtplib, email.message. Overall I quite enjoyed learning all these modules online through tutorials and websites
Debugging was also pretty difficult due to the nature of the program, which is to have notifications at set time intervals 
Especially nested schedules which took me a long time to debug especially the removal of schedules. 

Below is my TO DO LIST for the future of this project

TO DO LIST:
1. get rid of all symbols for clock 24 hour validate ->dictionary (rn only - but need to rid all symbols)

2. Add validator for number of reminders a day

3. Maybe add calendar module (Not sure yet)

4. need to debug why its None None for object print for equivalent unit when bottle unit choice

5. need to finish commenting and remove all debugging prints

6. need to implement email notifications

7. need to reset scheduler when new day (currently just ends) IMPORTANT

8. remove all test prints (DEBUGGING STUFF)

9. daily water consumption validator cannot have negative numbers 

10. time between reminder simplify to be more user friendly H M S

11. add function to edit email message (custom message)

12. add feature where after reach water goal, notifications temp stop for the day (Maybe add)

13. if scheduler is already removed and user tries removing, have custom message saying its already removed

14. Need to connect up email settings (custom emails), therefore some email related functions not implemented yet

15. GUI scroll wheel to input volume of water drank and heat map daily streak

16. simulation of water bottle drained (holding key while drinking)

17. button to reset the email message to be default from a custom message
'''
