import requests
import re

API_URL = 'https://inboxkitten.com/api/v1/mail'

def get_email(email:str):
  response = requests.get(f"{API_URL}/list?recipient={email}", verify=False)
  return response.json()

def read_mail(region:str,key:str):
  response = requests.get(f"{API_URL}/getKey?region={region}&key={key}", verify=False)
  return response.json()
  

def extract_code(subject:str):
  code_pattern = r'\b(\d{6})\b'  # Pattern to match a six-digit code

  match = re.search(code_pattern, subject)

  if match:
      code = match.group(1)
      return code
  else:
      raise Exception('Code not found in the email subject')
  

def get_code(email:str):
  inbox = get_email(email)
  if(len(inbox) == 0):
    raise Exception("No email")
  
  mail = inbox[0]['storage']
  read = read_mail(region=mail['region'],key=mail['key'])
  
  code = extract_code(read['subject'])
  
  return code