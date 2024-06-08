import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from code_clinics import (
    get_start_time,
    get_end_time,
    get_date,
    create_event,
    update_personal_calendar,
    get_event_list  # Fix function name
)

class TestCalendarFunctions(unittest.TestCase):

    def test_get_volunteer_events(self):
        # Arrange
        events = []
        event_1 = {
            "start": {
                "dateTime": "2023-02-14T10:00:00+02:00"
            },
            "summary": "Event 1",
            "extendedProperties": {
                "private": {
                    "volunteer": "volunteer_1"
                }
            }
        }
        event_2 = {
            "start": {
                "dateTime": "2023-02-15T12:00:00+02:00"
            },
            "summary": "Event 2",
            "extendedProperties": {
                "private": {
                    "volunteer": "volunteer_2"
                }
            }
        }
        events.append(event_1)
        events.append(event_2)

        expected_result = [
            (1, "volunteer_1", "Event 1", "2023-02-14", "10:00", "event_id_1"),
            (2, "volunteer_2", "Event 2", "2023-02-15", "12:00", "event_id_2")
        ]

        # Act
        result = get_event_list(events)  # Fix function name

        # Assert
        self.assertEqual(result, expected_result)

        # Arrange
        events = []

        # Act
        result = get_event_list(events)  # Fix function name

        # Assert
        self.assertEqual(result, [])

    def test_get_end_time(self):
        # Test cases for get_end_time function
        self.assertEqual(get_end_time("09:00"), "09:30")
        self.assertEqual(get_end_time("10:30"), "11:00")
        self.assertEqual(get_end_time("17:00"), "17:30")

    def test_get_date(self):
        # Mock input function to provide test values
        with patch('builtins.input', side_effect=['2024-03-01', '2023-02-28', '2024-02-29']):
            # Test for valid date
            self.assertEqual(get_date(), '2024-03-01')

            # Test for past date
            self.assertEqual(get_date(), '2024-02-29')

            # Test for invalid date format
            self.assertEqual(get_date(), '2024-03-01')

    def test_create_event(self):
        # Mock Google Calendar API service
        mock_service = MagicMock()
        mock_service.events().insert.return_value.execute.return_value = {'id': 'event_id'}

        # Arrange
        current_bookings = ['2024-03-01T09:00 - Meeting']
        username = 'test_user'

        # Act
        event = create_event(mock_service, current_bookings, username)

        # Assert
        self.assertIsNotNone(event)
        self.assertEqual(event['summary'], 'Test Event')
        self.assertEqual(event['location'], 'Test Location')
        self.assertEqual(event['description'], 'Test Description')

        # Arrange
        current_bookings.append('2024-03-01T10:00 - Another Meeting')

        # Act
        event = create_event(mock_service, current_bookings, username)

        # Assert
        self.assertIsNone(event)

    def test_update_personal_calendar(self):
        # Mock Google Calendar API service
        mock_service = MagicMock()
        mock_service.events().insert.return_value.execute.return_value = {'id': 'event_id'}

        event = {'summary': 'Test Event'}

        # Test case for updating personal calendar
        update_personal_calendar(mock_service, event, 'test_user')
        mock_service.events().insert.assert_called_once_with(calendarId='test_user@student.wethinkcode.co.za', body=event)

if __name__ == '__main__':
    unittest.main()
