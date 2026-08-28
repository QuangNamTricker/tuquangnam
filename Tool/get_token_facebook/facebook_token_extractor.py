#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
╔══════════════════════════════════════════════════════════════════╗
║     FACEBOOK TOKEN & COOKIE EXTRACTOR PRO v1.0.0               ║
║     Author: Từ Quang Nam                                       ║
║     Facebook: fb.com/tuquangnam07                              ║
║     Zalo: 0888385536                                          ║
╚══════════════════════════════════════════════════════════════════╝
"""

import random
import string
import json
import time
import requests
import uuid
import pyotp
import base64
import io
import struct
import sys
import os
import threading
import concurrent.futures
from datetime import datetime
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

# Thư viện màu sắc
try:
    from colorama import Fore, Back, Style, init
    init(autoreset=True)
except ImportError:
    class Fore:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
        LIGHTBLACK_EX = LIGHTRED_EX = LIGHTGREEN_EX = LIGHTYELLOW_EX = ""
        LIGHTBLUE_EX = LIGHTMAGENTA_EX = LIGHTCYAN_EX = LIGHTWHITE_EX = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""
    class Back:
        BLACK = RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""

# --- CẤU HÌNH TOÀN CỤ ---
VERSION = "1.0.0"
AUTHOR = "Từ Quang Nam"
FACEBOOK_URL = "fb.com/tuquangnam07"
ZALO = "0888385536"
OUTPUT_FILE = "tokens_and_cookies.txt"

# --- KHÓA CHO ĐA LUỒNG ---
file_lock = threading.Lock()
print_lock = threading.Lock()

# ===================================================================
# PHẦN 1: MÃ HÓA MẬT KHẨU FACEBOOK
# ===================================================================

class FacebookPasswordEncryptor:
    """Mã hóa mật khẩu Facebook theo định dạng #PWD_FB4A"""
    
    @staticmethod
    def get_public_key():
        """Lấy public key từ Facebook"""
        try:
            url = 'https://b-graph.facebook.com/pwd_key_fetch'
            params = {
                'version': '2',
                'flow': 'CONTROLLER_INITIALIZATION',
                'method': 'GET',
                'fb_api_req_friendly_name': 'pwdKeyFetch',
                'fb_api_caller_class': 'com.facebook.auth.login.AuthOperations',
                'access_token': '438142079694454|fc0a7caa49b192f64f6f5a6d9643bb28'
            }
            response = requests.post(url, params=params, timeout=10).json()
            return response.get('public_key'), str(response.get('key_id', '25'))
        except Exception as e:
            raise Exception(f"Không thể lấy public key: {e}")

    @staticmethod
    def encrypt(password, public_key=None, key_id="25"):
        """Mã hóa mật khẩu"""
        if public_key is None:
            public_key, key_id = FacebookPasswordEncryptor.get_public_key()

        try:
            rand_key = get_random_bytes(32)
            iv = get_random_bytes(12)
            
            pubkey = RSA.import_key(public_key)
            cipher_rsa = PKCS1_v1_5.new(pubkey)
            encrypted_rand_key = cipher_rsa.encrypt(rand_key)
            
            cipher_aes = AES.new(rand_key, AES.MODE_GCM, nonce=iv)
            current_time = int(time.time())
            cipher_aes.update(str(current_time).encode("utf-8"))
            encrypted_passwd, auth_tag = cipher_aes.encrypt_and_digest(password.encode("utf-8"))
            
            buf = io.BytesIO()
            buf.write(bytes([1, int(key_id)]))
            buf.write(iv)
            buf.write(struct.pack("<h", len(encrypted_rand_key)))
            buf.write(encrypted_rand_key)
            buf.write(auth_tag)
            buf.write(encrypted_passwd)
            
            encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
            return f"#PWD_FB4A:2:{current_time}:{encoded}"
        except Exception as e:
            raise Exception(f"Lỗi khi mã hóa mật khẩu: {e}")

# ===================================================================
# PHẦN 2: DANH SÁCH ỨNG DỤNG FACEBOOK
# ===================================================================

