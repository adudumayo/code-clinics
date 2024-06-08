from code_clinics import *
import os.path
import time

from random import randint

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError



def run_code_Clinics():


    count = 0
    code_Clinics()
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("calendar", "v3", credentials=creds)

        std_volunteer = get_booker()
        
        if std_volunteer[0] == "y":
            events = get_events(service)
            events_list = []
            events_list = get_event_list(events, events_list)
            username = get_username()

            while True:
                command = get_command()
                if command == "CREATE EVENT":
                    while True: 
                        current_bookings = []
                        current_bookings = get_available_times(events, current_bookings)

                        if count == 0:
                            events_info = show_student_available_events(events, events_list, service)
                            count += 1
                        if not events_list:
                            print("No Slots Taken\n")
                        else:
                            if count == 0:
                                events_info = show_student_available_events(events, events_list, service)
                                count += 1

                        create_event(service, current_bookings, username)
                        events = get_events(service)
                        
                        print("\nRedirecting you to the Menu\n")
                        time.sleep(0.5)
                        break
                    continue   

                elif command == "DELETE EVENT":
                    while True:
                        if not events_list:
                            print("No Slots To Delete!\n")
                            break
                        else:
                            if count == 0:
                                events_info = show_student_available_events(events, events_list, service)
                                count += 1
                        volunteer_cancelling(service, username, events_list)
                        events = get_events(service)
                        
                        print(f"Redirecting you to the Menu :)")
                        break
                        
                elif command == "VIEW EVENTS":
                    events = get_events(service)
                    events_list = []
                    events_list = get_event_list(events, events_list)
                    username = get_username()
                    
                    if count == 0:
                        events_info = show_student_available_events(events, events_list, service)
                    count += 1
                    turn_off = input("Do you want to turn off the program? (y/n): ")
                    while turn_off.lower() not in ["y","n"]:
                        print("Enter only y/n: ")
                        turn_off = input("Do you want to turn off the program? (y/n): ")
                    
                    if turn_off == "y":
                        print(f"Goodbye :), {USERNAME_MAP_NAME[username]}!")
                        quit()
                    else:
                        count = 0
                        time.sleep(0.05)
                        print("\nLoading...\n")
                        time.sleep(0.5)
                        continue           
                elif command == "HELP":
                    print("""===============================================================
select 1 to \"CREATE EVENT\": Create a new event...
select 2 to \"DELETE EVENT\": Delete event...
select 3 to \"VIEW EVENT\": View event...
select 4 to \"HELP\": For more information
select 5 to \"OFF\": Shut down...
===============================================================
""")
                    time.sleep(2)
                    continue
                elif command == "OFF":
                    time.sleep(0.05)
                    print("Shutting down",end="")
                    for i in range(3):
                        if i < 2:
                            time.sleep(0.5)
                            print(".",end="")
                            time.sleep(0.5)
                        else:
                            print(".")  
                    quit()           
        else:
            while True:
                username = get_username()
                command = get_student_command()
                events = get_event_results(service)
                events_list = []
                events_list = get_event_list(events, events_list)
                
                if command == "BOOK EVENT":
                    while True:
                        if count == 0:
                            events_info = show_student_available_events(events, events_list, service)
                        book_student_slot(events_info, service, username)
                        count += 1
                        break
                elif command == "CANCEL BOOKING":
                    while True:
                        if count == 0:
                            events_info = show_student_available_events(events, events_list, service)
                        unbook_student_slot(events_info, service, username)
                        count+=1
                        break
                elif command == "VIEW EVENTS":
                
                    if count == 0:
                        events_info = show_student_available_events(events, events_list, service)
                    count += 1
                    turn_off = input("Do you want to turn off the program? (y/n): ")
                    while turn_off.lower() not in ["y","n"]:
                        print("Enter only y/n: ")
                        turn_off = input("Do you want to turn off the program? (y/n): ")
                    
                    if turn_off == "y":
                        print(f"Goodbye :), {USERNAME_MAP_NAME[username]}!")
                        quit()
                    else:
                        time.sleep(0.05)
                        print("\nLoading...\n")
                        time.sleep(0.5)
                        count = 0
                        continue
                elif command == "HELP":

                    print("""===============================================================
select 1 to \"CREATE EVENT\": Create a new event...
select 2 to \"DELETE EVENT\": Delete event...
select 3 to \"VIEW EVENT\": View event...
select 4 to \"HELP\": For more information
select 5 to \"OFF\": Shut down...
===============================================================
""")

                    turn_off = input("Do you want to turn off the program? (y/n): ")
                    while turn_off.lower() not in ["y","n"]:
                        print("Enter only y/n: ")
                        turn_off = input("Do you want to turn off the program? (y/n): ")
                    if turn_off == "y":
                        print(f"Goodbye :), {USERNAME_MAP_NAME[username]}!")
                        quit()
                    else:
                        time.sleep(0.05)
                        print("\nLoading...\n")
                        time.sleep(0.5)
                elif command == "OFF":
                    time.sleep(0.05)
                    print("Shutting down",end="")
                    for i in range(3):
                        if i < 2:
                            time.sleep(0.5)
                            print(".",end="")
                            time.sleep(0.5)
                        else:
                            print(".")
                        quit()          

                

                
    except HttpError as error:
        print(f"An error occurred: {error}")


    

if __name__ == "__main__":
    run_code_Clinics()
    
    
