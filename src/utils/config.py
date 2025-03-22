import os
import json

CONFIG_FILE = 'config/settings.json'

DEFAULT_CONFIG = {
    'download_path': os.path.expanduser('~/Downloads'),
    'max_speed': 0,  # 0 means unlimited
    'concurrent_downloads': 3,
    'language': 'العربية',
    'auto_start_downloads': True,
    'show_notifications': True,
    'theme': 'light'
}

def get_config():
    """الحصول على إعدادات البرنامج"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return {**DEFAULT_CONFIG, **json.load(f)}
    return DEFAULT_CONFIG

def save_config(config):
    """حفظ إعدادات البرنامج"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=4)

def update_config(key, value):
    """تحديث قيمة في الإعدادات"""
    config = get_config()
    config[key] = value
    save_config(config)
