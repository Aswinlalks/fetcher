import requests
from bs4 import BeautifulSoup
from telegram import Bot
from datetime import datetime
import time

# ====== CONFIG ======
BOT_TOKEN = '7135913646:AAFvI_RsvWWAEfRkhsef9Yh0adZZgOt-D2I'
CHAT_ID = '5561323376'
USERNAME = '22ee523'
PASSWORD = 'failed@123'

bot = Bot(token=BOT_TOKEN)

def fetch_assignments():
    session = requests.Session()
    login_payload = {
        'LoginForm[username]': USERNAME,
        'LoginForm[password]': PASSWORD,
    }
    login_url = "https://mits.etlab.app/user/login"
    login_response = session.post(login_url, data=login_payload)

    if login_response.status_code == 200:
        assignments_url = "https://mits.etlab.app/student/assignments"
        assignments_response = session.get(assignments_url)
        soup = BeautifulSoup(assignments_response.content, 'html.parser')
        assignment_rows = soup.find_all('tr', class_=lambda x: x and ('odd' in x or 'even' in x))

        assignments = []
        for row in assignment_rows:
            cols = row.find_all('td')
            subject = cols[0].text.strip()
            last_date = cols[4].text.strip()
            assignments.append(f"{subject} - Due: {last_date}")
        return assignments
    else:
        return ["❌ Failed to login to Etlab"]

def send_assignment_update():
    assignments = fetch_assignments()
    message = "📚 *Assignment Updates*\n\n" + "\n".join(assignments)
    bot.send_message(chat_id=CHAT_ID, text=message, parse_mode='Markdown')

# Infinite loop - send updates every 6 hours
while True:
    send_assignment_update()
    time.sleep(6 * 60 * 60)  # 6 hours
