from helper.ua import get_random_user_agent
from helper.util import init_steps, final_steps, generate_timesteps_string
from helper.boarding import boarding
from instagrapi import Client
from faker import Faker
from typing import TypedDict, Literal
from concurrent.futures import ThreadPoolExecutor
from helper.sms import get_activation_status, balance_inquiry, request_quantity_of_vn, request_vn, cancel_activation
from datetime import datetime
from dotenv import load_dotenv
import hashlib
import time 
import csv
import os
import json
import random

load_dotenv()
PROXY_A = os.getenv('PROXY_A')
PROXY_B = os.getenv('PROXY_B')
PROXY = os.getenv('ROTATING_PROXY')
MAX_WORKERS = 2
MAX_RETRY = 2
TIMEOUT = 45
REFERENCE_USERNAME = os.getenv("IG_REFERENCE_USERNAME").lower()
REFERENCE_PASSWORD = os.getenv("IG_REFERENCE_PASSWORD")
REFERENCE_FILE = f'{REFERENCE_USERNAME}_login_reference.json'
NO_AVAILABLE_NUMBERS = False

class Setting(TypedDict):
    device_setting: dict
    user_agent: str
    
class Account(TypedDict):
    fullname: str
    day: str
    month: str
    year: str
    username: str
    password: str
    gender: Literal['male', 'female']
    setting: Setting
    
class AccountReference(TypedDict):
    user_id: str
    autorization: str

faker = Faker('id_ID')

def steps(step:int, total_step:int):
    return f"[{step}/{total_step}]"

def save_reference(reference):
    with open(os.path.join(os.path.dirname(__file__), REFERENCE_FILE), 'w') as f:
        json.dump(reference, f)

def load_reference():
    if os.path.exists(os.path.join(os.path.dirname(__file__), REFERENCE_FILE)):
        with open(os.path.join(os.path.dirname(__file__), REFERENCE_FILE), 'r') as f:
            return json.load(f)
    return None

def write_to_csv(file_path, data, fieldnames):
    file_path = f"result/{datetime.now().strftime('%d-%m-%Y')}-{file_path}"
    file_exists = os.path.isfile(os.path.join(os.path.dirname(__file__), file_path))
    with open(os.path.join(os.path.dirname(__file__), file_path), 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)
        
def get_name_based_on_gender(gender):
    if gender == 'male':
        return faker.name_male()
    else:
        return faker.name_female()    

