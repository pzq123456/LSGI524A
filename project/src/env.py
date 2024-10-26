from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TO_EMAIL_ADDRESS = os.getenv('TO_EMAIL_ADDRESS')

def get_email_address():
    return EMAIL_ADDRESS

def get_email_password():
    return EMAIL_PASSWORD

def get_to_email_address():
    return TO_EMAIL_ADDRESS

def get_all():
    return EMAIL_ADDRESS, EMAIL_PASSWORD, TO_EMAIL_ADDRESS

# print(EMAIL_ADDRESS)
# print(EMAIL_PASSWORD)
# print(TO_EMAIL_ADDRESS)