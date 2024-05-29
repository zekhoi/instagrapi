import os
import requests
import time
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('SMS_ACTIVATE_API_KEY')
SERVICE = 'ig'
COUNTRY = os.getenv("SMS_ACTIVATE_COUNTRY") # 6 Indonesia, 33 Colombia, 4 Philippines
MAX_TIMEOUT = 5 # 5 minutes

def request_quantity_of_vn():
    response = requests.get(
        f'https://api.sms-activate.org/stubs/handler_api.php?api_key={API_KEY}&action=getNumbersStatus&country={COUNTRY}'
    )
    result = response.json().get('ig_0', 0)
    return int(result)

def balance_inquiry():
    response = requests.get(
        f'https://api.sms-activate.org/stubs/handler_api.php?api_key={API_KEY}&action=getBalance'
    )
    if 'ACCESS_BALANCE:' in response.text:
        return float(response.text.replace('ACCESS_BALANCE:', ''))
    return 0

def request_vn():
    response = requests.get(
        f'https://sms-activate.org/stubs/handler_api.php?api_key={API_KEY}&action=getNumberV2&service={SERVICE}&country={COUNTRY}'
    )
    
    if "NO_NUMBERS" in response.text:
        raise ValueError('No available numbers')
    if "BANNED" in response.text:
        raise ValueError('Temporary banned from sms-activate.org')
    data = response.json()

    # NOTE: response example
    # {
    #   "activationId": 635468024,
    #   "phoneNumber": "79584******",
    #   "activationCost": "12.50",
    #   "countryCode": "0",
    #   "canGetAnotherSms": "1",
    #   "activationTime": "2022-06-01 17:30:57",
    #   "activationOperator": "mtt"
    # }
    return data

def get_activation_status(id, count=1):
    if count > MAX_TIMEOUT:
        raise ValueError('Activation status timeout')
    response = requests.get(
        f'https://api.sms-activate.org/stubs/handler_api.php?api_key={API_KEY}&action=getStatus&id={id}'
    )
    status = response.text
    print(f"Activation status: {status},  count: ({count})")
    count += 1
    if 'STATUS_WAIT' in status:
        time.sleep(60)  # every one minute
        return get_activation_status(id, count)
    elif 'STATUS_CANCEL' in status:
        raise ValueError('Activation canceled')
    elif 'STATUS_OK' in status:
        match = re.search(r'STATUS_OK:.*?(\d+)', status)
        if match:
            return match.group(1)
    else:
        raise ValueError('Unknown activation status')

def cancel_activation(id, status='failed'):
    code_status = 8 if status == 'failed' else 6
    response = requests.get(
        f'https://api.sms-activate.org/stubs/handler_api.php?api_key={API_KEY}&action=setStatus&status={code_status}&id={id}'
    )
    if 'DENIED' in response.text:
        print(f'Activation {id} cannot be canceled before 2 minutes')
        time.sleep(150)
        return cancel_activation(id)
    return response.text