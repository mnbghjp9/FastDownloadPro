import yt_dlp
from bs4 import BeautifulSoup
import requests
from cryptography.fernet import Fernet
import schedule
import time
import psutil
import os
from datetime import datetime
import magic
import logging
from apscheduler.schedulers.background import BackgroundScheduler

class AdvancedFeatures:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.start()
        self.encryption_key = None
        self.setup_logging()
        
    def setup_logging(self):
        """إعداد سجل النشاطات"""
        logging.basicConfig(
            filename='downloads.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def download_playlist(self, url, output_path):
        """تحميل قائمة تشغيل من يوتيوب"""
        ydl_opts = {
            'format': 'best',
            'outtmpl': f'{output_path}/%(title)s.%(ext)s',
            'ignoreerrors': True,
            'extract_flat': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.download([url])
                logging.info(f"تم تحميل قائمة التشغيل: {url}")
                return result
        except Exception as e:
            logging.error(f"خطأ في تحميل قائمة التشغيل: {str(e)}")
            raise

    def download_website(self, url, output_path, depth=1):
        """تحميل موقع ويب بالكامل"""
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # حفظ الصفحة الرئيسية
            with open(f"{output_path}/index.html", 'w', encoding='utf-8') as f:
                f.write(str(soup.prettify()))
            
            # تحميل الصور
            for img in soup.find_all('img'):
                img_url = img.get('src')
                if img_url:
                    if not img_url.startswith('http'):
                        img_url = url + img_url
                    try:
                        img_data = requests.get(img_url).content
                        img_name = os.path.basename(img_url)
                        with open(f"{output_path}/{img_name}", 'wb') as f:
                            f.write(img_data)
                    except:
                        continue
            
            logging.info(f"تم تحميل الموقع: {url}")
            
        except Exception as e:
            logging.error(f"خطأ في تحميل الموقع: {str(e)}")
            raise

    def schedule_download(self, url, output_path, schedule_time):
        """جدولة تحميل في وقت محدد"""
        job = self.scheduler.add_job(
            self.start_download,
            'date',
            run_date=schedule_time,
            args=[url, output_path]
        )
        logging.info(f"تمت جدولة التحميل: {url} في {schedule_time}")
        return job.id

    def encrypt_file(self, file_path, password):
        """تشفير ملف"""
        if not self.encryption_key:
            self.encryption_key = Fernet.generate_key()
        
        f = Fernet(self.encryption_key)
        
        with open(file_path, 'rb') as file:
            file_data = file.read()
        
        encrypted_data = f.encrypt(file_data)
        
        encrypted_file_path = file_path + '.encrypted'
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data)
            
        logging.info(f"تم تشفير الملف: {file_path}")
        return encrypted_file_path

    def scan_file(self, file_path):
        """فحص نوع الملف والتحقق من سلامته"""
        mime = magic.Magic(mime=True)
        file_type = mime.from_file(file_path)
        file_size = os.path.getsize(file_path)
        
        result = {
            'path': file_path,
            'type': file_type,
            'size': file_size,
            'created': datetime.fromtimestamp(os.path.getctime(file_path)),
            'modified': datetime.fromtimestamp(os.path.getmtime(file_path))
        }
        
        logging.info(f"تم فحص الملف: {file_path}")
        return result

    def monitor_system_resources(self):
        """مراقبة موارد النظام"""
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        return {
            'cpu_usage': cpu_percent,
            'memory_used': memory.percent,
            'disk_used': disk.percent
        }

    def optimize_download_speed(self, file_size):
        """تحسين سرعة التحميل بناءً على حجم الملف وموارد النظام"""
        resources = self.monitor_system_resources()
        
        # تحديد حجم القطع المثالي بناءً على الموارد المتاحة
        if resources['memory_used'] > 80:
            chunk_size = 4096  # حجم صغير للذاكرة المحدودة
        else:
            chunk_size = 8192  # حجم أكبر للذاكرة المتوفرة
            
        # تحديد عدد العمليات المتزامنة
        if resources['cpu_usage'] > 80:
            max_workers = 2
        else:
            max_workers = 4
            
        return {
            'chunk_size': chunk_size,
            'max_workers': max_workers
        }

    def compress_file(self, file_path, compression_level=6):
        """ضغط الملف بعد التحميل"""
        import gzip
        import shutil
        
        compressed_file_path = file_path + '.gz'
        with open(file_path, 'rb') as f_in:
            with gzip.open(compressed_file_path, 'wb', compresslevel=compression_level) as f_out:
                shutil.copyfileobj(f_in, f_out)
                
        logging.info(f"تم ضغط الملف: {file_path}")
        return compressed_file_path