def create_account(account:Account, index:int, total_account:int, reference:AccountReference):
    global NO_AVAILABLE_NUMBERS
    log = f"[{index}/{total_account}]"
    step = 1
    total_step = 9
    # wait_seconds = 5
    # max_attempts = 10
    client = Client()
    client.delay_range = [2, 5]
    client.set_device(account['setting']['device_setting'])
    client.set_proxy(
      random.choice([PROXY_A, PROXY_B]) if PROXY_A and PROXY_B else PROXY
    )
    client.set_user_agent(account['setting']['user_agent'])
    print(f"{log} {account['username']} using {account['setting']['user_agent']}")
    client.device_id = "android-%s" % hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
    email = f"{account['username']}@inboxkitten.com"
    phone_number = ""
    phone_id = ""
    status = 'failed'
    try:
      if NO_AVAILABLE_NUMBERS:
        raise Exception("Skipping account creation due to no available numbers")
      sms_balance = balance_inquiry()
      
      vn_quantity = request_quantity_of_vn()
      
      if vn_quantity < MAX_WORKERS:
        raise Exception(f"Insufficient quantity of phone number: {vn_quantity}")
      
      print(f"{log} {steps(step, total_step)} Checking phone number availability with balance {sms_balance} and quantity {vn_quantity}")
      
      
      step += 1
      print(f"{log} {steps(step, total_step)} Check credential for {account['username']}")
      
      client.get_signup_config()
      check = client.check_username(account['username'])
      assert check.get("available"), "Username not available"
      
      
      # check = client.check_email(email)
      # assert check.get("valid"), f"{log} {steps(step, total_step)} Email not valid ({check})"
      # assert check.get("available"), f"{log} {steps(step, total_step)} Email not available ({check})"
      
      
      if sms_balance < 20:
        raise Exception(f"Insufficient balance: {sms_balance}")
      else:
        response = request_vn()
        phone_id = response.get('activationId')
        phone_number = f"+{response.get('phoneNumber')}"
      step += 1
        
      print(f"{log} {steps(step, total_step)} Requested phone number: {phone_number} with id {phone_id}")
      retries = 0
      
      nav_chain = generate_timesteps_string(init_steps)
      while retries < MAX_RETRY:
        try:
            check = client.check_phone_number(phone_number, nav_chain)
            assert check.get("status") == "ok", "Phone number not valid"
            if check.get("status") == "ok":
                break
        except Exception as e:
            print(f"{log} {steps(step, total_step)} try {retries} {e}")
            time.sleep(TIMEOUT)
        retries += 1
      step += 1
      # print(f"{log} {steps(step, total_step)} Sending email to {email}")
      # sent = client.send_verify_email(email)
      # assert sent.get("email_sent"), f"{log} {steps(step, total_step)} Email not sent ({sent})"
      
      print(f"{log} {steps(step, total_step)} Sending verification to {phone_number}")
      retries = 0
      while retries < MAX_RETRY:
        try:
          sent = client.send_verify_phone(phone_number, nav_chain)
          assert sent.get("status") == "ok", "Verification not sent"
          if sent.get("status") == "ok":
            break
        except Exception as e:
          print(f"{log} {steps(step, total_step)} try {retries} {e}")
          time.sleep(TIMEOUT)
        retries += 1
      
      step += 1
      time.sleep(10)
      print(f"{log} {steps(step, total_step)} Getting code from sms")
      code = get_activation_status(phone_id)

      # for attempt in range(1, max_attempts):
        # try:
        #   code = get_code(email)
        #   print(f"{log} {steps(step, total_step)} Got code: {code}, attempt {attempt}")
        # except Exception as e:
        #   print(f"{log} {steps(step, total_step)} {e}: attempt {attempt}")
        # if code:
        #   break
        # time.sleep(wait_seconds * attempt)

      if not code:
        raise Exception(f"{log} {steps(step, total_step)} Failed to get code")
      step += 1
      print(f"{log} {steps(step, total_step)} Verifying code: {code}")
      # signup_code = client.check_confirmation_code(email, code).get("signup_code")
      
      retries = 0
      confirm_nav_chain = generate_timesteps_string(final_steps)
      full_nav_chain = f"{nav_chain},{confirm_nav_chain}"
      while retries < MAX_RETRY:
        try:
          verification_code = client.validate_confirmation_code(phone_number, code, full_nav_chain)
          assert verification_code.get("error_type") is None and verification_code.get("verified"), "Failed to verify code"
          if verification_code.get("verified"):
            break
        except Exception as e:
          print(f"{log} {steps(step, total_step)} {e}")
          time.sleep(TIMEOUT)
        retries += 1
      status = 'success'
      step += 1
      
      retries = 0
      kwargs = {
          "username": account['username'],
          "password": account['password'],
          "phone_number": phone_number,
          "verification_code": code,
          "email": email,
          "signup_code": "",
          "full_name": account['fullname'],
          "year": account['year'],
          "month": account['month'],
          "day": account['day'],
          "logged_user_id": reference['user_id'],
          "logged_user_authorization_token": reference['autorization'],
          "nav": full_nav_chain,
      }
      
      while retries < MAX_RETRY:
          # print(f"{log} {steps(step, total_step)} Creating account with signup code: {signup_code}")
          print(f"{log} {steps(step, total_step)} Creating account with verification code: {code}")
          try:
            data = client.accounts_create(**kwargs)
            if data.get("message") == "feedback_required":
                raise Exception("Feedback required, might be detected as spam")
            if data.get("message") != "challenge_required":
                break
            if client.challenge_flow(data["challenge"]):
                kwargs.update({"suggestedUsername": "", "sn_result": "MLA"})
            if data['created_user']:
                break
          except Exception as e:
            print(f"{log} {steps(step, total_step)} try {retries} {e}")
            time.sleep(TIMEOUT)
          retries += 1
      response = data["created_user"]
      
      step += 1
      if "Instagram" in response['username']:
        print(f"{log} {steps(step, total_step)} Account banned")
        write_to_csv('banned.csv', account, account.keys())
        return data
      write_to_csv('success.csv', account, account.keys())
      print(f"{log} {steps(step, total_step)} Successfully created account for {response['username']} with id {response['pk']} and full name {response['full_name']}")
      step += 1
      client.login(account['username'], account['password'])
      print(f"{log} {steps(step, total_step)} Boarding profile for {account['username']}")
      boarding(client, account['gender'])
      print(f"{log} {steps(step, total_step)} Success boarding for {account['username']}")
      client.logout()
      return data
  
    except Exception as e:
      if "No available numbers" in str(e) or "Insufficient quantity" in str(e):
        NO_AVAILABLE_NUMBERS = True
      print(f"{log} {steps(step, total_step)} Failed to create account for {account['username']} - {e}")
    
    finally:
      print(f"{log} {steps(step, total_step)} Cleaning up account {account['username']}")
      if phone_id:
        print(f"{log} {steps(step, total_step)} Cleaning up phone number {phone_number} with id {phone_id}")
        cancel_activation(phone_id, status)
        print(f"{log} {steps(step, total_step)} Activation with id {phone_id} {'cancelled' if status == 'success' else 'completed'}")

      else:
        print(f"{log} {steps(step, total_step)} No phone number to cancel")
  