class FacebookAppTokens:
    """Quản lý danh sách ứng dụng Facebook và token tương ứng"""
    
    APPS = {
        'FB_ANDROID': {
            'name': 'Facebook For Android',
            'app_id': '350685531728',
            'prefix': 'EAAAAU',
            'platform': 'Android'
        },
        'MESSENGER_ANDROID': {
            'name': 'Messenger For Android',
            'app_id': '256002347743983',
            'prefix': 'EAADo1',
            'platform': 'Android'
        },
        'FB_LITE': {
            'name': 'Facebook Lite',
            'app_id': '275254692598279',
            'prefix': 'EAAD6V7',
            'platform': 'Android'
        },
        'MESSENGER_LITE': {
            'name': 'Messenger Lite',
            'app_id': '200424423651082',
            'prefix': 'EAAC2S',
            'platform': 'Android'
        },
        'ADS_MANAGER_ANDROID': {
            'name': 'Ads Manager Android',
            'app_id': '438142079694454',
            'prefix': 'EAAGOf',
            'platform': 'Android'
        },
        'PAGES_MANAGER_ANDROID': {
            'name': 'Pages Manager Android',
            'app_id': '121876164619130',
            'prefix': 'EAABu2',
            'platform': 'Android'
        },
        'FB_IPHONE': {
            'name': 'Facebook For iPhone',
            'app_id': '6628568379',
            'prefix': 'EAAAAA',
            'platform': 'iOS'
        },
        'MESSENGER_IPHONE': {
            'name': 'Messenger For iPhone',
            'app_id': '237759909591655',
            'prefix': 'EAADYP',
            'platform': 'iOS'
        },
        'ADS_MANAGER_IOS': {
            'name': 'Ads Manager iOS',
            'app_id': '1479723375646806',
            'prefix': 'EAAVBz',
            'platform': 'iOS'
        },
        'PAGES_MANAGER_IOS': {
            'name': 'Pages Manager iOS',
            'app_id': '165907476854626',
            'prefix': 'EAACW5',
            'platform': 'iOS'
        },
        'MESSENGER_IPHONE_DEV': {
            'name': 'Messenger iPhone Dev',
            'app_id': '202805033077166',
            'prefix': 'EAAC4c',
            'platform': 'iOS'
        },
        'MESSENGER_KIDS_IOS': {
            'name': 'Messenger Kids iOS',
            'app_id': '522404077880990',
            'prefix': 'EAAHbH',
            'platform': 'iOS'
        },
        'MESSENGER_IOS_IN_HOUSE': {
            'name': 'Messenger iOS In-House',
            'app_id': '184182168294603',
            'prefix': 'EAACng',
            'platform': 'iOS'
        },
        'FB_IPAD': {
            'name': 'Facebook For iPad',
            'app_id': '124024574287414',
            'prefix': 'EAACeH',
            'platform': 'iOS'
        },
        'PAGES_MANAGER_WINDOWS': {
            'name': 'Pages Manager Windows',
            'app_id': '1174099472704185',
            'prefix': 'EAAQr1',
            'platform': 'Windows'
        },
        'BUSINESS_MANAGER': {
            'name': 'Business Manager',
            'app_id': '436761779744620',
            'prefix': 'EAAGNO',
            'platform': 'Web'
        }
    }
    
    @staticmethod
    def get_all_app_keys():
        """Lấy danh sách tất cả app keys"""
        return list(FacebookAppTokens.APPS.keys())
    
    @staticmethod
    def get_app_id(app_key):
        """Lấy app_id theo key"""
        app = FacebookAppTokens.APPS.get(app_key)
        return app['app_id'] if app else None
    
    @staticmethod
    def get_app_info(app_key):
        """Lấy thông tin đầy đủ của app"""
        return FacebookAppTokens.APPS.get(app_key)
    
    @staticmethod
    def get_prefix_hint(app_key):
        """Lấy prefix gợi ý"""
        app = FacebookAppTokens.APPS.get(app_key)
        return app['prefix'] if app else "UNKNOWN"
    
    @staticmethod
    def extract_token_prefix(token):
        """Trích xuất prefix từ token"""
        if not token:
            return "UNKNOWN"
        for i, char in enumerate(token):
            if char.islower():
                return token[:i]
        return token[:10] if len(token) > 10 else token

# ===================================================================
# PHẦN 3: ĐĂNG NHẬP FACEBOOK
# ===================================================================

