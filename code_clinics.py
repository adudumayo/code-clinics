import datetime
import os.path
from random import randint

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from rich.console import Console
from rich.table import Table


SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

USERNAME_MAP_NAME = {
    "sngcobo123": "Mashebhebs",
    "nngidi023": "Tamia",
    "tlucia023": "Lucia",
    "adudumayo023": "Dumza",
}



def get_booker():
    
    while True:
        booker = input("Are you a Volunteer? (y/n): ").rstrip().lower()
        if booker.lower() == "y":
            return booker, True
        elif booker.lower() == "n":
            return booker, False
        print(("Invalid input! Type either y/n."))


def get_available_times(events, current_bookings):
    
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        current_bookings.append(f'{start} - {event["summary"]}')

    return current_bookings


def get_start_time(date, now=str(datetime.datetime.now())[:16]):
    
    while True:
        startTime = input("Set the start time for the meeting (hh:mm): ")
        try:
            if datetime.datetime.now().strptime(startTime, "%H:%M"):

                if f"{date} {startTime}" < str(now):
                    print(f"Start time should be later than {now[11:]}!")
                    continue
                elif startTime < "07:30" or startTime > "17:00":
                    print("Booking starting time should be between 07:30 and 17:00")
                else:
                    if int(startTime[3:]) % 30 != 0:
                        print(f"You can not make bookings at this time")
                        continue

                    return startTime

        except ValueError:
            print("Please use the correct format (hh:mm)!")
            continue


def get_end_time(startTime):
   
    hour = startTime[:2]
    mins = startTime[3:]

    if mins == "00" and hour >= "10":
        return f"{int(hour)}:30"
    elif mins == "30" and hour >= "09":
        return f"{int(hour)+1}:00"
    elif mins == "00" and hour < "10":
        return f"0{int(hour)}:30"
    elif mins == "30" and hour < "09":
        return f"0{int(hour)+1}:00"


def get_date(today=str(datetime.date.today())):
    

    while True:
        date = input("Set the date for the meeting (yyyy-mm-dd): ")
        try:
            if datetime.datetime.strptime(date, "%Y-%M-%d"):
                if date[:4].isdigit() and date[5:7].isdigit() and date[8:12].isdigit():
                    if date < today:
                        print("Can't book a session on a date that has already past!")
                        continue
                    elif date >= today:
                        return date
        except ValueError:
            print("Invalid date format! Date format ==> (yyyy-mm-dd)")
            continue


def update_personal_calendar(service, event, volunteer):
    service.events().insert(
        calendarId=f"{volunteer}@student.wethinkcode.co.za",
        body=event,
    ).execute()

def create_event(service, current_bookings, username):
    
    print("Create an event")
    summary = input("Event summary: ")
    description = input("What is the event about: ")
    location = input("Where is the location: ")
    date = get_date()
    startTime = get_start_time(date)
    endTime = get_end_time(startTime)

    booked = False
    for booking in current_bookings:
        if f"{date}T{startTime}" in booking:
            booked = True
            print("That slot has been booked")

    if not booked:
        event = {
            "summary": summary,
            "location": location,
            "description": description,
            "start": {
                "dateTime": f"{date}T{startTime}:00",
                "timeZone": "Africa/Johannesburg",
            },
            "end": {
                "dateTime": f"{date}T{endTime}:00",
                "timeZone": "Africa/Johannesburg",
            },
            "extendedProperties": {
                "private": {
                    "volunteer": f"{USERNAME_MAP_NAME[username]}",
                    "booked": "Not Taken",
                }
            },
        }

        service.events().insert(
            calendarId="c_d1e770d25ecfae4f43d2245fd96259603fc987ec3539d677aee8679b4d399158@group.calendar.google.com",
            body=event,
        ).execute()

        update_personal_calendar(service, event, username)

        print("Event created")
        return event


