import streamlit as st
import pywhatkit
import pyautogui
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from instagrapi import Client
import datetime
import time
from twilio.rest import Client as TwilioClient

st.set_page_config(page_title="All-in-One Automation Tool", layout="centered")
st.title("🚀 Automation Dashboard (Email, WhatsApp, Instagram, SMS, Call, Text Message)")

menu = st.sidebar.selectbox("Choose an action:", (
    "Send WhatsApp Message",
    "Send Email",
    "Post to Instagram",
    "Send SMS",
    "Send Text Message",
    "Make Phone Call",
    "Exit"
))

if menu == "Send WhatsApp Message":
    st.header("📱 Send WhatsApp Message")
    phone = st.text_input("Enter phone number (with country code, e.g. +91...):")
    message = st.text_area("Enter your message:")

    now = datetime.datetime.now()
    send_hour = now.hour
    send_minute = now.minute + 2 if now.minute < 58 else now.minute + 1

    if st.button("Schedule & Send Message"):
        try:
            pywhatkit.sendwhatmsg(phone, message, send_hour, send_minute, wait_time=10)
            st.success(f"✅ Message scheduled at {send_hour}:{send_minute:02d}!")
        except Exception as e:
            st.error(f"❌ Failed to send message: {e}")

elif menu == "Send Email":
    st.header("📧 Send Email using Gmail")
    sender_email = st.text_input("Sender Email")
    app_password = st.text_input("App Password (16-char)", type="password")
    receiver_email = st.text_input("Receiver Email")
    subject = st.text_input("Email Subject")
    body = st.text_area("Email Body")

    if st.button("Send Email"):
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(sender_email, app_password)
                server.sendmail(sender_email, receiver_email, msg.as_string())

            st.success("✅ Email sent successfully!")
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")

elif menu == "Post to Instagram":
    st.header("📸 Post to Instagram")
    insta_user = st.text_input("Instagram Username")
    insta_pass = st.text_input("Instagram Password", type="password")
    photo_path = st.text_input("Path to Image File")
    caption = st.text_area("Caption for your post")

    if st.button("Post to Instagram"):
        try:
            cl = Client()
            cl.login(insta_user, insta_pass)
            cl.photo_upload(photo_path, caption)
            st.success("✅ Posted successfully to Instagram!")
        except Exception as e:
            st.error(f"❌ Failed to post: {e}")

elif menu == "Send SMS":
    st.header("📨 Send SMS using Twilio")
    account_sid = st.text_input("Twilio Account SID")
    auth_token = st.text_input("Twilio Auth Token", type="password")
    from_number = st.text_input("Twilio Phone Number (with +91)")
    to_number = st.text_input("Receiver Phone Number (with +91)")
    sms_message = st.text_area("Enter SMS message")

    if st.button("Send SMS"):
        try:
            client = TwilioClient(account_sid, auth_token)
            message = client.messages.create(
                body=sms_message,
                from_=from_number,
                to=to_number
            )
            st.success(f"✅ SMS sent! SID: {message.sid}")
        except Exception as e:
            st.error(f"❌ Failed to send SMS: {e}")

elif menu == "Send Text Message":
    st.header("💬 Send Text Message (via pywhatkit)")
    phone = st.text_input("Enter phone number (with country code, e.g. +91...):")
    message = st.text_area("Enter the text message to send:")
    hour = st.number_input("Hour (24-hr format):", min_value=0, max_value=23, step=1)
    minute = st.number_input("Minute:", min_value=0, max_value=59, step=1)

    if st.button("Send Scheduled Text"):
        try:
            pywhatkit.sendwhatmsg(phone, message, int(hour), int(minute))
            st.success("✅ Text message scheduled!")
        except Exception as e:
            st.error(f"❌ Failed to schedule message: {e}")

elif menu == "Make Phone Call":
    st.header("📞 Make a Phone Call using Twilio")
    account_sid = st.text_input("Twilio Account SID")
    auth_token = st.text_input("Twilio Auth Token", type="password")
    from_number = st.text_input("Twilio Phone Number (with +91)")
    to_number = st.text_input("Receiver Phone Number (with +91)")
    call_message = st.text_input("Message to Speak (will use Twilio's voice API)")

    if st.button("Make Call"):
        try:
            client = TwilioClient(account_sid, auth_token)
            twiml_url = f"http://twimlets.com/echo?Twiml=%3CResponse%3E%3CSay%3E{call_message}%3C%2FSay%3E%3C%2FResponse%3E"
            call = client.calls.create(
                twiml=f'<Response><Say>{call_message}</Say></Response>',
                to=to_number,
                from_=from_number
            )
            st.success(f"✅ Call initiated! Call SID: {call.sid}")
        except Exception as e:
            st.error(f"❌ Failed to make call: {e}")

else:
    st.info("Thank you for using the automation tool ✨")
