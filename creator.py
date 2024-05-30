from helper.ua import get_random_user_agent
from helper.util import init_steps, final_steps, generate_timesteps_string
from helper.boarding import boarding
from helper.backup import backup_data
from instagrapi import Client
from faker import Faker
from typing import TypedDict, Literal
from concurrent.futures import ThreadPoolExecutor
from helper.sms import get_activation_status, balance_inquiry, request_quantity_of_vn, request_vn, cancel_activation
from datetime import datetime
from dotenv import load_dotenv
from colorama import Fore, Style
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
REFERENCE_USERNAME = os.getenv("IG_REFERENCE_USERNAME").lower()
REFERENCE_PASSWORD = os.getenv("IG_REFERENCE_PASSWORD")
REFERENCE_FILE = f'{REFERENCE_USERNAME}_login_reference.json'
MAX_WORKERS = int(os.getenv('MAX_WORKERS'))
MAX_RETRY = int(os.getenv('MAX_RETRY'))
TIMEOUT = int(os.getenv('MAX_TIMEOUT'))
TARGET = int(os.getenv('TARGET'))

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
    folder_path = f"result/{datetime.now().strftime('%d-%m-%Y')}"
    file_path = f"{folder_path}/{file_path}"
    if not os.path.exists(os.path.join(os.path.dirname(__file__), 'result')):
        os.makedirs(os.path.join(os.path.dirname(__file__), 'result'))
    if not os.path.exists(os.path.join(os.path.dirname(__file__), folder_path)):
        os.makedirs(os.path.join(os.path.dirname(__file__), folder_path))
    if not os.path.exists(os.path.join(os.path.dirname(__file__), file_path)):
        with open(os.path.join(os.path.dirname(__file__), file_path), 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
            writer.writeheader()
            
    file_exists = os.path.exists(os.path.join(os.path.dirname(__file__), file_path))
      
    with open(os.path.join(os.path.dirname(__file__), file_path), 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='|')
        if not file_exists:
            writer.writeheader()
            if 'success' in file_path:
              backup_data(fieldnames)
        if 'success' in file_path:
          backup_data(data)
        writer.writerow(data)
        
def get_name_based_on_gender(gender):
    if gender == 'male':
        return faker.name_male()
    else:
        return faker.name_female()    

colors = [Fore.GREEN, Fore.BLUE, Fore.YELLOW, Fore.CYAN, Fore.MAGENTA]

def console(message, color=Fore.WHITE, index=0, total_account=0):
    log = f"[{time.strftime('%Y-%m-%d %H:%M:%S')} - {index}/{total_account}]"
    print(color + log + message + Style.RESET_ALL)

def create_account(account:Account, index:int, total_account:int, reference:AccountReference):
    color = colors[index % len(colors) - 1]
    step = 1
    total_step = 8
    # wait_seconds = 5
    # max_attempts = 10
    client = Client()
    client.delay_range = [2, 5]
    client.set_device(account['setting']['device_setting'])
    client.set_proxy(
      random.choice([PROXY_A, PROXY_B]) if PROXY_A and PROXY_B else PROXY
    )
    client.set_user_agent(account['setting']['user_agent'])
    console(f"{account['username']} using {account['setting']['user_agent']}", color, index, total_account)
    client.device_id = "android-%s" % hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
    email = f"{account['username']}@inboxkitten.com"
    phone_number = ""
    phone_id = ""
    status = 'failed'
    try:
      console(f"{steps(step, total_step)} Checking availablity balance and quantity for phone number...", color, index, total_account)
      sms_balance = balance_inquiry()
      
      vn_quantity = request_quantity_of_vn()
      
      while vn_quantity < MAX_WORKERS:
        try:
          vn_quantity = request_quantity_of_vn()
          if vn_quantity >= MAX_WORKERS:
            break
        except Exception as e:
          console(f"{steps(step, total_step)} {e}", color=Fore.RED, index=index, total_account=total_account)
          time.sleep(TIMEOUT)
      
      console(f"{steps(step, total_step)} Available with balance {sms_balance} and quantity {vn_quantity}", color, index, total_account)
      
      step += 1
      console(f"{steps(step, total_step)} Checking credential for {account['username']}...", color, index, total_account)
      
      client.get_signup_config()
      check = client.check_username(account['username'])
      assert check.get("available"), "Username not available"
      console(f"{steps(step, total_step)} Username available", color, index, total_account)
      
      
      # check = client.check_email(email)
      # assert check.get("valid"), f"{steps(step, total_step)} Email not valid ({check})"
      # assert check.get("available"), f"{steps(step, total_step)} Email not available ({check})"
      
      # if sms_balance < 20:
      #   raise Exception(f"Insufficient balance: {sms_balance}")
      # else:
      #   response = request_vn()
      #   phone_id = response.get('activationId')
      #   phone_number = f"+{response.get('phoneNumber')}"
      is_vn_available = False
      code = ''
      while not code:
        time.sleep(TIMEOUT)
        console(f"{steps(step, total_step)} Requesting phone number...", color, index, total_account)
        while not is_vn_available:
          try:
            response = request_vn()
            phone_id = response.get('activationId')
            phone_number = f"+{response.get('phoneNumber')}"
            is_vn_available = True
          except Exception as e:
            console(f"{steps(step, total_step)} {e}", color=Fore.RED, index=index, total_account=total_account)
            if "banned" in str(e):
              console(f"{steps(step, total_step)} Temporarily banned, waiting for timeout", color=Fore.RED, index=index, total_account=total_account)
              time.sleep(6 * TIMEOUT)
            else:
              console(f"{steps(step, total_step)} Retrying in {TIMEOUT} seconds", color=Fore.RED, index=index, total_account=total_account)
              time.sleep(TIMEOUT)
        step += 1
          
        console(f"{steps(step, total_step)} Got phone number: {phone_number} with id {phone_id}", color, index, total_account)
        retries = 0
        
        nav_chain = generate_timesteps_string(init_steps)
        while retries < MAX_RETRY:
          try:
              check = client.check_phone_number(phone_number, nav_chain)
              assert check.get("status") == "ok", "Phone number not valid"
              if check.get("status") == "ok":
                  break
          except Exception as e:
              console(f"{steps(step, total_step)} try {retries} {e}", color=Fore.RED, index=index, total_account=total_account)
              time.sleep(TIMEOUT)
          retries += 1
        step += 1
        # console(f"{steps(step, total_step)} Sending email to {email}", color, index, total_account)
        # sent = client.send_verify_email(email)
        # assert sent.get("email_sent"), f"{steps(step, total_step)} Email not sent ({sent})"
        
        console(f"{steps(step, total_step)} Send verification to {phone_number}", color, index, total_account)
        retries = 0
        while retries < MAX_RETRY:
          try:
            sent = client.send_verify_phone(phone_number, nav_chain)
            assert sent.get("status") == "ok", "Verification not sent"
            if sent.get("status") == "ok":
              break
          except Exception as e:
            console(f"{steps(step, total_step)} try {retries} {e}", color=Fore.RED, index=index, total_account=total_account)
            time.sleep(TIMEOUT)
          retries += 1
        console(f"{steps(step, total_step)} Verification sent to {phone_number}", color, index, total_account)
        
        step += 1
        time.sleep(10)
        console(f"{steps(step, total_step)} Waiting for code...", color, index, total_account)
        code = ''
        # code = get_activation_status(phone_id)
          
        try:
          code = get_activation_status(phone_id)
          if code:
            break
        except Exception as e:
          console(f"{steps(step, total_step)} timeout exceeded, cancelling activation", color=Fore.RED, index=index, total_account=total_account)
          is_vn_available = False
          if phone_id:
            console(f"{steps(step, total_step)} Cleaning up phone number {phone_number} with id {phone_id}", color, index, total_account)
            cancel_activation(phone_id, status)
            console(f"{steps(step, total_step)} Activation with id {phone_id} {'completed' if status == 'success' else 'cancelled'}", color, index, total_account)
          step = 3

      # for attempt in range(1, max_attempts):
        # try:
        #   code = get_code(email)
        #   console(f"{steps(step, total_step)} Got code: {code}, attempt {attempt}", color, index, total_account)
        # except Exception as e:
        #   console(f"{steps(step, total_step)} {e}: attempt {attempt}", color, index, total_account)
        # if code:
        #   break
        # time.sleep(wait_seconds * attempt)

      if not code:
        raise Exception(f"{steps(step, total_step)} Failed to get code")
      console(f"{steps(step, total_step)} Got code: {code}", color, index, total_account)
      
      step += 1
      console(f"{steps(step, total_step)} Verifying code...", color, index, total_account)
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
          console(f"{steps(step, total_step)} {e}", color=Fore.RED, index=index, total_account=total_account)
          time.sleep(TIMEOUT)
        retries += 1
      status = 'success'
      console(f"{steps(step, total_step)} Code verified", color, index, total_account)
      
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
          # console(f"{steps(step, total_step)} Creating account with signup code: {signup_code}", color, index, total_account)
          console(f"{steps(step, total_step)} Create account with code: {code}", color, index, total_account)
          try:
            data = client.accounts_create(**kwargs)
            if data.get("message") != "challenge_required":
                break
            if client.challenge_flow(data["challenge"]):
                kwargs.update({"suggestedUsername": "", "sn_result": "MLA"})
            if data['created_user']:
                break
          except Exception as e:
            if "feedback_required" in str(e):
                raise Exception("Feedback required, might be detected as spam")
            time.sleep(TIMEOUT)
          retries += 1
      response = data["created_user"]
      
      if "Instagram" in response['username']:
        console(f"{steps(step, total_step)} Account banned", color, index, total_account)
        write_to_csv('banned.csv', account, account.keys())
        return data
      write_to_csv('success.csv', account, account.keys())
      console(f"{steps(step, total_step)} Successfully created account for {response['username']} with id {response['pk']} and full name {response['full_name']}", color, index, total_account)
      step += 1
      client.login(account['username'], account['password'])
      console(f"{steps(step, total_step)} Boarding profile for {account['username']}", color, index, total_account)
      boarding(client, account['gender'])
      console(f"{steps(step, total_step)} Success boarding for {account['username']}", color, index, total_account)
      client.logout()
      return data
  
    except Exception as e:
      if 'created_user' in str(e):
        write_to_csv('banned.csv', account, account.keys())
      console(f"{steps(step, total_step)} Failed to create account for {account['username']} - {e}", color=Fore.RED, index=index, total_account=total_account)
    
    finally:
      if phone_id:
        console(f"{steps(step, total_step)} Cleaning up phone number {phone_number} with id {phone_id}", color, index, total_account)
        cancel_activation(phone_id, status)
        console(f"{steps(step, total_step)} Activation with id {phone_id} {'completed' if status == 'success' else 'cancelled'}", color, index, total_account)
      else:
        console(f"{steps(step, total_step)} No phone number to cancel", color, index, total_account)
  
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
    main(TARGET)