from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.message import EmailMessage
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/contact")
def contact(name: str = Form(...), email: str = Form(...), message: str = Form(...)):
    msg = EmailMessage()
    msg["Subject"] = f"New message from {name}"
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg.set_content(f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return {"success": True, "message": "Message sent successfully."}
    except Exception as e:
        print("SMTP ERROR:", e)
        return {"success": False, "message": "Failed to send message."}
