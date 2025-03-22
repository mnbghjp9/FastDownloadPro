from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import dropbox
import os
import json

class CloudManager:
    def __init__(self):
        self.gdrive_service = None
        self.dropbox_client = None
        self.config_dir = 'config'
        os.makedirs(self.config_dir, exist_ok=True)
        
    def connect_gdrive(self):
        """ربط حساب Google Drive"""
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        creds = None
        token_path = os.path.join(self.config_dir, 'gdrive_token.json')
        
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
            
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                
            with open(token_path, 'w') as token:
                token.write(creds.to_json())
                
        self.gdrive_service = build('drive', 'v3', credentials=creds)
        return True
        
    def connect_dropbox(self):
        """ربط حساب Dropbox"""
        APP_KEY = 'your-app-key'
        APP_SECRET = 'your-app-secret'
        
        auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
        authorize_url = auth_flow.start()
        print(f"1. افتح هذا الرابط: {authorize_url}")
        print("2. اضغط 'السماح' (قد تحتاج إلى تسجيل الدخول أولاً)")
        print("3. انسخ رمز التفويض")
        auth_code = input("أدخل رمز التفويض هنا: ").strip()
        
        try:
            oauth_result = auth_flow.finish(auth_code)
            self.dropbox_client = dropbox.Dropbox(oauth_result.access_token)
            
            # حفظ التوكن للاستخدام المستقبلي
            token_path = os.path.join(self.config_dir, 'dropbox_token.json')
            with open(token_path, 'w') as f:
                json.dump({'access_token': oauth_result.access_token}, f)
                
            return True
        except Exception as e:
            print(f"خطأ في الاتصال مع Dropbox: {str(e)}")
            return False
            
    def upload_to_gdrive(self, file_path):
        """رفع ملف إلى Google Drive"""
        if not self.gdrive_service:
            raise Exception("يرجى الاتصال بـ Google Drive أولاً")
            
        file_metadata = {'name': os.path.basename(file_path)}
        # TODO: تنفيذ رفع الملف
        
    def upload_to_dropbox(self, file_path):
        """رفع ملف إلى Dropbox"""
        if not self.dropbox_client:
            raise Exception("يرجى الاتصال بـ Dropbox أولاً")
            
        with open(file_path, 'rb') as f:
            # TODO: تنفيذ رفع الملف
            pass
            
    def get_gdrive_storage_info(self):
        """الحصول على معلومات المساحة في Google Drive"""
        if not self.gdrive_service:
            return None
            
        about = self.gdrive_service.about().get(fields="storageQuota").execute()
        quota = about.get('storageQuota', {})
        used = int(quota.get('usage', 0))
        total = int(quota.get('limit', 0))
        return used, total
        
    def get_dropbox_storage_info(self):
        """الحصول على معلومات المساحة في Dropbox"""
        if not self.dropbox_client:
            return None
            
        space = self.dropbox_client.users_get_space_usage()
        used = space.used
        total = space.allocation.get_individual().allocated
        return used, total
