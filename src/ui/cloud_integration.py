from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QPushButton, QLabel, 
                           QProgressBar, QMessageBox, QGroupBox)
from PyQt5.QtCore import Qt
from ..core.cloud_manager import CloudManager

class CloudIntegration(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("إدارة حسابات السحابة")
        self.setModal(True)
        self.cloud_manager = CloudManager()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Google Drive
        gdrive_group = QGroupBox("Google Drive")
        gdrive_layout = QVBoxLayout()
        
        self.gdrive_status = QLabel("غير متصل")
        self.gdrive_btn = QPushButton("ربط الحساب")
        self.gdrive_btn.clicked.connect(self.connect_google_drive)
        self.gdrive_space = QProgressBar()
        
        gdrive_layout.addWidget(self.gdrive_status)
        gdrive_layout.addWidget(self.gdrive_btn)
        gdrive_layout.addWidget(self.gdrive_space)
        gdrive_group.setLayout(gdrive_layout)

        # Dropbox
        dropbox_group = QGroupBox("Dropbox")
        dropbox_layout = QVBoxLayout()
        
        self.dropbox_status = QLabel("غير متصل")
        self.dropbox_btn = QPushButton("ربط الحساب")
        self.dropbox_btn.clicked.connect(self.connect_dropbox)
        self.dropbox_space = QProgressBar()
        
        dropbox_layout.addWidget(self.dropbox_status)
        dropbox_layout.addWidget(self.dropbox_btn)
        dropbox_layout.addWidget(self.dropbox_space)
        dropbox_group.setLayout(dropbox_layout)

        # إضافة المجموعات إلى التخطيط الرئيسي
        layout.addWidget(gdrive_group)
        layout.addWidget(dropbox_group)
        
        self.setLayout(layout)

    def connect_google_drive(self):
        try:
            if self.cloud_manager.connect_gdrive():
                self.gdrive_status.setText("متصل")
                self.update_storage_info()
                QMessageBox.information(self, "نجاح", "تم الاتصال بنجاح مع Google Drive")
        except Exception as e:
            QMessageBox.warning(self, "خطأ", str(e))

    def connect_dropbox(self):
        try:
            if self.cloud_manager.connect_dropbox():
                self.dropbox_status.setText("متصل")
                self.update_storage_info()
                QMessageBox.information(self, "نجاح", "تم الاتصال بنجاح مع Dropbox")
        except Exception as e:
            QMessageBox.warning(self, "خطأ", str(e))

    def update_storage_info(self):
        # تحديث معلومات المساحة المتوفرة
        gdrive_info = self.cloud_manager.get_gdrive_storage_info()
        dropbox_info = self.cloud_manager.get_dropbox_storage_info()
        
        if gdrive_info:
            used, total = gdrive_info
            self.gdrive_space.setValue(int(used/total * 100))
            
        if dropbox_info:
            used, total = dropbox_info
            self.dropbox_space.setValue(int(used/total * 100))