class FacebookLogin:
    """Xử lý đăng nhập Facebook và lấy token/cookies"""
    
    API_URL = "https://b-graph.facebook.com/auth/login"
    ACCESS_TOKEN = "350685531728|62f8ce9f74b12f84c123cc23437a4a32"
    API_KEY = "882a8490361da98702bf97a021ddc14d"
    SIG = "214049b9f17c38bd767de53752b53946"
    
    BASE_HEADERS = {
        "content-type": "application/x-www-form-urlencoded",
        "x-fb-net-hni": "45201",
        "zero-rated": "0",
        "x-fb-sim-hni": "45201",
        "x-fb-connection-quality": "EXCELLENT",
        "x-fb-friendly-name": "authenticate",
        "x-fb-connection-bandwidth": "78032897",
        "x-tigon-is-retry": "False",
        "authorization": "OAuth null",
        "x-fb-connection-type": "WIFI",
        "x-fb-device-group": "3342",
        "priority": "u=3,i",
        "x-fb-http-engine": "Liger",
        "x-fb-client-ip": "True",
        "x-fb-server-cluster": "True"
    }
    
    def __init__(self, uid_phone_mail, password, twwwoo2fa="", machine_id=None, 
                 convert_all_tokens=True, show_progress=True):
        """
        Khởi tạo đăng nhập
        
        Args:
            uid_phone_mail: Email, số điện thoại hoặc UID Facebook
            password: Mật khẩu (plain text hoặc đã mã hóa)
            twwwoo2fa: Mã bí mật 2FA (nếu có)
            machine_id: Machine ID từ cookie datr
            convert_all_tokens: Chuyển đổi sang tất cả app
            show_progress: Hiển thị tiến trình
        """
        self.uid_phone_mail = uid_phone_mail
        self.twwwoo2fa = twwwoo2fa.replace(" ", "") if twwwoo2fa else ""
        self.show_progress = show_progress
        
        # Mã hóa mật khẩu nếu cần
        if password.startswith("#PWD_FB4A"):
            self.password = password
        else:
            self.password = FacebookPasswordEncryptor.encrypt(password)
        
        # Cấu hình chuyển đổi token
        if convert_all_tokens:
            self.convert_token_to = FacebookAppTokens.get_all_app_keys()
        else:
            self.convert_token_to = []
        
        # Tạo session
        self.session = requests.Session()
        
        # Tạo các ID ngẫu nhiên
        self.device_id = str(uuid.uuid4())
        self.adid = str(uuid.uuid4())
        self.secure_family_device_id = str(uuid.uuid4())
        self.machine_id = machine_id if machine_id else self._generate_machine_id()
        self.jazoest = ''.join(random.choices(string.digits, k=5))
        self.sim_serial = ''.join(random.choices(string.digits, k=20))
        
        # Xây dựng headers và data
        self.headers = self._build_headers()
        self.data = self._build_data()
        
        # Kết quả
        self.result = None
    
    @staticmethod
    def _generate_machine_id():
        """Tạo machine_id ngẫu nhiên"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    
    def _build_headers(self):
        """Xây dựng headers giả lập Android"""
        headers = self.BASE_HEADERS.copy()
        headers.update({
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"350685531728","retry_attempt":"0"},"application_tags":"unknown"}',
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23113RKC6C Build/PQ3A.190705.08211809) [FBAN/FB4A;FBAV/417.0.0.33.65;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/480086274;FBCR/MobiFone;FBMF/Redmi;FBBD/Redmi;FBDV/23113RKC6C;FBSV/9;FBCA/x86:armeabi-v7a;FBDM/{density=1.5,width=1280,height=720};FB_FW/1;FBRV/0;]"
        })
        return headers
    
    def _build_data(self):
        """Xây dựng data gửi lên server"""
        base_data = {
            "format": "json",
            "email": self.uid_phone_mail,
            "password": self.password,
            "credentials_type": "password",
            "generate_session_cookies": "1",
            "locale": "vi_VN",
            "client_country_code": "VN",
            "api_key": self.API_KEY,
            "access_token": self.ACCESS_TOKEN,
            "adid": self.adid,
            "device_id": self.device_id,
            "generate_analytics_claim": "1",
            "community_id": "",
            "linked_guest_account_userid": "",
            "cpl": "true",
            "try_num": "1",
            "family_device_id": self.device_id,
            "secure_family_device_id": self.secure_family_device_id,
            "sim_serials": f'["{self.sim_serial}"]',
            "openid_flow": "android_login",
            "openid_provider": "google",
            "openid_tokens": "[]",
            "account_switcher_uids": f'["{self.uid_phone_mail}"]',
            "fb4a_shared_phone_cpl_experiment": "fb4a_shared_phone_nonce_cpl_at_risk_v3",
            "fb4a_shared_phone_cpl_group": "enable_v3_at_risk",
            "enroll_misauth": "false",
            "error_detail_type": "button_with_disabled",
            "source": "login",
            "machine_id": self.machine_id,
            "jazoest": self.jazoest,
            "meta_inf_fbmeta": "V2_UNTAGGED",
            "advertiser_id": self.adid,
            "encrypted_msisdn": "",
            "currently_logged_in_userid": "0",
            "fb_api_req_friendly_name": "authenticate",
            "fb_api_caller_class": "Fb4aAuthHandler",
            "sig": self.SIG
        }
        return base_data
    
    def _get_user_name(self, access_token):
        """Lấy tên người dùng từ token"""
        try:
            r = requests.get(f"https://graph.facebook.com/me?access_token={access_token}", timeout=10)
            if r.status_code == 200:
                return r.json().get('name', 'Unknown')
        except:
            pass
        return "Unknown"
    
    def _convert_token(self, access_token, target_app):
        """Chuyển đổi token sang ứng dụng khác"""
        try:
            app_id = FacebookAppTokens.get_app_id(target_app)
            if not app_id:
                return None
            
            response = requests.post(
                'https://api.facebook.com/method/auth.getSessionforApp',
                data={
                    'access_token': access_token,
                    'format': 'json',
                    'new_app_id': app_id,
                    'generate_session_cookies': '1'
                },
                timeout=15
            )
            
            result = response.json()
            
            if 'access_token' in result:
                token = result['access_token']
                prefix = FacebookAppTokens.extract_token_prefix(token)
                
                cookies_dict = {}
                cookies_string = ""
                
                if 'session_cookies' in result:
                    for cookie in result['session_cookies']:
                        cookies_dict[cookie['name']] = cookie['value']
                        cookies_string += f"{cookie['name']}={cookie['value']}; "
                
                return {
                    'token_prefix': prefix,
                    'access_token': token,
                    'cookies': {
                        'dict': cookies_dict,
                        'string': cookies_string.rstrip('; ')
                    }
                }
            
            return None
        except:
            return None
    
    def _parse_success_response(self, response_json):
        """Xử lý response thành công"""
        original_token = response_json.get('access_token')
        original_prefix = FacebookAppTokens.extract_token_prefix(original_token)
        account_name = self._get_user_name(original_token)
        
        result = {
            'success': True,
            'name': account_name,
            'uid': response_json.get('session_cookies', [{}])[0].get('value', '') if response_json.get('session_cookies') else '',
            'original_token': {
                'token_prefix': original_prefix,
                'access_token': original_token
            },
            'cookies': {},
            'converted_tokens': {}
        }
        
        # Lấy cookies
        if 'session_cookies' in response_json:
            cookies_dict = {}
            cookies_string = ""
            uid_value = ""
            for cookie in response_json['session_cookies']:
                cookies_dict[cookie['name']] = cookie['value']
                cookies_string += f"{cookie['name']}={cookie['value']}; "
                if cookie['name'] == 'c_user':
                    uid_value = cookie['value']
            result['cookies'] = {
                'dict': cookies_dict,
                'string': cookies_string.rstrip('; ')
            }
            if uid_value:
                result['uid'] = uid_value
        
        # Chuyển đổi token
        if self.convert_token_to:
            # Bỏ qua FB_ANDROID vì đã có token gốc
            apps_to_process = [app for app in self.convert_token_to if app != 'FB_ANDROID']
            total_apps = len(apps_to_process)
            
            if self.show_progress:
                with print_lock:
                    print(f"{Fore.BLUE}[INFO] {self.uid_phone_mail} | Đang lấy token cho {total_apps} ứng dụng...")
            
            for index, target_app in enumerate(apps_to_process):
                percent = int(((index + 1) / total_apps) * 100)
                
                # Hiển thị tiến trình
                if self.show_progress:
                    bar_len = 20
                    filled = int(bar_len * (index + 1) // total_apps)
                    bar = "█" * filled + "░" * (bar_len - filled)
                    app_info = FacebookAppTokens.get_app_info(target_app)
                    
                    with print_lock:
                        sys.stdout.write(f"\r{Fore.CYAN}[{self.uid_phone_mail[:20]}] {Fore.GREEN}[{bar}] {percent}% {Fore.YELLOW}>> {app_info['name'][:25]}...")
                        sys.stdout.flush()
                
                converted = self._convert_token(original_token, target_app)
                if converted:
                    result['converted_tokens'][target_app] = converted
                
                time.sleep(0.05)  # Tránh rate limit
            
            if self.show_progress:
                with print_lock:
                    print()  # Xuống dòng sau khi hoàn thành
        
        return result
    
    def _handle_2fa(self, error_data):
        """Xử lý xác thực 2FA"""
        if not self.twwwoo2fa:
            return {'success': False, 'error': 'Cần mã 2FA nhưng chưa được cung cấp'}
        
        try:
            clean_2fa_key = self.twwwoo2fa.replace(" ", "")
            twofactor_code = pyotp.TOTP(clean_2fa_key).now()
            
            data_2fa = {
                'locale': 'vi_VN',
                'format': 'json',
                'email': self.uid_phone_mail,
                'device_id': self.device_id,
                'access_token': self.ACCESS_TOKEN,
                'generate_session_cookies': 'true',
                'generate_machine_id': '1',
                'twofactor_code': twofactor_code,
                'credentials_type': 'two_factor',
                'error_detail_type': 'button_with_disabled',
                'first_factor': error_data.get('login_first_factor', ''),
                'password': self.password,
                'userid': error_data.get('uid', ''),
                'machine_id': error_data.get('login_first_factor', '')
            }
            
            response = self.session.post(self.API_URL, data=data_2fa, headers=self.headers, timeout=30)
            response_json = response.json()
            
            if 'access_token' in response_json:
                return self._parse_success_response(response_json)
            elif 'error' in response_json:
                return {
                    'success': False,
                    'error': response_json['error'].get('message', 'Unknown error')
                }
            
        except Exception as e:
            return {'success': False, 'error': f'Lỗi 2FA: {str(e)}'}
        
        return {'success': False, 'error': 'Không thể xử lý 2FA'}
    
    def login(self):
        """Thực hiện đăng nhập"""
        try:
            response = self.session.post(self.API_URL, headers=self.headers, data=self.data, timeout=30)
            response_json = response.json()
            
            if 'access_token' in response_json:
                self.result = self._parse_success_response(response_json)
                return self.result
            
            if 'error' in response_json:
                error_data = response_json.get('error', {}).get('error_data', {})
                
                if 'login_first_factor' in error_data and 'uid' in error_data:
                    if self.show_progress:
                        with print_lock:
                            print(f"{Fore.MAGENTA}[2FA] {self.uid_phone_mail} | Yêu cầu 2FA. Đang xác thực...")
                    self.result = self._handle_2fa(error_data)
                    return self.result
                
                self.result = {
                    'success': False,
                    'error': response_json['error'].get('message', 'Unknown error'),
                    'error_user_msg': response_json['error'].get('error_user_msg')
                }
                return self.result
            
            self.result = {'success': False, 'error': 'Không xác định được response'}
            return self.result
            
        except json.JSONDecodeError:
            self.result = {'success': False, 'error': 'Response không phải JSON hợp lệ'}
            return self.result
        except requests.exceptions.Timeout:
            self.result = {'success': False, 'error': 'Timeout - Server không phản hồi'}
            return self.result
        except Exception as e:
            self.result = {'success': False, 'error': str(e)}
            return self.result

# ===================================================================
# PHẦN 4: GIAO DIỆN NGƯỜI DÙNG
# ===================================================================

def clear_screen():
    """Xóa màn hình"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """In banner chương trình"""
    clear_screen()
    banner = f"""
{Fore.CYAN}{Style.BRIGHT}╔══════════════════════════════════════════════════════════════════╗
║                                                                  ║
║  {Fore.YELLOW}███████╗ █████╗  ██████╗███████╗██████╗  ██████╗  {Fore.CYAN}║
║  {Fore.YELLOW}██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗ {Fore.CYAN}║
║  {Fore.YELLOW}█████╗  ███████║██║     █████╗  ██████╔╝██║   ██║ {Fore.CYAN}║
║  {Fore.YELLOW}██╔══╝  ██╔══██║██║     ██╔══╝  ██╔══██╗██║   ██║ {Fore.CYAN}║
║  {Fore.YELLOW}██║     ██║  ██║╚██████╗███████╗██║  ██║╚██████╔╝ {Fore.CYAN}║
║  {Fore.YELLOW}╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝╚═╝  ╚═╝ ╚═════╝  {Fore.CYAN}║
║                                                                  ║
║  {Fore.GREEN}   FACEBOOK TOKEN & COOKIE EXTRACTOR PRO v{VERSION}       {Fore.CYAN}║
║                                                                  ║
║  {Fore.WHITE}   Author : {Fore.LIGHTYELLOW_EX}{AUTHOR}                         {Fore.CYAN}║
║  {Fore.WHITE}   Facebook: {Fore.LIGHTBLUE_EX}{FACEBOOK_URL}              {Fore.CYAN}║
║  {Fore.WHITE}   Zalo   : {Fore.LIGHTGREEN_EX}{ZALO}                              {Fore.CYAN}║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
{Style.RESET_ALL}"""

    print(banner)

def print_menu():
    """In menu chính"""
    print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                        {Fore.YELLOW}MENU CHÍNH{Fore.CYAN}                            ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  {Fore.GREEN}[1] {Fore.WHITE}Nhập thông tin thủ công (CMD)                    {Fore.CYAN}║
║  {Fore.GREEN}[2] {Fore.WHITE}Đọc từ file data.txt                            {Fore.CYAN}║
║  {Fore.GREEN}[3] {Fore.WHITE}Xem hướng dẫn sử dụng                          {Fore.CYAN}║
║  {Fore.RED}[0] {Fore.WHITE}Thoát chương trình                              {Fore.CYAN}║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
{Fore.YELLOW}┌─ {Fore.WHITE}Lựa chọn của bạn{Fore.YELLOW} › {Fore.WHITE}""", end="")

