# facebook_token_extractor_ui_allinone.py
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
FACEBOOK TOKEN & COOKIE EXTRACTOR PRO v2.0.0 - GUI Edition (All-in-One)
Author: Từ Quang Nam
"""

import sys
import os
import json
import time
import random
import string
import struct
import io
import base64
import uuid
import threading
import concurrent.futures
from datetime import datetime
from Crypto.Cipher import AES, PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import requests
import pyotp

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

# ===================================================================
# PHẦN 1: CORE LOGIC - Từ file gốc
# ===================================================================

# --- CẤU HÌNH TOÀN CỤ ---
VERSION = "2.0.0"
AUTHOR = "Từ Quang Nam"
FACEBOOK_URL = "fb.com/tuquangnam07"
ZALO = "0888385536"
OUTPUT_FILE = "tokens_and_cookies.txt"


# ===================================================================
# PHẦN 1.1: MÃ HÓA MẬT KHẨU FACEBOOK
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
# PHẦN 1.2: DANH SÁCH ỨNG DỤNG FACEBOOK
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
        return list(FacebookAppTokens.APPS.keys())
    
    @staticmethod
    def get_app_id(app_key):
        app = FacebookAppTokens.APPS.get(app_key)
        return app['app_id'] if app else None
    
    @staticmethod
    def get_app_info(app_key):
        return FacebookAppTokens.APPS.get(app_key)
    
    @staticmethod
    def get_prefix_hint(app_key):
        app = FacebookAppTokens.APPS.get(app_key)
        return app['prefix'] if app else "UNKNOWN"
    
    @staticmethod
    def extract_token_prefix(token):
        if not token:
            return "UNKNOWN"
        for i, char in enumerate(token):
            if char.islower():
                return token[:i]
        return token[:10] if len(token) > 10 else token


# ===================================================================
# PHẦN 1.3: ĐĂNG NHẬP FACEBOOK
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
        self.uid_phone_mail = uid_phone_mail
        self.twwwoo2fa = twwwoo2fa.replace(" ", "") if twwwoo2fa else ""
        self.show_progress = show_progress
        
        if password.startswith("#PWD_FB4A"):
            self.password = password
        else:
            self.password = FacebookPasswordEncryptor.encrypt(password)
        
        if convert_all_tokens:
            self.convert_token_to = FacebookAppTokens.get_all_app_keys()
        else:
            self.convert_token_to = []
        
        self.session = requests.Session()
        self.device_id = str(uuid.uuid4())
        self.adid = str(uuid.uuid4())
        self.secure_family_device_id = str(uuid.uuid4())
        self.machine_id = machine_id if machine_id else self._generate_machine_id()
        self.jazoest = ''.join(random.choices(string.digits, k=5))
        self.sim_serial = ''.join(random.choices(string.digits, k=20))
        
        self.headers = self._build_headers()
        self.data = self._build_data()
        self.result = None
    
    @staticmethod
    def _generate_machine_id():
        return ''.join(random.choices(string.ascii_letters + string.digits, k=24))
    
    def _build_headers(self):
        headers = self.BASE_HEADERS.copy()
        headers.update({
            "x-fb-request-analytics-tags": '{"network_tags":{"product":"350685531728","retry_attempt":"0"},"application_tags":"unknown"}',
            "user-agent": "Dalvik/2.1.0 (Linux; U; Android 9; 23113RKC6C Build/PQ3A.190705.08211809) [FBAN/FB4A;FBAV/417.0.0.33.65;FBPN/com.facebook.katana;FBLC/vi_VN;FBBV/480086274;FBCR/MobiFone;FBMF/Redmi;FBBD/Redmi;FBDV/23113RKC6C;FBSV/9;FBCA/x86:armeabi-v7a;FBDM/{density=1.5,width=1280,height=720};FB_FW/1;FBRV/0;]"
        })
        return headers
    
    def _build_data(self):
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
        try:
            r = requests.get(f"https://graph.facebook.com/me?access_token={access_token}", timeout=10)
            if r.status_code == 200:
                return r.json().get('name', 'Unknown')
        except:
            pass
        return "Unknown"
    
    def _convert_token(self, access_token, target_app):
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
        
        if self.convert_token_to:
            apps_to_process = [app for app in self.convert_token_to if app != 'FB_ANDROID']
            total_apps = len(apps_to_process)
            
            for index, target_app in enumerate(apps_to_process):
                converted = self._convert_token(original_token, target_app)
                if converted:
                    result['converted_tokens'][target_app] = converted
                time.sleep(0.05)
        
        return result
    
    def _handle_2fa(self, error_data):
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
        try:
            response = self.session.post(self.API_URL, headers=self.headers, data=self.data, timeout=30)
            response_json = response.json()
            
            if 'access_token' in response_json:
                self.result = self._parse_success_response(response_json)
                return self.result
            
            if 'error' in response_json:
                error_data = response_json.get('error', {}).get('error_data', {})
                
                if 'login_first_factor' in error_data and 'uid' in error_data:
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
# PHẦN 2: UI - GIAO DIỆN NGƯỜI DÙNG
# ===================================================================

class WorkerSignals(QObject):
    """Tín hiệu cho worker thread"""
    log = pyqtSignal(str, str)
    progress = pyqtSignal(int, int)
    finished = pyqtSignal()
    account_done = pyqtSignal(str, bool, str)


class Worker(QRunnable):
    """Worker thread để xử lý tài khoản"""
    
    def __init__(self, accounts, max_workers=5):
        super().__init__()
        self.accounts = accounts
        self.max_workers = max_workers
        self.signals = WorkerSignals()
        self.is_running = True
        self.total = len(accounts)
        self.completed = 0
        self.file_lock = threading.Lock()
        
    def run(self):
        """Chạy xử lý"""
        from concurrent.futures import ThreadPoolExecutor
        
        self.signals.log.emit("🚀 Bắt đầu xử lý tài khoản...", "info")
        self.signals.log.emit(f"📊 Số tài khoản: {self.total}", "info")
        self.signals.log.emit(f"⚡ Số luồng: {self.max_workers}", "info")
        self.signals.log.emit("=" * 60, "info")
        
        start_time = time.time()
        
        # Xóa file output cũ
        if os.path.exists(OUTPUT_FILE):
            os.remove(OUTPUT_FILE)
        
        # Xử lý đa luồng
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = []
            for uid, pwd, fa2 in self.accounts:
                if not self.is_running:
                    break
                future = executor.submit(self._process_account, uid, pwd, fa2)
                futures.append(future)
            
            for future in futures:
                if not self.is_running:
                    break
                try:
                    future.result()
                except Exception as e:
                    self.signals.log.emit(f"❌ Lỗi luồng: {str(e)}", "error")
        
        elapsed = time.time() - start_time
        
        self.signals.log.emit("=" * 60, "info")
        self.signals.log.emit(f"✅ HOÀN TẤT! Thời gian: {elapsed:.2f} giây", "success")
        self.signals.log.emit(f"📁 Kết quả được lưu trong: {OUTPUT_FILE}", "info")
        self.signals.finished.emit()
    
    def _process_account(self, uid, password, fa2):
        """Xử lý một tài khoản"""
        if not self.is_running:
            return
        
        try:
            self.signals.log.emit(f"🔄 Đang xử lý: {uid[:20]}...", "process")
            
            self.completed += 1
            self.signals.progress.emit(self.completed, self.total)
            
            fb_login = FacebookLogin(
                uid_phone_mail=uid,
                password=password,
                twwwoo2fa=fa2,
                convert_all_tokens=True,
                show_progress=False
            )
            
            result = fb_login.login()
            
            if result.get('success'):
                name = result.get('name', 'Unknown')
                self.signals.log.emit(f"✅ {uid[:20]}... | {name} | Thành công!", "success")
                self.signals.account_done.emit(uid, True, name)
                self._save_result(result, uid)
            else:
                error = result.get('error_user_msg') or result.get('error', 'Unknown error')
                self.signals.log.emit(f"❌ {uid[:20]}... | Lỗi: {error[:50]}", "error")
                self.signals.account_done.emit(uid, False, error)
                self._save_error(uid, error)
                
        except Exception as e:
            self.signals.log.emit(f"⚠️ {uid[:20]}... | Exception: {str(e)[:50]}", "error")
            self.signals.account_done.emit(uid, False, str(e))
            self._save_error(uid, str(e))
    
    def _save_result(self, result, uid):
        """Lưu kết quả thành công"""
        with self.file_lock:
            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write("=" * 70 + "\n")
                f.write(f"✅ THÀNH CÔNG: {uid}\n")
                f.write(f"📛 Tên: {result.get('name', 'Unknown')}\n")
                f.write(f"🆔 UID: {result.get('uid', 'Unknown')}\n")
                f.write("=" * 70 + "\n\n")
                
                if result.get('cookies'):
                    f.write("🍪 COOKIES:\n")
                    f.write("-" * 50 + "\n")
                    f.write(result['cookies']['string'] + "\n")
                    f.write("-" * 50 + "\n\n")
                
                if result.get('original_token'):
                    f.write("🎯 TOKEN GỐC (Facebook Android):\n")
                    f.write("-" * 50 + "\n")
                    f.write(f"Prefix: {result['original_token']['token_prefix']}\n")
                    f.write(f"Token: {result['original_token']['access_token']}\n")
                    f.write("-" * 50 + "\n\n")
                
                if result.get('converted_tokens'):
                    f.write("🔄 TOKEN CHUYỂN ĐỔI:\n")
                    f.write("=" * 50 + "\n")
                    for app_key, token_data in result['converted_tokens'].items():
                        app_info = FacebookAppTokens.get_app_info(app_key)
                        app_name = app_info['name'] if app_info else app_key
                        platform = app_info['platform'] if app_info else 'Unknown'
                        f.write(f"\n📱 {app_name} ({platform})\n")
                        f.write(f"   Prefix: {token_data['token_prefix']}\n")
                        f.write(f"   Token: {token_data['access_token']}\n")
                    f.write("=" * 50 + "\n")
                
                f.write("\n" + "=" * 70 + "\n")
                f.write(f"🕐 Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("=" * 70 + "\n\n")
    
    def _save_error(self, uid, error):
        """Lưu lỗi"""
        with self.file_lock:
            with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                f.write("=" * 50 + "\n")
                f.write(f"❌ THẤT BẠI: {uid}\n")
                f.write(f"Lỗi: {error}\n")
                f.write("=" * 50 + "\n\n")
    
    def stop(self):
        """Dừng xử lý"""
        self.is_running = False


class LogWidget(QPlainTextEdit):
    """Widget hiển thị log"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 10))
        self.setMaximumBlockCount(10000)
        self.setLineWrapMode(QPlainTextEdit.NoWrap)
        self.auto_scroll = True
        
    def append_log(self, message, color_type="info"):
        """Thêm log với màu sắc"""
        colors = {
            "info": "#4a9eff",
            "success": "#00d05a",
            "error": "#ff4757",
            "warning": "#ffa502",
            "process": "#ff6b6b",
            "debug": "#a8b2d1"
        }
        
        color = colors.get(color_type, "#ffffff")
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        html = f'<span style="color: #666;">[{timestamp}]</span> <span style="color: {color};">{message}</span>'
        self.appendHtml(html)
        
        if self.auto_scroll:
            scrollbar = self.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    def set_auto_scroll(self, enabled):
        self.auto_scroll = enabled


