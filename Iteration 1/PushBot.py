'''
Goal(s):
- Create a useful notification bot 
    My bot will send reminders throughout the workday
'''

import requests
from datetime import datetime


#Setting time
current_time = datetime.now()

#Time values
start_work_time_start = current_time.replace(hour=7, minute=0, second=0)
start_work_time_end = current_time.replace(hour=8, minute=0, second=0)
lunch_reminder_time_start = current_time.replace(hour=10, minute=30, second=0)
lunch_reminder_time_end = current_time.replace(hour=12, minute=0, second=0)
end_work_time = current_time.replace(hour=14, minute=0, second=0)

#Initializing messages
message = ''

#Different cases
if start_work_time_start <= current_time < start_work_time_end:
    message = "Welcome to work!"

if lunch_reminder_time_start <= current_time < lunch_reminder_time_end:
    message = "Lunch is coming up at 12!"

if lunch_reminder_time_end < current_time < end_work_time:
    message = "You made it past lunch, keep going!"

if current_time >= end_work_time:
    message = "There's under an hour left in your work day. Finish strong!"

ATTUID = 'jq1226'

url = 'https://chatbots.q.att.com/service/notify/' + ATTUID + '?platform=teams'
body = 'Hello ' + ATTUID + '! This is a push message.\n' + message
headers = {'authorization': 'Basic Ym90OmFhX2NjX3JlcXVlc3RfbmV3X3NwQGNoYXRib3RzLnEuYXR0LmNvbTpNeVNlY3JldEtleQ=='}
r = requests.post(url, data=body, headers=headers, verify=False)
