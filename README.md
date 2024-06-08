# Google Calendar Booking System

This Python script provides a booking system integrated with Google Calendar. Users can create, view, and manage events such as appointments or meetings through a simple command-line interface. The script utilizes the Google Calendar API for accessing and managing events.

## Requirements

To run this script, you need to have Python installed on your system. Additionally, you'll need to install the required Python packages listed in `requirements.txt`. You also need to have Google API credentials set up to access the Google Calendar API.

## Setup

1. Clone this repository to your local machine.

2. Install the required Python packages by running: pip install -r requirements.txt

3. Set up Google API credentials:
- Follow the instructions provided by Google to create a project and enable the Google Calendar API.
- Download the credentials file (`credentials.json`) and save it in the project directory.

## Usage

Run the script by executing `main.py`. Follow the prompts to create or manage events. There are two modes of operation:

- **Volunteer Mode**: Volunteers can view, create events or cancel their own bookings.
- **User Mode**: Users can view available events, book available slots and cancel their booked events.

### Volunteer Mode

In Volunteer Mode, volunteers can perform the following actions:

1. **Create Event**: Volunteers can create new events by providing event details such as summary, description, location, date, and time.
2. **Delete Event**: Volunteers can cancel their own bookings by selecting the slot they want to delete.
3. **View Events**: Volunteers can view available events and their details.
4. **Help**: Provides information on how to use the system.
5. **Exit**: Quit the program.

### User Mode

In User Mode, users can perform the following actions:

1. **View Available Slots**: Users can view available slots for booking.
2. **Book a Slot**: Users can book available slots for events.
3. **Delete Event**: Users can cancel their own bookings by selecting the slot they want to delete.
4. **Help**: Provides information on how to use the system.
5. **Exit**: Quit the program.

## Important Notes

- Make sure your Google Calendar API credentials are properly set up and accessible to the script.
- Ensure that the system's date and time settings are accurate for correct booking functionality.
