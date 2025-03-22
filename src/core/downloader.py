import aiohttp
import asyncio
import os
from tqdm import tqdm
from ..utils.config import get_config

class Downloader:
    def __init__(self):
        self.config = get_config()
        self.active_downloads = {}
        self.download_queue = asyncio.Queue()
        
    async def add_download(self, url, filename=None):
        """إضافة تحميل جديد إلى قائمة الانتظار"""
        if not filename:
            filename = url.split('/')[-1]
            
        download_path = os.path.join(self.config['download_path'], filename)
        await self.download_queue.put((url, download_path))
        
    async def start_download_worker(self):
        """بدء عامل التحميل"""
        while True:
            url, path = await self.download_queue.get()
            try:
                await self.download_file(url, path)
            except Exception as e:
                print(f"خطأ في تحميل {url}: {str(e)}")
            finally:
                self.download_queue.task_done()
                
    async def download_file(self, url, destination, chunk_size=8192):
        """تحميل ملف من URL"""
        temp_file = f"{destination}.part"
        
        headers = {}
        if os.path.exists(temp_file):
            file_size = os.path.getsize(temp_file)
            headers['Range'] = f'bytes={file_size}-'
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                total_size = int(response.headers.get('content-length', 0))
                
                if os.path.exists(temp_file):
                    mode = 'ab'
                    initial_size = os.path.getsize(temp_file)
                    total_size += initial_size
                else:
                    mode = 'wb'
                    initial_size = 0
                
                with open(temp_file, mode) as f:
                    with tqdm(
                        total=total_size,
                        initial=initial_size,
                        unit='B',
                        unit_scale=True,
                        desc=os.path.basename(destination)
                    ) as pbar:
                        async for chunk in response.content.iter_chunked(chunk_size):
                            f.write(chunk)
                            pbar.update(len(chunk))
                            
        # بعد اكتمال التحميل، نقوم بتغيير اسم الملف
        os.rename(temp_file, destination)
        
    def get_download_progress(self, url):
        """الحصول على تقدم التحميل"""
        if url in self.active_downloads:
            return self.active_downloads[url]
        return None
        
    def pause_download(self, url):
        """إيقاف التحميل مؤقتاً"""
        # TODO: تنفيذ إيقاف مؤقت للتحميل
        pass
        
    def resume_download(self, url):
        """استئناف التحميل"""
        # TODO: تنفيذ استئناف التحميل
        pass
        
    def cancel_download(self, url):
        """إلغاء التحميل"""
        # TODO: تنفيذ إلغاء التحميل
        pass