def print_help():
    """In hướng dẫn sử dụng"""
    clear_screen()
    help_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗
║                    {Fore.YELLOW}HƯỚNG DẪN SỬ DỤNG{Fore.CYAN}                      ║
╚══════════════════════════════════════════════════════════════════╝

{Fore.GREEN}1. CHẾ ĐỘ NHẬP THỦ CÔNG (CMD){Fore.WHITE}
   - Nhập email/SĐT/UID
   - Nhập mật khẩu
   - Nhập mã 2FA (nếu có, để trống nếu không)
   - Kết quả sẽ được lưu vào file {Fore.YELLOW}tokens_and_cookies.txt{Fore.WHITE}

{Fore.GREEN}2. CHẾ ĐỘ ĐỌC FILE{Fore.WHITE}
   - Tạo file {Fore.YELLOW}data.txt{Fore.WHITE} với định dạng:
   {Fore.CYAN}  user|password|2fa_secret{Fore.WHITE}
   
   Ví dụ:
   {Fore.CYAN}  example@gmail.com|myPassword123|G4G7Z6SNWUTLTTV72UNZD2FHJAEOVHT3
   user2@gmail.com|pass123|{Fore.WHITE}
   
   - File sẽ được đọc và xử lý từng dòng
   - Hỗ trợ đa luồng để xử lý nhanh

