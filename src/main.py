import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import DownloadManager

def main():
    app = QApplication(sys.argv)
    
    # تطبيق ملف الستايل
    with open('src/ui/styles.qss', 'r') as f:
        app.setStyleSheet(f.read())
    
    window = DownloadManager()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
