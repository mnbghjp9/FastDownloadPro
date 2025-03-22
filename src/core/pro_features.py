import os
import subprocess
import qbittorrent
import requests
import socks
import socket
from moviepy.editor import VideoFileClip
from PIL import Image
import threading
from concurrent.futures import ThreadPoolExecutor

class ProFeatures:
    def __init__(self):
        self.proxy_enabled = False
        self.torrent_client = None
        self.max_threads = 4
        
    def setup_proxy(self, proxy_type, host, port, username=None, password=None):
        """إعداد البروكسي"""
        if proxy_type.lower() == 'socks5':
            socks.set_default_proxy(socks.SOCKS5, host, port, username=username, password=password)
        elif proxy_type.lower() == 'socks4':
            socks.set_default_proxy(socks.SOCKS4, host, port)
        elif proxy_type.lower() == 'http':
            socks.set_default_proxy(socks.HTTP, host, port)
            
        socket.socket = socks.socksocket
        self.proxy_enabled = True
        
    def disable_proxy(self):
        """تعطيل البروكسي"""
        socket.socket = socket.socket
        self.proxy_enabled = False
        
    def setup_torrent(self, host='localhost', port=8080):
        """إعداد عميل التورنت"""
        self.torrent_client = qbittorrent.Client(f'http://{host}:{port}/')
        
    def add_torrent(self, torrent_path):
        """إضافة ملف تورنت"""
        if not self.torrent_client:
            raise Exception("يجب إعداد عميل التورنت أولاً")
        self.torrent_client.download_from_file(torrent_path)
        
    def add_magnet(self, magnet_link):
        """إضافة رابط ماغنت"""
        if not self.torrent_client:
            raise Exception("يجب إعداد عميل التورنت أولاً")
        self.torrent_client.download_from_link(magnet_link)
        
    def convert_video(self, input_path, output_format):
        """تحويل صيغة الفيديو"""
        output_path = os.path.splitext(input_path)[0] + f'.{output_format}'
        video = VideoFileClip(input_path)
        video.write_videofile(output_path)
        video.close()
        return output_path
        
    def convert_image(self, input_path, output_format):
        """تحويل صيغة الصورة"""
        output_path = os.path.splitext(input_path)[0] + f'.{output_format}'
        image = Image.open(input_path)
        image.save(output_path)
        return output_path
        
    def convert_audio(self, input_path, output_format):
        """تحويل صيغة الصوت"""
        output_path = os.path.splitext(input_path)[0] + f'.{output_format}'
        subprocess.run([
            'ffmpeg', '-i', input_path,
            output_path
        ])
        return output_path
        
    def batch_convert(self, files, output_format):
        """تحويل مجموعة ملفات"""
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            results = []
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in ['.mp4', '.avi', '.mkv', '.mov']:
                    future = executor.submit(self.convert_video, file, output_format)
                elif ext in ['.jpg', '.png', '.bmp', '.gif']:
                    future = executor.submit(self.convert_image, file, output_format)
                elif ext in ['.mp3', '.wav', '.ogg', '.m4a']:
                    future = executor.submit(self.convert_audio, file, output_format)
                results.append(future)
            return [f.result() for f in results]
            
    def optimize_video(self, input_path, quality='medium'):
        """تحسين جودة الفيديو"""
        output_path = os.path.splitext(input_path)[0] + '_optimized.mp4'
        quality_presets = {
            'low': '-crf 28',
            'medium': '-crf 23',
            'high': '-crf 18'
        }
        subprocess.run([
            'ffmpeg', '-i', input_path,
            '-c:v', 'libx264',
            '-preset', 'medium',
            quality_presets.get(quality, '-crf 23'),
            '-c:a', 'aac',
            output_path
        ])
        return output_path
        
    def create_preview(self, input_path, duration=10):
        """إنشاء معاينة للفيديو"""
        output_path = os.path.splitext(input_path)[0] + '_preview.mp4'
        video = VideoFileClip(input_path)
        preview = video.subclip(0, min(duration, video.duration))
        preview.write_videofile(output_path)
        video.close()
        preview.close()
        return output_path
        
    def extract_audio(self, video_path):
        """استخراج الصوت من الفيديو"""
        output_path = os.path.splitext(video_path)[0] + '.mp3'
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(output_path)
        video.close()
        return output_path
        
    def create_gif(self, video_path, start_time=0, duration=3):
        """تحويل جزء من الفيديو إلى GIF"""
        output_path = os.path.splitext(video_path)[0] + '.gif'
        video = VideoFileClip(video_path)
        video.subclip(start_time, start_time + duration).write_gif(output_path)
        video.close()
        return output_path
        
    def merge_videos(self, video_paths, output_path):
        """دمج عدة مقاطع فيديو"""
        clips = [VideoFileClip(path) for path in video_paths]
        final_clip = clips[0].concatenate_videoclips(clips[1:])
        final_clip.write_videofile(output_path)
        for clip in clips:
            clip.close()
        final_clip.close()
        return output_path
