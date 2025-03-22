from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QDateTimeEdit, QLineEdit, QFormLayout)
from PyQt5.QtCore import Qt, QDateTime
from ..core.advanced_features import AdvancedFeatures

class ScheduleDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("جدولة التحميل")
        self.setModal(True)
        self.advanced = AdvancedFeatures()
        self.init_ui()
        
    def init_ui(self):
        layout = QFormLayout()
        
        # رابط التحميل
        self.url = QLineEdit()
        layout.addRow("الرابط:", self.url)
        
        # مجلد الحفظ
        self.save_path = QLineEdit()
        browse_btn = QPushButton("تصفح")
        browse_btn.clicked.connect(self.browse_save_path)
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.save_path)
        path_layout.addWidget(browse_btn)
        layout.addRow("مجلد الحفظ:", path_layout)
        
        # وقت التحميل
        self.schedule_time = QDateTimeEdit()
        self.schedule_time.setDateTime(QDateTime.currentDateTime())
        self.schedule_time.setCalendarPopup(True)
        layout.addRow("وقت التحميل:", self.schedule_time)
        
        # أزرار
        buttons = QHBoxLayout()
        schedule_btn = QPushButton("جدولة")
        cancel_btn = QPushButton("إلغاء")
        
        schedule_btn.clicked.connect(self.schedule_download)
        cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(schedule_btn)
        buttons.addWidget(cancel_btn)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addLayout(buttons)
        
        self.setLayout(main_layout)
    
    def browse_save_path(self):
        from PyQt5.QtWidgets import QFileDialog
        path = QFileDialog.getExistingDirectory(
            self,
            "اختر مجلد الحفظ",
            ""
        )
        if path:
            self.save_path.setText(path)
    
    def schedule_download(self):
        url = self.url.text()
        save_path = self.save_path.text()
        schedule_time = self.schedule_time.dateTime().toPyDateTime()
        
        if url and save_path:
            try:
                job_id = self.advanced.schedule_download(url, save_path, schedule_time)
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(
                    self,
                    "تمت الجدولة",
                    f"تم جدولة التحميل في {schedule_time}"
                )
                self.accept()
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "خطأ",
                    f"حدث خطأ أثناء جدولة التحميل: {str(e)}"
                )
        else:
            QMessageBox.warning(
                self,
                "خطأ",
                "يرجى ملء جميع الحقول المطلوبة"
            )
