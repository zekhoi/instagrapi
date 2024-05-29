import time
import random

def get_current_timestamp():
    """
    Returns the current Unix timestamp with three digits after the decimal point.
    """
    current_timestamp = time.time()
    formatted_timestamp = f"{current_timestamp:.3f}"
    return float(formatted_timestamp)

def generate_timesteps_string(steps, max_interval_seconds=10):
    current_time = get_current_timestamp()
    result_string = ""

    for step in steps:
        result_string += f"{step}{current_time:.3f}::,"
        interval = random.randint(1, max_interval_seconds)
        current_time += interval
    
    return result_string.rstrip(',')

init_steps = [
    "SelfFragment:self_profile:1:cold_start:",
    "AccountSwitchFragment:account_switch_fragment:2:button:",
    "AddAccountBottomSheetFragment:add_account_bottom_sheet:3:button:",
    "CreateUsernameFragment:sac_create_username:4:warm_start:",
    "CreatePasswordFragment:sac_create_password:5:button:",
    "SACWelcomeFragment:sac_welcome_page:6:button:",
    "ContactPointTriageFragment:email_or_phone:7:button:"
]

final_steps = [
    "PhoneConfirmationFragment:phone_confirmation:9:button:",
]