def get_event_results(service):
    
    now = datetime.datetime.utcnow()
    end_date = now + datetime.timedelta(days=7)
    now = now.isoformat() + "Z"
    end_date = end_date.isoformat() + "Z"

    events_result = (
        service.events()
        .list(
            calendarId="c_d1e770d25ecfae4f43d2245fd96259603fc987ec3539d677aee8679b4d399158@group.calendar.google.com",
            timeMin=now,
            timeMax=end_date,
            maxResults=None,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    return events


def get_event_list(events, events_list):
    
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        
        booked_date = start.split("T")[0]
        booked_time = (start.split("T")[1]).split("+")[0]
        volunteer = (
            event.get("extendedProperties", {})
            .get("private", {})
            .get("volunteer", "N/A")
        )
        availability = (
            event.get("extendedProperties", {}).get("private", {}).get("booked", "N/A")
        )

        if availability == "Not Taken":
            availability = "Not Taken"
        else:
            availability = "Taken"

        events_list.append(
            f'{len(events_list)+1} - {volunteer} - {event["summary"]} - {booked_date} - {booked_time} - {availability} - {event.get("id")}'
        )

        for availability in events_list:
            if availability == "Taken" and availability != "Not Taken":
                print("sorry! all slots have been booked")

    return events_list


def show_student_available_events(events, events_list,service):
    
    if not events_list:
        print("No upcoming events found.")
        return None
    
    events = get_events(service)
    

    with open("upcoming_events.txt", "w") as file:
        for event in events_list:
            file.write(str(event) + "\n")

    events_info = [data.split(" - ") for data in events_list]

    table = Table(title="Code Clinics")
    rows = [data.split(" - ")[:-1] for data in events_list]
    columns = ["Slot ID", "Volunteer Name", "Topic", "Date", "Time", "Availability"]

    for column in columns:
        table.add_column(column)

    for row in rows[:-1]:
        table.add_row(*row, style="hot_pink")

    console = Console()
    console.print(table)

    return events_info


def update_student_slot(events_info, service):
    
    while True:
        slot_id = input("Enter the Slot by ID or 0 to close the program: ")
        if slot_id.isdigit():
            if (int(slot_id)) == 0:
                print("Thank you for using our booking service. Goodbye :)")
                break
            if (
                int(slot_id) > 0 and int(slot_id) <= len(events_info)
            ) and "Not Taken" not in events_info[int(slot_id) - 1]:
                print(
                    f"slot with {''.join(events_info[int(slot_id) - 1][1]).capitalize()} on {' '.join(events_info[int(slot_id) - 1][3:5])} Already taken!"
                )
                print("Select an available slot!")
                continue
            elif (
                int(slot_id) > 0 and int(slot_id) <= len(events_info)
            ) and "Not Taken" in events_info[int(slot_id) - 1]:
                print(
                    f"You have booked slot {slot_id} with {' '.join(events_info[int(slot_id) - 1][1:4])}"
                )
                event_id = events_info[int(slot_id) - 1][6]

                event_updates = {"extendedProperties": {"private": {"booked": "Taken"}}}

                service.events().patch(calendarId="c_d1e770d25ecfae4f43d2245fd96259603fc987ec3539d677aee8679b4d399158@group.calendar.google.com",eventId=event_id,body=event_updates,).execute()
                
                break
            else:
                print("Invalid slot ID")
        else:
            print("Please enter a valid slot ID")
            continue


def code_Clinics():
    """
    Prints the WeThinkCode Code Clinics banner to the console.
    """
    header = """
     '\033[30m\033[32m    ==============================================================================     \033[0m'                                   
    ''\033[30m\033[32m    =   ####  ####  ###   ####    ####  #     #####  #     #  #####  ####  ####  =     \033[0m'' 
    ''\033[30m\033[32m    =   #     #  #  #  #  #       #     #       #    ##    #    #    #     #  #  =     \033[0m''  
    ''\033[30m\033[32m    =   #     #  #  #  #  #       #     #       #    # #   #    #    #     #     =     \033[0m''
    ''\033[30m\033[32m    =   #     WeThink_ #  ####    #     #       #    #  #  #    #    #     ####  =     \033[0m''
    ''\033[30m\033[32m    =   #     #  #  #  #  #       #     #       #    #   # #    #    #        #  =     \033[0m''
    ''\033[30m\033[32m    =   #     #  #  #  #  #       #     #       #    #    ##    #    #     #  #  =     \033[0m''
    ''\033[30m\033[32m    =   ####  ####  ###   ####    ####  ####  #####  #     #  #####  ####  ####  =     \033[0m''
     '\033[30m\033[32m    ==============================================================================     \033[0m'                                                                               
    """
    for char in header:
        if char == "#":
            print("#", end="")

        else:
            print(char, end="")
    print()


def volunteer_cancelling(service, volunteer_name, events):
    
    events = [data.split(" - ") for data in events]
    print(len(events))

    volunteer_name = USERNAME_MAP_NAME[volunteer_name]

    while True:
        slot_id = input("Enter the slot by ID that you want to delete: ")
        if int(slot_id) < 1 or int(slot_id) > len(events):
            print("Invalid slot ID")
            continue
        break
    
    event_id = events[int(slot_id) - 1][6]

    slot_owner = events[int(slot_id) - 1][1]

    if volunteer_name == slot_owner:
        service.events().delete(
            calendarId="c_d1e770d25ecfae4f43d2245fd96259603fc987ec3539d677aee8679b4d399158@group.calendar.google.com",
            eventId=event_id,
        ).execute()
        print(f"Slot cancelled successfully for {volunteer_name}.")
    else:
        print(
            f"You do not have permission to cancel this event. The event is booked by {slot_owner}."
        )

def get_volunteer_events(events,events_list):
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        booked_date = start.split("T")[0]
        booked_time = (start.split("T")[1]).split("+")[0]
        volunteer = (
            event.get("extendedProperties", {})
            .get("private", {})
            .get("volunteer", "N/A")
        )

        events_list.append(f'{len(events_list) + 1} - {volunteer} - {event["summary"]} - {booked_date} - {booked_time} - {event.get("id")}')

    return events_list

def show_volunteer_events(events, events_list):
    
    if not events:
        print("No upcoming events found.")
    else:
        table = Table(title="Current Events")
        rows = [data.split(" - ")[:-1] for data in events_list]
        columns = ["Slot ID", "Volunteer Name", "Session", "Date", "Time", "Availability"]

        for column in columns:
            table.add_column(column)

        for row in rows:
            table.add_row(*row, style="hot_pink")

        console = Console()
        console.print(table)

def get_username():
    while True:
        username = input("Enter your username or q to stop the program: ")
        if username.lower() == "q":
            quit()
        if username not in USERNAME_MAP_NAME.keys():
            print("User not authorized. Enter correct username!")
            continue
        else:
            return username
        
def get_events(service):
    
    now = datetime.datetime.utcnow()
    end_date = now + datetime.timedelta(days=7)
    now = now.isoformat() + "Z"
    end_date = end_date.isoformat() + "Z"

    events_result = (
        service.events()
       .list(
            calendarId="c_d1e770d25ecfae4f43d2245fd96259603fc987ec3539d677aee8679b4d399158@group.calendar.google.com",
            timeMin=now,
            timeMax=end_date,
            maxResults=None,
            singleEvents=True,
            orderBy="startTime",
        )
       .execute()
    )

    events = events_result.get("items", [])

    return events

MENU_VOLUNTEER =["MENU",'1. CREATE EVENT','2. DELETE EVENT','3. VIEW EVENTS','4. HELP',"5. OFF"]
MENU_STUDENT =["MENU","1. BOOK EVENT","2. CANCEL BOOKING","3. VIEW EVENTS","4. HELP","5. OFF"]

def book_student_slot(events_info, service, student_username):
    
    while True:
        slot_id = input("Enter the Slot by ID or 0 to close the program: ")
        if slot_id.isdigit():
            if int(slot_id) == 0:
                print("Thank you for using our booking service. Goodbye :)")
                break
            elif 0 < int(slot_id) <= len(events_info):
                event_info = events_info[int(slot_id) - 1]
                if "Not Taken" not in event_info:
                    print(f"Slot with {''.join(event_info[1]).capitalize()} on {' '.join(event_info[3:5])} Already taken!")
                    print("Select an available slot!")
                else:
                    print(f"You have booked slot {slot_id} with {' '.join(event_info[1:4])}")
                    event_id = event_info[6]
                    event_updates = {
                        "extendedProperties": {
                            "private": {
                                "booked": "Taken",
                                "student": f"{student_username}"
                            }
                        }
                    }
                    try:
                        service.events().patch(
                            calendarId="c_d1e770d25ecfae4f43d2245fd96259603fc987ec3539d677aee8679b4d399158@group.calendar.google.com",
                            eventId=event_id,
                            body=event_updates,
                        ).execute()
                        print("Slot booking successful!")
                        break
                    except Exception as e:
                        print("An error occurred while updating the slot:", e)
                        break
            else:
                print("Invalid slot ID")
        else:
            print("Please enter a valid slot ID")

def unbook_student_slot(events_info, service, student_username):
    
    while True:
        slot_id = input("Enter the Slot by ID or 0 to close the program: ")
        if slot_id.isdigit():
            if int(slot_id) == 0:
                print("Thank you for using our unbooking service. Goodbye :)")
                break
            elif 0 < int(slot_id) <= len(events_info):
                event_info = events_info[int(slot_id) - 1]
                if "Not Taken" in event_info:
                    print("This slot is already available.")
                    continue
                event_id = event_info[6]
                try:
                    event = service.events().get(
                        calendarId="c_d1e770d25ecfae4f43d2245fd96259603fc987ec3539d677aee8679b4d399158@group.calendar.google.com",
                        eventId=event_id
                    ).execute()
                    event_student_username = event["extendedProperties"]["private"].get("student", "")
                    if event_student_username != student_username:
                        print("You are not authorized to unbook this slot.")
                        continue
                    print(f"You have unbooked slot {slot_id} with {' '.join(event_info[1:4])}")
                    event_updates = {
                        "extendedProperties": {
                            "private": {
                                "booked": "Not Taken",
                                "student": ""
                            }
                        }
                    }
                    service.events().patch(
                        calendarId="c_d1e770d25ecfae4f43d2245fd96259603fc987ec3539d677aee8679b4d399158@group.calendar.google.com",
                        eventId=event_id,
                        body=event_updates
                    ).execute()
                    print("Slot unbooking successful!")
                    break
                except Exception as e:
                    print("An error occurred while unbooking the slot:", e)
                    break
            else:
                print("Invalid slot ID")
        else:
            print("Please enter a valid slot ID")
def get_command():
    while True:
    
        for i in MENU_VOLUNTEER:
            if i == "MENU":
                print(f"================================================================\n{' '*20}Volunteer's Menu\n================================================================")
            else:
                print(i)
        
        command = input("What do you want to do? Enter (1, 2, 3, 4, 5): ").rstrip()
        if not command.isdigit():
            print("Invalid command!")
            continue
        elif command.lower() == "q":
            break
        elif int(command)-1<0 or int(command)-1>=len(MENU_VOLUNTEER):
            print("Enter only a number that corresponds to a valid command.\n")
            continue
        else:
            command = MENU_VOLUNTEER[int(command)][3:]
            return command

def get_student_command():
    while True:
    
        for i in MENU_STUDENT:
            if i == "MENU":
                print(f"================================================================\n{' '*20}Student's Menu\n================================================================")
            else:
                print(i)
        
        command = input("What do you want to do? Enter (1, 2, 3, 4, 5): ").rstrip()
        if not command.isdigit():
            print("Invalid command!")
            continue
        elif command.lower() == "q":
            break
        elif int(command)-1<0 or int(command)-1>=len(MENU_STUDENT):
            print("Enter only a number that corresponds to a valid command.\n")
            continue
        else:
            command = MENU_STUDENT[int(command)][3:]
            return command     