class ThemeManager:
    """Quản lý theme"""
    
    THEMES = {
        "dark": {
            "name": "Dark",
            "bg_primary": "#1a1a2e",
            "bg_secondary": "#16213e",
            "bg_card": "#0f3460",
            "text_primary": "#ffffff",
            "text_secondary": "#a8b2d1",
            "accent": "#64ffda",
            "accent2": "#4a9eff",
            "success": "#00d05a",
            "error": "#ff4757",
            "warning": "#ffa502",
            "border": "#2a2a4a"
        },
        "light": {
            "name": "Light",
            "bg_primary": "#f0f2f5",
            "bg_secondary": "#ffffff",
            "bg_card": "#e8ecf1",
            "text_primary": "#1a1a2e",
            "text_secondary": "#4a4a6a",
            "accent": "#0066ff",
            "accent2": "#4a9eff",
            "success": "#00b894",
            "error": "#e17055",
            "warning": "#fdcb6e",
            "border": "#dcdde1"
        },
        "ocean": {
            "name": "Ocean",
            "bg_primary": "#0c2461",
            "bg_secondary": "#1e3799",
            "bg_card": "#4a69bd",
            "text_primary": "#ffffff",
            "text_secondary": "#b8c6db",
            "accent": "#78e08f",
            "accent2": "#38ada9",
            "success": "#78e08f",
            "error": "#eb4d4b",
            "warning": "#f6b93b",
            "border": "#3c6382"
        }
    }
    
    def __init__(self):
        self.current_theme = "dark"
    
    def get_style(self, theme_name):
        theme = self.THEMES.get(theme_name, self.THEMES["dark"])
        
        return f"""
        QMainWindow, QDialog {{
            background-color: {theme['bg_primary']};
            color: {theme['text_primary']};
        }}
        QWidget {{
            background-color: transparent;
            color: {theme['text_primary']};
        }}
        QFrame, QGroupBox {{
            background-color: {theme['bg_secondary']};
            border: 1px solid {theme['border']};
            border-radius: 10px;
            padding: 5px;
        }}
        QLabel {{
            color: {theme['text_primary']};
            font-size: 12px;
        }}
        QPushButton {{
            background-color: {theme['accent']};
            color: {theme['bg_primary']};
            border: none;
            border-radius: 8px;
            padding: 10px 20px;
            font-weight: bold;
            font-size: 13px;
        }}
        QPushButton:hover {{
            background-color: {theme['accent2']};
        }}
        QPushButton:pressed {{
            background-color: {theme['border']};
        }}
        QPushButton:disabled {{
            background-color: {theme['border']};
            color: {theme['text_secondary']};
        }}
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {theme['bg_primary']};
            color: {theme['text_primary']};
            border: 1px solid {theme['border']};
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 12px;
        }}
        QLineEdit:focus, QTextEdit:focus {{
            border: 2px solid {theme['accent']};
        }}
        QComboBox {{
            background-color: {theme['bg_primary']};
            color: {theme['text_primary']};
            border: 1px solid {theme['border']};
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 12px;
        }}
        QComboBox::drop-down {{
            border: none;
        }}
        QComboBox QAbstractItemView {{
            background-color: {theme['bg_secondary']};
            color: {theme['text_primary']};
            selection-background-color: {theme['accent']};
            selection-color: {theme['bg_primary']};
        }}
        QTabWidget::pane {{
            background-color: {theme['bg_secondary']};
            border: 1px solid {theme['border']};
            border-radius: 10px;
        }}
        QTabBar::tab {{
            background-color: {theme['bg_primary']};
            color: {theme['text_secondary']};
            padding: 10px 20px;
            margin: 2px;
            border-radius: 8px 8px 0 0;
        }}
        QTabBar::tab:selected {{
            background-color: {theme['accent']};
            color: {theme['bg_primary']};
        }}
        QTabBar::tab:hover {{
            background-color: {theme['accent2']};
            color: {theme['bg_primary']};
        }}
        QScrollBar:vertical {{
            background-color: {theme['bg_primary']};
            border-radius: 5px;
            width: 8px;
        }}
        QScrollBar::handle:vertical {{
            background-color: {theme['border']};
            border-radius: 5px;
            min-height: 20px;
        }}
        QScrollBar::handle:vertical:hover {{
            background-color: {theme['accent']};
        }}
        QScrollBar:horizontal {{
            background-color: {theme['bg_primary']};
            border-radius: 5px;
            height: 8px;
        }}
        QScrollBar::handle:horizontal {{
            background-color: {theme['border']};
            border-radius: 5px;
            min-width: 20px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background-color: {theme['accent']};
        }}
        QProgressBar {{
            background-color: {theme['bg_primary']};
            border: 1px solid {theme['border']};
            border-radius: 8px;
            height: 20px;
            text-align: center;
            color: {theme['text_primary']};
        }}
        QProgressBar::chunk {{
            background-color: {theme['accent']};
            border-radius: 8px;
        }}
        QTableWidget {{
            background-color: {theme['bg_primary']};
            border: 1px solid {theme['border']};
            border-radius: 8px;
            gridline-color: {theme['border']};
        }}
        QTableWidget::item {{
            padding: 5px;
            color: {theme['text_primary']};
        }}
        QTableWidget::item:selected {{
            background-color: {theme['accent']};
            color: {theme['bg_primary']};
        }}
        QHeaderView::section {{
            background-color: {theme['bg_secondary']};
            color: {theme['text_secondary']};
            padding: 5px;
            border: 1px solid {theme['border']};
        }}
        QCheckBox {{
            color: {theme['text_primary']};
        }}
        QCheckBox::indicator {{
            border-radius: 4px;
            border: 2px solid {theme['border']};
            width: 18px;
            height: 18px;
        }}
        QCheckBox::indicator:checked {{
            background-color: {theme['accent']};
            border-color: {theme['accent']};
        }}
        QMenuBar {{
            background-color: {theme['bg_secondary']};
            color: {theme['text_primary']};
            border-bottom: 1px solid {theme['border']};
        }}
        QMenuBar::item:selected {{
            background-color: {theme['accent']};
            color: {theme['bg_primary']};
        }}
        QMenu {{
            background-color: {theme['bg_secondary']};
            color: {theme['text_primary']};
            border: 1px solid {theme['border']};
            border-radius: 8px;
        }}
        QMenu::item:selected {{
            background-color: {theme['accent']};
            color: {theme['bg_primary']};
        }}
        """


