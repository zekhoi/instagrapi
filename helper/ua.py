import random

APP_VERSION = '332.0.0.37.95'
VERSION_CODE = '575345811'

android_releases = [
    '8.0.0',
    '8.1.0',
    '9.0.0',
    '10.0.0',
    '11.0.0',
    '12.0.0',
    '13.0.0',
    '14.0.0',
]
dpis = ['160dpi', '240dpi', '320dpi', '480dpi']
resolutions = ['720x1280', '1080x1920', '1440x2560', '2160x3840', '3840x2160']
locales = ['en_US', 'id_ID']

def generate_random_digits(length):
    min_value = 10**(length - 1)
    max_value = 10**length - 1
    random_digit = random.randint(min_value, max_value)
    return str(random_digit)

class DeviceSetting:
    def __init__(self, app_version, android_version, android_release, dpi, resolution, manufacturer, device, model, cpu, version_code):
        self.app_version = app_version
        self.android_version = android_version
        self.android_release = android_release
        self.dpi = dpi
        self.resolution = resolution
        self.manufacturer = manufacturer
        self.device = device
        self.model = model
        self.cpu = cpu
        self.version_code = version_code

def generate_user_agent(android_version, android_release, dpi, resolution, manufacturer, device, model, cpu, locale, version_code):
    return f"Instagram {APP_VERSION} Android ({android_version}/{android_release}; {dpi}; {resolution}; {manufacturer}; {model}; {device}; {cpu}; {locale}; {version_code})"

def get_random_element(elements):
    return random.choice(elements)

def get_random_user_agent():
    device = get_random_element(DEVICES)
    android_release = get_random_element(android_releases)
    dpi = get_random_element(dpis)
    resolution = get_random_element(resolutions)
    locale = get_random_element(locales)
    device_setting = DeviceSetting(
        app_version=APP_VERSION,
        android_version=device['androidVersion'],
        android_release=android_release,
        dpi=dpi,
        resolution=resolution,
        manufacturer=device['manufacturer'],
        device=device['device'],
        model=device['model'],
        cpu=device['cpu'],
        version_code=VERSION_CODE
    )
    user_agent = generate_user_agent(
        device_setting.android_version,
        device_setting.android_release,
        device_setting.dpi,
        device_setting.resolution,
        device_setting.manufacturer,
        device_setting.device,
        device_setting.model,
        device_setting.cpu,
        locale,
        device_setting.version_code
    )

    return {
        'user_agent': user_agent,
        'device_setting': vars(device_setting)
    }
    
