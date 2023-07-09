from flask import Flask, render_template, request, redirect
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

app = Flask(__name__)

# Load Google Calendar API credentials
credentials = service_account.Credentials.from_service_account_file(
    'credentials.json',
    scopes=['https://www.googleapis.com/auth/calendar']
)
service = build('calendar', 'v3', credentials=credentials)

# Set up the calendar ID for appointments
calendar_id = 'primary'  # Use 'primary' for the user's primary calendar

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/schedule', methods=['POST'])
def schedule_appointment():
    pet_name = request.form.get('pet_name')
    appointment_date = request.form.get('appointment_date')
    appointment_time = request.form.get('appointment_time')

    # Create start and end datetime objects
    start_datetime = datetime.datetime.strptime(appointment_date + ' ' + appointment_time, '%Y-%m-%d %H:%M')
    end_datetime = start_datetime + datetime.timedelta(hours=1)

    # Create event for appointment
    event = {
        'summary': f'Pet Grooming: {pet_name}',
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'YOUR_TIMEZONE'  # Replace with the desired timezone
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'YOUR_TIMEZONE'
        },
    }

    # Insert the event to the calendar
    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()

    return redirect('/success')


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    app.run(debug=True) 