class MainWindow(QMainWindow):
    """Cửa sổ chính của ứng dụng"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.theme_manager = ThemeManager()
        self.results = []
        self.init_ui()
        self.apply_theme("dark")
        
    def init_ui(self):
        self.setWindowTitle(f"Facebook Token & Cookie Extractor Pro v{VERSION}")
        self.setGeometry(100, 100, 1200, 750)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Top bar
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)
        
        # Main content
        content_layout = QHBoxLayout()
        content_layout.setSpacing(15)
        
        left_panel = self.create_left_panel()
        content_layout.addWidget(left_panel, 3)
        
        right_panel = self.create_right_panel()
        content_layout.addWidget(right_panel, 7)
        
        main_layout.addLayout(content_layout)
        
        # Status bar
        self.status_bar = self.create_status_bar()
        main_layout.addWidget(self.status_bar)
        
        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_status_time)
        self.timer.start(1000)
        
    def create_top_bar(self):
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0f3460, stop:1 #1a1a2e);
                border-radius: 12px;
                padding: 10px;
            }
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(15, 10, 15, 10)
        
        logo_label = QLabel("🎯 FB Extractor Pro")
        logo_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #64ffda;")
        layout.addWidget(logo_label)
        
        layout.addStretch()
        
        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("color: #a8b2d1;")
        layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(self.theme_manager.THEMES.keys())
        self.theme_combo.currentTextChanged.connect(self.apply_theme)
        self.theme_combo.setStyleSheet("""
            QComboBox {
                background-color: #1a1a2e;
                color: white;
                border: 1px solid #2a2a4a;
                border-radius: 6px;
                padding: 5px 10px;
                min-width: 100px;
            }
        """)
        layout.addWidget(self.theme_combo)
        
        version_label = QLabel(f"v{VERSION}")
        version_label.setStyleSheet("color: #a8b2d1; font-size: 11px;")
        layout.addWidget(version_label)
        
        return widget
        
    def create_left_panel(self):
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(15)
        
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                background-color: #1a1a2e;
                border-radius: 8px;
                padding: 10px;
            }
            QTabBar::tab {
                padding: 8px 15px;
                border-radius: 6px 6px 0 0;
                background-color: #0f3460;
                color: #a8b2d1;
            }
            QTabBar::tab:selected {
                background-color: #64ffda;
                color: #1a1a2e;
            }
        """)
        
        single_tab = self.create_single_tab()
        tabs.addTab(single_tab, "🎯 Đơn lẻ")
        
        batch_tab = self.create_batch_tab()
        tabs.addTab(batch_tab, "📁 Hàng loạt")
        
        layout.addWidget(tabs)
        
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("▶ Bắt đầu")
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #00d05a;
                color: white;
                font-size: 14px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #00e86b;
            }
        """)
        self.start_btn.clicked.connect(self.start_processing)
        control_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Dừng")
        self.stop_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4757;
                color: white;
                font-size: 14px;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #ff6b81;
            }
        """)
        self.stop_btn.clicked.connect(self.stop_processing)
        self.stop_btn.setEnabled(False)
        control_layout.addWidget(self.stop_btn)
        
        layout.addLayout(control_layout)
        
        progress_layout = QVBoxLayout()
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                background-color: #1a1a2e;
                border: 1px solid #2a2a4a;
                border-radius: 8px;
                height: 25px;
                text-align: center;
                color: white;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #64ffda, stop:1 #4a9eff);
                border-radius: 8px;
            }
        """)
        progress_layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Sẵn sàng")
        self.status_label.setStyleSheet("color: #a8b2d1; font-size: 12px;")
        self.status_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(self.status_label)
        
        layout.addLayout(progress_layout)
        
        return widget
        
    def create_single_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        
        layout.addWidget(QLabel("📧 Email/SĐT/UID:"))
        self.single_email = QLineEdit()
        self.single_email.setPlaceholderText("example@gmail.com hoặc số điện thoại")
        layout.addWidget(self.single_email)
        
        layout.addWidget(QLabel("🔑 Mật khẩu:"))
        self.single_password = QLineEdit()
        self.single_password.setPlaceholderText("Nhập mật khẩu")
        self.single_password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.single_password)
        
        layout.addWidget(QLabel("🔐 Mã 2FA (để trống nếu không có):"))
        self.single_2fa = QLineEdit()
        self.single_2fa.setPlaceholderText("Mã bí mật 2FA")
        layout.addWidget(self.single_2fa)
        
        self.show_pass = QCheckBox("Hiển thị mật khẩu")
        self.show_pass.stateChanged.connect(self.toggle_password_visibility)
        layout.addWidget(self.show_pass)
        
        layout.addStretch()
        
        return widget
        
    def create_batch_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(12)
        
        info_label = QLabel("📌 Nhập danh sách tài khoản theo định dạng:")
        info_label.setStyleSheet("color: #64ffda; font-weight: bold;")
        layout.addWidget(info_label)
        
        format_label = QLabel("user|password|2fa (mỗi dòng một tài khoản)")
        format_label.setStyleSheet("color: #a8b2d1; font-style: italic;")
        layout.addWidget(format_label)
        
        self.batch_input = QPlainTextEdit()
        self.batch_input.setPlaceholderText("""
