from code_clinics import *

import datetime
import os.path
import time

from random import randint

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from rich.console import Console
from rich.table import Table


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
            events_list =  get_volunteer_events(events,events_list)
            username = get_username()

            while True:
                command = get_command()

                if command == "CREATE EVENT":
                    
                    while True: 
                        current_bookings = []
                        current_bookings = get_available_times(events, current_bookings)
                        if not current_bookings:
                            print("No Slots Taken\n")
                        else:
                            show_volunteer_events(events, events_list)
                        create_event(service, current_bookings, username)
                        # update_personal_calendar(service, clinics_calendar_event,username)
                        create_another_event = input("Do you want to create another event? (y/n): ")
                        if create_another_event.lower() == "n":
                            print("Goodbye :)!")
                            break
                        elif create_another_event.lower() == "y":
                            # code to check if the event is available fo booking
                            continue
                        else:
                            print("Invalid choice!! Choose (y/n)")
                        

                elif command == "DELETE EVENT":
                    while True:
                        if not events_list:
                            print("No Slots To Delete!\n")
                            break
                        else:
                            show_volunteer_events(events, events_list)
                        volunteer_cancelling(service, username, events_list)
                        delete_another_event = input("Do you want to delete another event? (y/n): ").rstrip().lower()
                        if delete_another_event == "y":
                            continue
                        elif delete_another_event == "n":
                            print("Goodbye :)!")
                            break
                        else:
                            print("Invalid choice!! Choose (y/n)")
                
                elif command == "VIEW EVENTS":
                    
                    if count == 0:
                        events_list  = get_volunteer_events(events,events_list)
                    count+=1
                    while True:
                        
                        if not events_list:
                            print("There are no events to view!\n")
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
                                break
                        else:
                            show_volunteer_events(events, events_list)
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
                                break
                elif command == "HELP":
                    print("""
===============================================================
                          
select 1 to \"CREATE EVENT\": Create a new event...
select 2 to \"DELETE EVENT\": Delete event...
select 3 to \"VIEW EVENT\": View event...
select 4 to \"HELP\": For more information
select 5 to \"OFF\": Shut down...
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
                
                if events_info == None:
                    print("No events available!\n Goodbye!")
                else:
                    if command == "BOOK EVENT":
                        while True:
                            events_info = show_student_available_events(events, events_list)
                            book_student_slot(events_info, service, username)
                            break
                    elif command == "CANCEL EVENT":
                        while True:
                            events_info = show_student_available_events(events, events_list)
                            unbook_student_slot(events_info, service, username)
                            break
                    elif command == "VIEW EVENTS":
                        event_info = show_student_available_events(events, events_list)
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
                            break
                    elif command == "HELP":
    
                        print("BOOK EVENT: Books an event...")
                        print("UNBOOK EVENT: Unbooks an event you've booked...")
                        print("VIEW EVENT: View events...")
                        print("OFF: Shut down")

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
                            break
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
    
