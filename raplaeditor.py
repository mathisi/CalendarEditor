from flask import Flask, Response
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import re
from threading import Lock

app = Flask(__name__)

calendar_url = "https://rapla.dhbw-karlsruhe.de/rapla?page=ical&user=braun&file=TINF22B2"
words_to_remove = ["AdA", "Robotik", "Workflow", "Enterprise Networking", "AI"]

edited_calendar_data = ""
lock = Lock()

def fetch_and_process_calendar():
    global edited_calendar_data
    response = requests.get(calendar_url)
    calendar_data = response.text
    events = re.findall(r'BEGIN:VEVENT(.*?)END:VEVENT', calendar_data, re.DOTALL)
    
    for event in events:
        summary_match = re.search(r'SUMMARY:(.*?)\n', event)
        if summary_match:
            summary = summary_match.group(1)
            if any(word in summary for word in words_to_remove):
                calendar_data = calendar_data.replace(f"BEGIN:VEVENT{event}END:VEVENT", "")
    
    with lock:
        edited_calendar_data = calendar_data

scheduler = BackgroundScheduler()
scheduler.add_job(fetch_and_process_calendar, 'interval', hours=12)
scheduler.start()

fetch_and_process_calendar()

@app.route('/TINF22B2', methods=['GET'])
def get_calendar():
    with lock:
        global edited_calendar_data
        return Response(iter(edited_calendar_data), mimetype='text/calendar', headers={
            'Content-Disposition': 'attachment; filename=TINF22B2.ics'
        })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9014)
