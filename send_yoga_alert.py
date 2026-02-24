import os
from dotenv import load_dotenv
from openai import OpenAI
from twilio.rest import Client
from datetime import datetime

# Load environment variables
load_dotenv()

# OpenAI setup
client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Twilio setup
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_client = Client(account_sid, auth_token)

from_whatsapp = os.getenv("TWILIO_WHATSAPP_FROM")
to_whatsapp = os.getenv("YOUR_WHATSAPP")

# Generate yoga plan
today = datetime.now().strftime("%A")

prompt = f"""
You are a disciplined AI coach.
Generate a 20-minute structured yoga plan for {today} morning.
Keep it practical and motivating.
Format:
- Warmup (5 min)
- Main Flow (10 min)
- Breathing (5 min)
Keep it concise.
"""

response = client_ai.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

yoga_plan = response.choices[0].message.content

# Send WhatsApp message
message = twilio_client.messages.create(
    body=f"🌅 Good Morning Manidhar!\n\nHere is your Yoga Plan:\n\n{yoga_plan}",
    from_=from_whatsapp,
    to=to_whatsapp
)

print("✅ Yoga alert sent successfully!")
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        