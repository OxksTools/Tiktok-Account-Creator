

import requests
import SignerPy 

def xor(string):
    """Simple XOR encryption for email and password"""
    return "".join([hex(ord(c) ^ 5)[2:] for c in string])

class TikTokAccountCreator:
    def __init__(self):
        self.client = requests.session()
        self.cookies = {
            "tt-target-idc": "eu-ttp2",
            "store-country-code": "fr",
        }
        self.client.cookies.update(self.cookies)
        self.base_params = {
            "passport-sdk-version": "6031990",
            "device_platform": "android",
        }

    def send_verification_code(self, email):
        """Send verification code to email"""
        url = "https://api16-normal-no1a.tiktokv.eu/passport/email/send_code/"
        params = self.base_params.copy()
        params.update({
            "_rticket": "1752961596612",
            "ts": "1752961596",
        })
        
        payload = {
            'account_sdk_source': "app",
            'rule_strategies': "2",
            'mix_mode': "1",
            'multi_login': "1",
            'type': "3732",
            'email': xor(email),
            'email_theme': "2"
        }
        
        # Generate signatures
        m = SignerPy.sign(params=params, cookie=self.cookies, payload=payload)
        
        headers = {
            'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_GB; SM-S908E; Build/TP1A.220624.014;tt-ok/3.12.13.16)",
            'x-ladon': m['x-ladon'],
            'x-khronos': m['x-khronos'],
            'x-argus': m['x-argus'],
            'x-gorgon': m['x-gorgon']
        }
        
        response = self.client.post(url, data=payload, headers=headers, params=params)
        print(response.text)
        return response.json()

    def set_password(self, password):
        """Set account password"""
        url = "https://api32-normal-no1a.tiktokv.eu/passport/password/set/"
        params = self.base_params.copy()
        params.update({
            "_rticket": "1752961649155",
            "ts": "1752961648",
        })
        
        payload = {
            'rules_version': "v2",
            'password': xor(password),
            'account_sdk_source': "app",
            'multi_login': "1",
            'mix_mode': "1"
        }
        
        m = SignerPy.sign(params=params, cookie=self.cookies, payload=payload)
        
        headers = {
            'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_GB; SM-S908E; Build/TP1A.220624.014;tt-ok/3.12.13.16)",
            'x-ladon': m['x-ladon'],
            'x-khronos': m['x-khronos'],
            'x-argus': m['x-argus'],
            'x-gorgon': m['x-gorgon']
        }
        
        response = self.client.post(url, data=payload, headers=headers, params=params)
        return response.json()

    def verify_code_and_register(self, email, code):
        """Verify code and complete registration"""
        url = "https://api16-normal-no1a.tiktokv.eu/passport/email/register_verify_login/"
        params = self.base_params.copy()
        params.update({
            "_rticket": "1752961618176",
            "ts": "1752961617",
        })
        
        payload = {
            'birthday': "1996-12-10",
            'fixed_mix_mode': "1",
            'code': xor(code),
            'account_sdk_source': "app",
            'mix_mode': "1",
            'multi_login': "1",
            'type': "3732",
            'email': xor(email)
        }
        
        m = SignerPy.sign(params=params, cookie=self.cookies, payload=payload)
        
        headers = {
            'User-Agent': "com.zhiliaoapp.musically/2023708050 (Linux; U; Android 9; en_GB; SM-S908E; Build/TP1A.220624.014;tt-ok/3.12.13.16)",
            'x-ladon': m['x-ladon'],
            'x-khronos': m['x-khronos'],
            'x-argus': m['x-argus'],
            'x-gorgon': m['x-gorgon']
        }
        
        response = self.client.post(url, data=payload, headers=headers, params=params)
        return response.json()

if __name__ == "__main__":
    creator = TikTokAccountCreator()
    
    try:
        email = input("Enter email: ")
        print("Sending verification code...")
        send_result = creator.send_verification_code(email)
        print(send_result)
        
        # Step 2: Set password
        password = input("Enter password: ")
        print("Setting password...")
        password_result = creator.set_password(password)
        print(password_result)
        
        code = input("Enter verification code: ")
        print("Completing registration...")
        register_result = creator.verify_code_and_register(email, code)
        print(register_result)
        
        try:
            sessionid = register_result["data"]["session_key"]
            print(f"Account created successfully! Session ID: {sessionid}")
        except KeyError:
            print("IP may be blocked or verification failed")
            
    except Exception as e:
        print(f"An error occurred: {str(e)}")
