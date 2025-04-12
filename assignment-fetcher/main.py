import requests
from bs4 import BeautifulSoup
from telegram import Bot
from datetime import datetime

# ====== CONFIG ======
BOT_TOKEN = '7135913646:AAFvI_RsvWWAEfRkhsef9Yh0adZZgOt-D2I'
CHAT_ID = '5561323376'
USERNAME = '22ee523'
PASSWORD = 'failed@123'

# ====== FUNCTIONS ======
def fetch_assignments(username, password):
    login_url = "https://mits.etlab.app/user/login"
    session = requests.Session()

    login_payload = {
        'LoginForm[username]': username,
        'LoginForm[password]': password,
    }

    login_response = session.post(login_url, data=login_payload)

    if login_response.status_code == 200:
        assignments_url = "https://mits.etlab.app/student/assignments"
        assignments_response = session.get(assignments_url)
        soup = BeautifulSoup(assignments_response.content, 'html.parser')
        assignment_details = []

        assignment_rows = soup.find_all('tr', class_=lambda x: x and ('odd' in x or 'even' in x))
        for row in assignment_rows:
            columns = row.find_all('td')
            subject = columns[0].text.strip()
            title = columns[1].text.strip()
            last_date = columns[4].text.strip()
            assignment_details.append({'subject': subject, 'title': title, 'last_date': last_date})

        return assignment_details
    else:
        return None

def send_telegram_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    bot.send_message(chat_id=chat_id, text=message, parse_mode='Markdown')

def format_assignments(assignments):
    if not assignments:
        return "No assignments found or failed to fetch."

    msg = f"*📚 Daily Assignments - {datetime.now().strftime('%d %b %Y')}*\n\n"
    for a in assignments:
        msg += f"• *{a['subject']}* - {a['title']}\n  🗓️ Last Date: `{a['last_date']}`\n\n"
    return msg

# ====== MAIN ======
if __name__ == "__main__":
    data = fetch_assignments(USERNAME, PASSWORD)
    msg = format_assignments(data)
    send_telegram_message(BOT_TOKEN, CHAT_ID, msg)