{Fore.GREEN}3. KẾT QUẢ XUẤT RA{Fore.WHITE}
   - File: {Fore.YELLOW}tokens_and_cookies.txt{Fore.WHITE}
   - Bao gồm:
     • Cookie đầy đủ (c_user, xs, fr, datr, ...)
     • Token gốc (FB Android)
     • Token chuyển đổi cho 15 ứng dụng khác
     • Thông tin UID và tên người dùng

{Fore.GREEN}4. LƯU Ý{Fore.RED}
   ⚠ Tool này chỉ dùng cho mục đích học tập và nghiên cứu
   ⚠ Không sử dụng để tấn công, spam hoặc vi phạm điều khoản Facebook
   ⚠ Tác giả không chịu trách nhiệm với mục đích sử dụng sai

{Fore.YELLOW}Press Enter để quay lại menu...{Fore.WHITE}"""
    print(help_text)
    input()

# ===================================================================
# PHẦN 5: XỬ LÝ ĐĂNG NHẬP VÀ LƯU KẾT QUẢ
# ===================================================================

def format_result(result, uid_phone_mail):
    """Định dạng kết quả để lưu ra file"""
    if not result.get('success'):
        return f"""
{'='*50}
❌ THẤT BẠI: {uid_phone_mail}
Lỗi: {result.get('error', 'Unknown error')}
{'='*50}
"""

    output = []
    output.append("=" * 70)
    output.append(f"✅ THÀNH CÔNG: {uid_phone_mail}")
    output.append(f"📛 Tên: {result.get('name', 'Unknown')}")
    output.append(f"🆔 UID: {result.get('uid', 'Unknown')}")
    output.append("=" * 70)
    output.append("")
    
    # Cookies
    if result.get('cookies'):
        output.append("🍪 COOKIES:")
        output.append("-" * 50)
        output.append(result['cookies']['string'])
        output.append("-" * 50)
        output.append("")
    
    # Token gốc
    if result.get('original_token'):
        output.append("🎯 TOKEN GỐC (Facebook Android):")
        output.append("-" * 50)
        output.append(f"Prefix: {result['original_token']['token_prefix']}")
        output.append(f"Token: {result['original_token']['access_token']}")
        output.append("-" * 50)
        output.append("")
    
    # Token chuyển đổi
    if result.get('converted_tokens'):
        output.append("🔄 TOKEN CHUYỂN ĐỔI:")
        output.append("=" * 50)
        
        success_count = 0
        fail_count = 0
        
        for app_key, token_data in result['converted_tokens'].items():
            app_info = FacebookAppTokens.get_app_info(app_key)
            app_name = app_info['name'] if app_info else app_key
            platform = app_info['platform'] if app_info else 'Unknown'
            
            output.append(f"\n📱 {app_name} ({platform})")
            output.append(f"   Prefix: {token_data['token_prefix']}")
            output.append(f"   Token: {token_data['access_token']}")
            success_count += 1
        
        # Liệt kê các app thất bại
        all_apps = FacebookAppTokens.get_all_app_keys()
        converted_keys = set(result['converted_tokens'].keys())
        
        for app_key in all_apps:
            if app_key == 'FB_ANDROID':
                continue
            if app_key not in converted_keys:
                app_info = FacebookAppTokens.get_app_info(app_key)
                app_name = app_info['name'] if app_info else app_key
                output.append(f"\n❌ {app_name}: Get Token Failed")
                fail_count += 1
        
        output.append("")
        output.append("-" * 50)
        output.append(f"✅ Thành công: {success_count}  ❌ Thất bại: {fail_count}")
        output.append("=" * 50)
    
    output.append("")
    output.append("=" * 70)
    output.append(f"🕐 Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append("=" * 70)
    output.append("")
    
    return "\n".join(output)

def save_to_file(content, filename=OUTPUT_FILE):
    """Lưu kết quả vào file"""
    with file_lock:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content)
            f.write("\n\n")

def process_single_account(uid, password, fa2=""):
    """Xử lý một tài khoản đơn lẻ"""
    try:
        with print_lock:
            print(f"{Fore.YELLOW}[START] Đang xử lý: {uid}...")
        
        fb_login = FacebookLogin(
            uid_phone_mail=uid,
            password=password,
            twwwoo2fa=fa2,
            convert_all_tokens=True,
            show_progress=True
        )
        
        result = fb_login.login()
        
        if result.get('success'):
            # Lưu kết quả
            content = format_result(result, uid)
            save_to_file(content)
            
            with print_lock:
                print(f"{Fore.GREEN}[SUCCESS] ✅ {uid} | Tên: {result.get('name', 'Unknown')} | Đã lưu thành công!")
                print(f"{Fore.CYAN}→ Kiểm tra file {OUTPUT_FILE}")
            return result
        else:
            error_msg = result.get('error_user_msg') if result.get('error_user_msg') else result.get('error', 'Unknown error')
            with print_lock:
                print(f"{Fore.RED}[FAILED] ❌ {uid} | Lỗi: {error_msg}")
            
            # Lưu lỗi vào file
            content = format_result(result, uid)
            save_to_file(content)
            return result
            
    except Exception as e:
        with print_lock:
            print(f"{Fore.RED}[ERROR] ❌ {uid} | Exception: {str(e)}")
        
        # Lưu lỗi vào file
        content = f"""
{'='*50}
❌ LỖI: {uid}
Lỗi: {str(e)}
{'='*50}
"""
        save_to_file(content)
        return {'success': False, 'error': str(e)}

def process_from_file(filename="data.txt", max_workers=5):
    """Xử lý từ file data.txt"""
    if not os.path.exists(filename):
        print(f"{Fore.RED}❌ Không tìm thấy file '{filename}'")
        print(f"{Fore.YELLOW}📌 Vui lòng tạo file '{filename}' với định dạng: user|password|2fa")
        input("Press Enter để tiếp tục...")
        return
    
    with open(filename, 'r', encoding='utf-8') as f:
        accounts = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not accounts:
        print(f"{Fore.RED}❌ File '{filename}' trống hoặc không có dữ liệu hợp lệ!")
        input("Press Enter để tiếp tục...")
        return
    
    print(f"{Fore.CYAN}📁 Đã tìm thấy {len(accounts)} tài khoản trong {filename}")
    
    # Xóa file output cũ nếu có
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        print(f"{Fore.YELLOW}🗑️ Đã xóa file output cũ: {OUTPUT_FILE}")
    
    print(f"{Fore.GREEN}🚀 Bắt đầu xử lý với {max_workers} luồng...")
    print("=" * 70)
    
    # Danh sách tài khoản cần xử lý
    account_list = []
    for acc in accounts:
        parts = acc.split('|')
        uid = parts[0].strip()
        pwd = parts[1].strip() if len(parts) > 1 else ""
        fa2 = parts[2].strip().replace(" ", "") if len(parts) > 2 else ""
        account_list.append((uid, pwd, fa2))
    
    start_time = time.time()
    
    # Xử lý đa luồng
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for uid, pwd, fa2 in account_list:
            future = executor.submit(process_single_account, uid, pwd, fa2)
            futures.append(future)
        
        # Đợi tất cả hoàn thành
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"{Fore.RED}Lỗi trong luồng: {e}")
    
    elapsed_time = time.time() - start_time
    
    print("=" * 70)
    print(f"{Fore.GREEN}✅ HOÀN TẤT QUÁ TRÌNH XỬ LÝ!")
    print(f"{Fore.CYAN}⏱️ Thời gian: {elapsed_time:.2f} giây")
    print(f"{Fore.YELLOW}📁 Kết quả được lưu trong: {OUTPUT_FILE}")
    input(f"\n{Fore.WHITE}Press Enter để tiếp tục...")

def manual_input():
    """Nhập thông tin thủ công từ CMD"""
    print_banner()
    print(f"\n{Fore.CYAN}╔══════════════════════════════════════════════════════════════════╗")
    print(f"║              {Fore.YELLOW}NHẬP THÔNG TIN TÀI KHOẢN{Fore.CYAN}                  ║")
    print(f"╚══════════════════════════════════════════════════════════════════╝\n")
    
    # Nhập email
    uid = input(f"{Fore.GREEN}📧 Email/SĐT/UID{Fore.WHITE}: ").strip()
    if not uid:
        print(f"{Fore.RED}❌ Không được để trống!")
        input("Press Enter để tiếp tục...")
        return
    
    # Nhập mật khẩu
    pwd = input(f"{Fore.GREEN}🔑 Mật khẩu{Fore.WHITE}: ").strip()
    if not pwd:
        print(f"{Fore.RED}❌ Không được để trống!")
        input("Press Enter để tiếp tục...")
        return
    
    # Nhập 2FA (có thể để trống)
    fa2 = input(f"{Fore.GREEN}🔐 Mã 2FA (để trống nếu không có){Fore.WHITE}: ").strip().replace(" ", "")
    
    # Xác nhận
    print(f"\n{Fore.YELLOW}📋 Thông tin đã nhập:")
    print(f"  {Fore.CYAN}User: {Fore.WHITE}{uid}")
    print(f"  {Fore.CYAN}Pass: {Fore.WHITE}{'*' * len(pwd)}")
    if fa2:
        print(f"  {Fore.CYAN}2FA : {Fore.WHITE}{fa2[:10]}...")
    else:
        print(f"  {Fore.CYAN}2FA : {Fore.WHITE}Không sử dụng")
    
    confirm = input(f"\n{Fore.GREEN}👉 Xác nhận xử lý? (y/n){Fore.WHITE}: ").strip().lower()
    if confirm != 'y':
        print(f"{Fore.YELLOW}Đã hủy!")
        input("Press Enter để tiếp tục...")
        return
    
    # Xóa file output cũ
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    
    # Xử lý
    print(f"\n{Fore.GREEN}🚀 Bắt đầu xử lý...\n")
    process_single_account(uid, pwd, fa2)
    
    print(f"\n{Fore.GREEN}✅ Hoàn tất!")
    print(f"{Fore.CYAN}📁 Kết quả được lưu trong: {OUTPUT_FILE}")
    input(f"\n{Fore.WHITE}Press Enter để tiếp tục...")

# ===================================================================
# PHẦN 6: MAIN
# ===================================================================

def main():
    """Chương trình chính"""
    while True:
        print_banner()
        print_menu()
        
        try:
            choice = input().strip()
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}👋 Tạm biệt!")
            sys.exit(0)
        
        if choice == "1":
            manual_input()
        elif choice == "2":
            # Hỏi số luồng
            print(f"\n{Fore.CYAN}⚙️ Cấu hình đa luồng:")
            try:
                max_workers = int(input(f"{Fore.YELLOW}Nhập số luồng (mặc định 5){Fore.WHITE}: ").strip() or "5")
                if max_workers < 1:
                    max_workers = 1
                if max_workers > 20:
                    print(f"{Fore.YELLOW}⚠️ Giới hạn tối đa 20 luồng!")
                    max_workers = 20
            except ValueError:
                max_workers = 5
                print(f"{Fore.YELLOW}⚠️ Sử dụng mặc định: 5 luồng")
            
            process_from_file("data.txt", max_workers)
        elif choice == "3":
            print_help()
        elif choice == "0":
            print(f"\n{Fore.GREEN}👋 Cảm ơn bạn đã sử dụng tool!")
            print(f"{Fore.CYAN}📌 Author: {AUTHOR}")
            print(f"{Fore.CYAN}📌 Facebook: {FACEBOOK_URL}")
            print(f"{Fore.CYAN}📌 Zalo: {ZALO}")
            sys.exit(0)
        else:
            print(f"{Fore.RED}❌ Lựa chọn không hợp lệ!")
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}👋 Tạm biệt!")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}❌ Lỗi không mong muốn: {e}")
        input("Press Enter để thoát...")