import requests
from otp import settings

def send_otp(mobile, otp, user):
 """
 Send OTP via SMS.
 """
 url = f"https://2factor.in/API/V1/{settings.SMS_API_KEY}/SMS/{mobile}/{otp}/Your OTP is"
 payload = ""
 headers = {'content-type': 'application/x-www-form-urlencoded'}
 response = requests.get(url, data=payload, headers=headers)
 print(response.content)
 return bool(response.ok)