DEVICES = [
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-J530FM",
    "device": "j5y17lte",
    "cpu": "samsungexynos7870"
  },
  {
    "androidVersion": 22,
    "manufacturer": "Meizu",
    "model": "M3s",
    "device": "M3s",
    "cpu": "mt6755"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-G925F",
    "device": "zerolte",
    "cpu": "samsungexynos7420"
  },
  {
    "androidVersion": 23,
    "manufacturer": "HUAWEI",
    "model": "EVA-L09",
    "device": "HWEVA",
    "cpu": "hi3650"
  },
  {
    "androidVersion": 26,
    "manufacturer": "samsung",
    "model": "SM-G950F",
    "device": "dreamlte",
    "cpu": "samsungexynos8895"
  },
  {
    "androidVersion": 23,
    "manufacturer": "samsung",
    "model": "SM-J500H",
    "device": "j53g",
    "cpu": "qcom"
  },
  {
    "androidVersion": 22,
    "manufacturer": "Meizu",
    "model": "m3 note",
    "device": "m3note",
    "cpu": "mt6755"
  },
  {
    "androidVersion": 22,
    "manufacturer": "samsung",
    "model": "SM-T331",
    "device": "millet3g",
    "cpu": "qcom"
  },
  {
    "androidVersion": 24,
    "manufacturer": "LENOVO/Lenovo",
    "model": "Lenovo P2a42",
    "device": "P2a42",
    "cpu": "qcom"
  },
  {
    "androidVersion": 19,
    "manufacturer": "Lenovo",
    "model": "Lenovo S660",
    "device": "S660",
    "cpu": "mt6582"
  },
  {
    "androidVersion": 23,
    "manufacturer": "Meizu",
    "model": "MX6",
    "device": "MX6",
    "cpu": "mt6797"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-A520F",
    "device": "a5y17lte",
    "cpu": "samsungexynos7880"
  },
  {
    "androidVersion": 19,
    "manufacturer": "Sony",
    "model": "E2115",
    "device": "E2115",
    "cpu": "mt6582"
  },
  {
    "androidVersion": 22,
    "manufacturer": "HUAWEI",
    "model": "HUAWEI TIT-U02",
    "device": "HWTIT-U6582",
    "cpu": "mt6582"
  },
  {
    "androidVersion": 26,
    "manufacturer": "samsung",
    "model": "SM-G950F",
    "device": "dreamlte",
    "cpu": "samsungexynos8895"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-C7000",
    "device": "c7ltechn",
    "cpu": "qcom"
  },
  {
    "androidVersion": 24,
    "manufacturer": "HUAWEI",
    "model": "SLA-L22",
    "device": "HWSLA-Q",
    "cpu": "qcom"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-A520F",
    "device": "a5y17lte",
    "cpu": "samsungexynos7880"
  },
  {
    "androidVersion": 21,
    "manufacturer": "samsung",
    "model": "GT-I9500",
    "device": "ja3g",
    "cpu": "universal5410"
  },
  {
    "androidVersion": 26,
    "manufacturer": "HTC/htc",
    "model": "HTC U11",
    "device": "htc_ocndugl",
    "cpu": "htc_ocn"
  },
  {
    "androidVersion": 25,
    "manufacturer": "Xiaomi",
    "model": "Redmi 4A",
    "device": "rolex",
    "cpu": "qcom"
  },
  {
    "androidVersion": 23,
    "manufacturer": "Meizu",
    "model": "U10",
    "device": "U10",
    "cpu": "mt6755"
  },
  {
    "androidVersion": 17,
    "manufacturer": "Lenovo",
    "model": "Lenovo S660",
    "device": "S660",
    "cpu": "mt6582"
  },
  {
    "androidVersion": 16,
    "manufacturer": "LENOVO/Lenovo",
    "model": "Lenovo A706_ROW",
    "device": "armani_row",
    "cpu": "qcom"
  },
  {
    "androidVersion": 23,
    "manufacturer": "LENOVO/Lenovo",
    "model": "Lenovo A7010a48",
    "device": "A7010a48",
    "cpu": "mt6735"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-A510F",
    "device": "a5xelte",
    "cpu": "samsungexynos7580"
  },
  {
    "androidVersion": 25,
    "manufacturer": "Xiaomi/xiaomi",
    "model": "Redmi 5 Plus",
    "device": "vince",
    "cpu": "qcom"
  },
  {
    "androidVersion": 22,
    "manufacturer": "samsung",
    "model": "SM-J320H",
    "device": "j3x3g",
    "cpu": "sc8830"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-G920F",
    "device": "zeroflte",
    "cpu": "samsungexynos7420"
  },
  {
    "androidVersion": 25,
    "manufacturer": "Xiaomi",
    "model": "Redmi 5A",
    "device": "riva",
    "cpu": "qcom"
  },
  {
    "androidVersion": 22,
    "manufacturer": "Meizu",
    "model": "m2",
    "device": "m2",
    "cpu": "mt6735"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-J730FM",
    "device": "j7y17lte",
    "cpu": "samsungexynos7870"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-G935F",
    "device": "hero2lte",
    "cpu": "samsungexynos8890"
  },
  {
    "androidVersion": 22,
    "manufacturer": "Meizu",
    "model": "m2",
    "device": "m2",
    "cpu": "mt6735"
  },
  {
    "androidVersion": 22,
    "manufacturer": "samsung",
    "model": "SM-J5108",
    "device": "j5xltecmcc",
    "cpu": "qcom"
  },
  {
    "androidVersion": 23,
    "manufacturer": "samsung",
    "model": "SM-A700FD",
    "device": "a7lte",
    "cpu": "qcom"
  },
  {
    "androidVersion": 22,
    "manufacturer": "LENOVO/Lenovo",
    "model": "Lenovo A6020a40",
    "device": "A6020a40",
    "cpu": "qcom"
  },
  {
    "androidVersion": 22,
    "manufacturer": "Meizu",
    "model": "MX4",
    "device": "mx4",
    "cpu": "mt6595"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-J710F",
    "device": "j7xelte",
    "cpu": "samsungexynos7870"
  },
  {
    "androidVersion": 23,
    "manufacturer": "Meizu",
    "model": "M5s",
    "device": "M5s",
    "cpu": "mt6735"
  },
  {
    "androidVersion": 22,
    "manufacturer": "HUAWEI",
    "model": "HUAWEI TIT-U02",
    "device": "HWTIT-U6582",
    "cpu": "mt6582"
  },
  {
    "androidVersion": 21,
    "manufacturer": "ZTE",
    "model": "ZTE BLADE A5 PRO",
    "device": "P731A20",
    "cpu": "sc8830"
  },
  {
    "androidVersion": 22,
    "manufacturer": "Meizu",
    "model": "m2",
    "device": "m2",
    "cpu": "mt6735"
  },
  {
    "androidVersion": 22,
    "manufacturer": "samsung",
    "model": "SM-J320H",
    "device": "j3x3g",
    "cpu": "sc8830"
  },
  {
    "androidVersion": 23,
    "manufacturer": "Sony",
    "model": "E5633",
    "device": "E5633",
    "cpu": "mt6795"
  },
  {
    "androidVersion": 21,
    "manufacturer": "samsung",
    "model": "SM-G530H",
    "device": "fortunave3g",
    "cpu": "qcom"
  },
  {
    "androidVersion": 19,
    "manufacturer": "Xiaomi",
    "model": "HM 1S",
    "device": "armani",
    "cpu": "qcom"
  },
  {
    "androidVersion": 23,
    "manufacturer": "Meizu",
    "model": "U20",
    "device": "U20",
    "cpu": "mt6755"
  },
  {
    "androidVersion": 25,
    "manufacturer": "Xiaomi/xiaomi",
    "model": "Redmi 5 Plus",
    "device": "vince",
    "cpu": "qcom"
  },
  {
    "androidVersion": 21,
    "manufacturer": "Sony",
    "model": "E2303",
    "device": "E2303",
    "cpu": "qcom"
  },
  {
    "androidVersion": 26,
    "manufacturer": "samsung",
    "model": "SM-G950F",
    "device": "dreamlte",
    "cpu": "samsungexynos8895"
  },
  {
    "androidVersion": 22,
    "manufacturer": "Xiaomi",
    "model": "Redmi Note 3",
    "device": "kenzo",
    "cpu": "qcom"
  },
  {
    "androidVersion": 22,
    "manufacturer": "CUBOT",
    "model": "CUBOT_NOTE_S",
    "device": "CUBOT_NOTE_S",
    "cpu": "mt6580"
  },
  {
    "androidVersion": 26,
    "manufacturer": "HUAWEI/HONOR",
    "model": "STF-L09",
    "device": "HWSTF",
    "cpu": "hi3660"
  },
  {
    "androidVersion": 23,
    "manufacturer": "myPhone",
    "model": "HAMMER_ENERGY",
    "device": "HAMMER_ENERGY_PLAY",
    "cpu": "mt6735"
  },
  {
    "androidVersion": 26,
    "manufacturer": "samsung",
    "model": "SM-G955F",
    "device": "dream2lte",
    "cpu": "samsungexynos8895"
  },
  {
    "androidVersion": 24,
    "manufacturer": "HUAWEI",
    "model": "EVA-L09",
    "device": "HWEVA",
    "cpu": "hi3650"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-J701F",
    "device": "j7velte",
    "cpu": "samsungexynos7870"
  },
  {
    "androidVersion": 23,
    "manufacturer": "samsung",
    "model": "SM-G903F",
    "device": "s5neolte",
    "cpu": "samsungexynos7580"
  },
  {
    "androidVersion": 23,
    "manufacturer": "Meizu",
    "model": "M5 Note",
    "device": "M5Note",
    "cpu": "mt6755"
  },
  {
    "androidVersion": 26,
    "manufacturer": "samsung",
    "model": "SM-G950F",
    "device": "dreamlte",
    "cpu": "samsungexynos8895"
  },
  {
    "androidVersion": 21,
    "manufacturer": "samsung",
    "model": "GT-I9515",
    "device": "jfvelte",
    "cpu": "qcom"
  },
  {
    "androidVersion": 16,
    "manufacturer": "HTC/htc",
    "model": "HTC Desire 600 dual sim",
    "device": "cp3dug",
    "cpu": "cp3dug"
  },
  {
    "androidVersion": 22,
    "manufacturer": "Meizu",
    "model": "m2 note",
    "device": "m2note",
    "cpu": "mt6735"
  },
  {
    "androidVersion": 25,
    "manufacturer": "Xiaomi",
    "model": "Redmi 4X",
    "device": "santoni",
    "cpu": "qcom"
  },
  {
    "androidVersion": 22,
    "manufacturer": "Meizu",
    "model": "m2 note",
    "device": "m2note",
    "cpu": "mt6735"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-A710F",
    "device": "a7xelte",
    "cpu": "samsungexynos7580"
  },
  {
    "androidVersion": 23,
    "manufacturer": "Meizu",
    "model": "U10",
    "device": "U10",
    "cpu": "mt6755"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-A710F",
    "device": "a7xelte",
    "cpu": "samsungexynos7580"
  },
  {
    "androidVersion": 23,
    "manufacturer": "Meizu",
    "model": "PRO 6",
    "device": "PRO6",
    "cpu": "mt6797"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-G920F",
    "device": "zeroflte",
    "cpu": "samsungexynos7420"
  },
  {
    "androidVersion": 25,
    "manufacturer": "samsung",
    "model": "SM-A730F",
    "device": "jackpot2lte",
    "cpu": "samsungexynos7885"
  },
  {
    "androidVersion": 23,
    "manufacturer": "Sony",
    "model": "E5633",
    "device": "E5633",
    "cpu": "mt6795"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-G935F",
    "device": "hero2lte",
    "cpu": "samsungexynos8890"
  },
  {
    "androidVersion": 25,
    "manufacturer": "Xiaomi",
    "model": "Redmi 4A",
    "device": "rolex",
    "cpu": "qcom"
  },
  {
    "androidVersion": 25,
    "manufacturer": "Xiaomi",
    "model": "Redmi 4X",
    "device": "santoni",
    "cpu": "qcom"
  },
  {
    "androidVersion": 22,
    "manufacturer": "Meizu",
    "model": "M3s",
    "device": "M3s",
    "cpu": "mt6755"
  },
  {
    "androidVersion": 21,
    "manufacturer": "samsung",
    "model": "SM-G530H",
    "device": "fortuna3g",
    "cpu": "qcom"
  },
  {
    "androidVersion": 23,
    "manufacturer": "Meizu",
    "model": "M5 Note",
    "device": "M5Note",
    "cpu": "mt6755"
  },
  {
    "androidVersion": 22,
    "manufacturer": "Sony",
    "model": "D2302",
    "device": "D2302",
    "cpu": "qcom"
  },
  {
    "androidVersion": 26,
    "manufacturer": "samsung",
    "model": "SM-G955F",
    "device": "dream2lte",
    "cpu": "samsungexynos8895"
  },
  {
    "androidVersion": 26,
    "manufacturer": "OnePlus",
    "model": "ONEPLUS A3010",
    "device": "OnePlus3T",
    "cpu": "qcom"
  },
  {
    "androidVersion": 22,
    "manufacturer": "samsung",
    "model": "SM-J120H",
    "device": "j1x3g",
    "cpu": "sc8830"
  },
  {
    "androidVersion": 23,
    "manufacturer": "Meizu",
    "model": "M5s",
    "device": "M5s",
    "cpu": "mt6735"
  },
  {
    "androidVersion": 25,
    "manufacturer": "samsung",
    "model": "SM-A530F",
    "device": "jackpotlte",
    "cpu": "samsungexynos7885"
  },
  {
    "androidVersion": 26,
    "manufacturer": "samsung",
    "model": "SM-A520F",
    "device": "a5y17lte",
    "cpu": "samsungexynos7880"
  },
  {
    "androidVersion": 22,
    "manufacturer": "samsung",
    "model": "SM-J200H",
    "device": "j23g",
    "cpu": "sc8830"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-A320F",
    "device": "a3y17lte",
    "cpu": "samsungexynos7870"
  },
  {
    "androidVersion": 21,
    "manufacturer": "samsung",
    "model": "SAMSUNG-SGH-I537",
    "device": "jactivelteatt",
    "cpu": "qcom"
  },
  {
    "androidVersion": 26,
    "manufacturer": "samsung",
    "model": "SM-N950F",
    "device": "greatlte",
    "cpu": "samsungexynos8895"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-A310F",
    "device": "a3xelte",
    "cpu": "samsungexynos7580"
  },
  {
    "androidVersion": 19,
    "manufacturer": "samsung",
    "model": "SM-G360H",
    "device": "core33g",
    "cpu": "sc8830"
  },
  {
    "androidVersion": 24,
    "manufacturer": "samsung",
    "model": "SM-A310F",
    "device": "a3xelte",
    "cpu": "samsungexynos7580"
  },
  {
    "androidVersion": 22,
    "manufacturer": "Meizu",
    "model": "m3 note",
    "device": "m3note",
    "cpu": "mt6755"
  },
  {
    "androidVersion": 25,
    "manufacturer": "Xiaomi",
    "model": "Redmi 4X",
    "device": "santoni",
    "cpu": "qcom"
  },
  {
    "androidVersion": 26,
    "manufacturer": "samsung",
    "model": "SM-G950F",
    "device": "dreamlte",
    "cpu": "samsungexynos8895"
  }
]