def main(total):
  total_account = total
  accounts = [
    {
        'username': f'{faker.user_name().lower()}{random.randint(1, 999)}',
        'password': 'Password32!',
        'fullname': get_name_based_on_gender(gender := random.choice(['male', 'female'])),
        'day': str(random.choice(list(range(1, 28)))),
        'month': str(random.choice(list(range(1, 12)))),
        'year': str(random.choice(list(range(1990, 2001)))),
        'gender': gender,
        'setting': get_random_user_agent()
    }
    for _ in range(total_account)
  ]
  
  print("Logging in to get reference account")
  reference = load_reference()

  if reference:
          print("Using existing reference")
          client = Client()
          client.load_settings(os.path.join(os.path.dirname(__file__), f"{REFERENCE_USERNAME}_session.json"))
          client.set_device(reference['device_setting'])
          client.set_proxy(random.choice([PROXY_A, PROXY_B]))
          client.set_user_agent(reference['user_agent'])
          client.authorization_data = reference['authorization_data']
          # client.authorization = reference['authorization']
          client.login(REFERENCE_USERNAME, REFERENCE_PASSWORD)
  else:
      print("Creating a new reference")
      setting = get_random_user_agent()
      client = Client()
      client.set_device(setting['device_setting'])
      client.set_proxy(random.choice([PROXY_A, PROXY_B]))
      client.set_user_agent(setting['user_agent'])
      client.login(REFERENCE_USERNAME, REFERENCE_PASSWORD)
      client.dump_settings(f"{REFERENCE_USERNAME}_session.json")
      
      reference = {
          'device_setting': setting['device_setting'],
          'user_agent': setting['user_agent'],
          'authorization_data': client.authorization_data,
          'authorization': client.authorization
      }
      save_reference(reference)
  
  print(f"Creating {total_account} accounts with reference {client.authorization_data['ds_user_id']} {client.username}")
  
  reference = AccountReference(user_id=client.authorization_data['ds_user_id'], autorization=client.authorization)
  with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
      {executor.submit(create_account, account, index, total_account, reference): account for index, account in enumerate(accounts, start=1)}
      
if __name__ == '__main__':
    main(500)