example@gmail.com|password123|G4G7Z6SNWUTLTTV7
user2@gmail.com|pass456|
user3@yahoo.com|pass789|SECRET_KEY_HERE
        """.strip())
        self.batch_input.setFont(QFont("Consolas", 10))
        self.batch_input.textChanged.connect(self.update_account_count)
        layout.addWidget(self.batch_input)
        
        load_btn = QPushButton("📂 Tải từ file data.txt")
        load_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #6ab0ff;
            }
        """)
        load_btn.clicked.connect(self.load_from_file)
        layout.addWidget(load_btn)
        
        thread_layout = QHBoxLayout()
        thread_layout.addWidget(QLabel("⚡ Số luồng:"))
        self.thread_count = QSpinBox()
        self.thread_count.setRange(1, 20)
        self.thread_count.setValue(5)
        self.thread_count.setStyleSheet("""
            QSpinBox {
                background-color: #1a1a2e;
                color: white;
                border: 1px solid #2a2a4a;
                border-radius: 6px;
                padding: 5px;
                min-width: 60px;
            }
        """)
        thread_layout.addWidget(self.thread_count)
        thread_layout.addStretch()
        layout.addLayout(thread_layout)
        
        self.account_count = QLabel("Tổng: 0 tài khoản")
        self.account_count.setStyleSheet("color: #a8b2d1;")
        layout.addWidget(self.account_count)
        
        return widget
        
    def create_right_panel(self):
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        
        tabs = QTabWidget()
        tabs.setStyleSheet("""
            QTabWidget::pane {
                background-color: #1a1a2e;
                border-radius: 8px;
                padding: 5px;
            }
            QTabBar::tab {
                padding: 8px 15px;
                border-radius: 6px 6px 0 0;
                background-color: #0f3460;
                color: #a8b2d1;
            }
            QTabBar::tab:selected {
                background-color: #64ffda;
                color: #1a1a2e;
            }
        """)
        
        results_tab = self.create_results_tab()
        tabs.addTab(results_tab, "📊 Kết quả")
        
        log_tab = self.create_log_tab()
        tabs.addTab(log_tab, "📝 Log")
        
        layout.addWidget(tabs)
        
        return widget
        
    def create_results_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.results_table = QTableWidget()
        self.results_table.setColumnCount(4)
        self.results_table.setHorizontalHeaderLabels(["UID", "Tên", "Trạng thái", "Thông tin"])
        self.results_table.horizontalHeader().setStretchLastSection(True)
        self.results_table.setAlternatingRowColors(True)
        self.results_table.setStyleSheet("""
            QTableWidget {
                background-color: #1a1a2e;
                border: none;
                gridline-color: #2a2a4a;
            }
            QTableWidget::item {
                padding: 8px;
                color: white;
            }
            QTableWidget::item:selected {
                background-color: #64ffda;
                color: #1a1a2e;
            }
            QHeaderView::section {
                background-color: #0f3460;
                color: #a8b2d1;
                padding: 8px;
                border: none;
            }
        """)
        layout.addWidget(self.results_table)
        
        export_btn = QPushButton("💾 Export kết quả")
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: #4a9eff;
                color: white;
                padding: 8px;
            }
            QPushButton:hover {
                background-color: #6ab0ff;
            }
        """)
        export_btn.clicked.connect(self.export_results)
        layout.addWidget(export_btn)
        
        return widget
        
    def create_log_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(5, 5, 5, 5)
        
        self.log_widget = LogWidget()
        layout.addWidget(self.log_widget)
        
        log_controls = QHBoxLayout()
        
        clear_btn = QPushButton("🗑 Xóa log")
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #ff4757;
                color: white;
                padding: 5px 15px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #ff6b81;
            }
        """)
        clear_btn.clicked.connect(self.log_widget.clear)
        log_controls.addWidget(clear_btn)
        
        log_controls.addStretch()
        
        auto_scroll = QCheckBox("Tự động cuộn")
        auto_scroll.setChecked(True)
        auto_scroll.setStyleSheet("color: #a8b2d1;")
        auto_scroll.stateChanged.connect(lambda state: self.log_widget.set_auto_scroll(state == Qt.Checked))
        log_controls.addWidget(auto_scroll)
        
        layout.addLayout(log_controls)
        
        return widget
        
    def create_status_bar(self):
        widget = QFrame()
        widget.setStyleSheet("""
            QFrame {
                background-color: #16213e;
                border-radius: 8px;
                padding: 8px 15px;
            }
        """)
        
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 5, 10, 5)
        
        self.status_icon = QLabel("🟢")
        layout.addWidget(self.status_icon)
        
        self.status_text = QLabel("Sẵn sàng")
        self.status_text.setStyleSheet("color: #a8b2d1; font-weight: bold;")
        layout.addWidget(self.status_text)
        
        layout.addStretch()
        
        self.stats_label = QLabel("📊 0 thành công | 0 thất bại")
        self.stats_label.setStyleSheet("color: #a8b2d1;")
        layout.addWidget(self.stats_label)
        
        layout.addStretch()
        
        self.time_label = QLabel(datetime.now().strftime("%H:%M:%S"))
        self.time_label.setStyleSheet("color: #a8b2d1; font-family: monospace;")
        layout.addWidget(self.time_label)
        
        return widget
    
    # ===== CÁC PHƯƠNG THỨC CHỨC NĂNG =====
    
    def apply_theme(self, theme_name):
        style = self.theme_manager.get_style(theme_name)
        self.setStyleSheet(style)
        
    def toggle_password_visibility(self, state):
        if state == Qt.Checked:
            self.single_password.setEchoMode(QLineEdit.Normal)
        else:
            self.single_password.setEchoMode(QLineEdit.Password)
            
    def update_status_time(self):
        self.time_label.setText(datetime.now().strftime("%H:%M:%S"))
        
    def load_from_file(self):
        if not os.path.exists("data.txt"):
            QMessageBox.warning(self, "Thông báo", 
                "Không tìm thấy file data.txt!\nVui lòng tạo file với định dạng:\nuser|password|2fa")
            return
            
        try:
            with open("data.txt", "r", encoding="utf-8") as f:
                content = f.read()
            self.batch_input.setPlainText(content)
            self.update_account_count()
            self.log_widget.append_log("📂 Đã tải danh sách từ data.txt", "info")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể đọc file: {str(e)}")
            
    def update_account_count(self):
        accounts = self.parse_batch_input()
        self.account_count.setText(f"Tổng: {len(accounts)} tài khoản")
        
    def parse_batch_input(self):
        text = self.batch_input.toPlainText()
        accounts = []
        for line in text.strip().split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('|')
                if len(parts) >= 2:
                    uid = parts[0].strip()
                    pwd = parts[1].strip()
                    fa2 = parts[2].strip() if len(parts) > 2 else ""
                    if uid and pwd:
                        accounts.append((uid, pwd, fa2))
        return accounts
        
    def start_processing(self):
        if self.worker and hasattr(self.worker, 'is_running') and self.worker.is_running:
            return
            
        accounts = []
        tabs = self.centralWidget().findChildren(QTabWidget)[0]
        current_index = tabs.currentIndex()
        
        if current_index == 0:
            uid = self.single_email.text().strip()
            pwd = self.single_password.text().strip()
            fa2 = self.single_2fa.text().strip().replace(" ", "")
            
            if not uid or not pwd:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập đầy đủ Email và Mật khẩu!")
                return
            accounts = [(uid, pwd, fa2)]
            max_workers = 1
        else:
            accounts = self.parse_batch_input()
            if not accounts:
                QMessageBox.warning(self, "Lỗi", "Không có tài khoản hợp lệ!\nĐịnh dạng: user|password|2fa")
                return
            max_workers = self.thread_count.value()
        
        self.results_table.setRowCount(0)
        self.results = []
        
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.progress_bar.setMaximum(len(accounts))
        self.progress_bar.setValue(0)
        self.status_label.setText(f"🔄 Đang xử lý: 0/{len(accounts)}")
        self.status_text.setText("Đang xử lý...")
        self.status_icon.setText("🟡")
        
        self.worker = Worker(accounts, max_workers)
        self.worker.signals.log.connect(self.log_widget.append_log)
        self.worker.signals.progress.connect(self.update_progress)
        self.worker.signals.finished.connect(self.on_processing_finished)
        self.worker.signals.account_done.connect(self.add_account_result)
        
        thread_pool = QThreadPool.globalInstance()
        thread_pool.start(self.worker)
        
        self.log_widget.append_log(f"🚀 Bắt đầu xử lý {len(accounts)} tài khoản...", "info")
        
    def stop_processing(self):
        if self.worker:
            self.worker.stop()
            self.log_widget.append_log("⏹ Đang dừng xử lý...", "warning")
            self.status_text.setText("Đang dừng...")
            self.status_icon.setText("🔴")
            
    def update_progress(self, current, total):
        self.progress_bar.setValue(current)
        self.status_label.setText(f"🔄 Đang xử lý: {current}/{total}")
        
    def add_account_result(self, uid, success, message):
        row = self.results_table.rowCount()
        self.results_table.insertRow(row)
        
        self.results_table.setItem(row, 0, QTableWidgetItem(uid))
        if success:
            self.results_table.setItem(row, 1, QTableWidgetItem(message))
        else:
            self.results_table.setItem(row, 1, QTableWidgetItem(""))
        self.results_table.setItem(row, 2, QTableWidgetItem("✅ Thành công" if success else "❌ Thất bại"))
        self.results_table.setItem(row, 3, QTableWidgetItem(message[:50] if not success else ""))
        
        if success:
            self.results_table.item(row, 2).setForeground(QColor("#00d05a"))
        else:
            self.results_table.item(row, 2).setForeground(QColor("#ff4757"))
            
        success_count = sum(1 for i in range(self.results_table.rowCount()) 
                          if "Thành công" in self.results_table.item(i, 2).text())
        fail_count = self.results_table.rowCount() - success_count
        self.stats_label.setText(f"📊 {success_count} thành công | {fail_count} thất bại")
        
    def on_processing_finished(self):
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_text.setText("Hoàn tất")
        self.status_icon.setText("🟢")
        self.progress_bar.setValue(self.progress_bar.maximum())
        
        success_count = sum(1 for i in range(self.results_table.rowCount()) 
                          if "Thành công" in self.results_table.item(i, 2).text())
        total = self.results_table.rowCount()
        
        self.status_label.setText(f"✅ Hoàn tất! {success_count}/{total} thành công")
        self.log_widget.append_log(f"✅ Hoàn tất! {success_count}/{total} thành công", "success")
        
    def export_results(self):
        if self.results_table.rowCount() == 0:
            QMessageBox.information(self, "Thông báo", "Chưa có kết quả để export!")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Lưu kết quả", "results.txt", "Text Files (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write("=" * 60 + "\n")
                    f.write("FACEBOOK TOKEN EXTRACTOR - RESULTS\n")
                    f.write(f"Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("=" * 60 + "\n\n")
                    
                    for i in range(self.results_table.rowCount()):
                        uid = self.results_table.item(i, 0).text()
                        status = self.results_table.item(i, 2).text()
                        info = self.results_table.item(i, 3).text()
                        f.write(f"{uid} | {status} | {info}\n")
                        
                QMessageBox.information(self, "Thành công", f"Đã lưu kết quả vào:\n{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể lưu file: {str(e)}")


# ===================================================================
# MAIN
# ===================================================================

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()