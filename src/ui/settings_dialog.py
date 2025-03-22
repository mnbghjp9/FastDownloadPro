from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
                           QLabel, QSpinBox, QComboBox, QGroupBox, QFormLayout,
                           QLineEdit, QFileDialog, QCheckBox, QTabWidget, QWidget)
from PyQt5.QtCore import Qt

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("الإعدادات")
        self.setModal(True)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # إنشاء تبويبات للإعدادات
        tabs = QTabWidget()
        
        # التبويب الأول: إعدادات عامة
        general_tab = QWidget()
        general_layout = QFormLayout()
        
        # مجلد التحميل
        self.download_path = QLineEdit()
        browse_button = QPushButton("تصفح")
        browse_button.clicked.connect(self.browse_download_path)
        
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.download_path)
        path_layout.addWidget(browse_button)
        
        general_layout.addRow("مجلد التحميل:", path_layout)
        
        # السرعة القصوى
        self.max_speed = QSpinBox()
        self.max_speed.setRange(0, 100000)
        self.max_speed.setSuffix(" KB/s")
        general_layout.addRow("السرعة القصوى:", self.max_speed)
        
        # التحميلات المتزامنة
        self.concurrent_downloads = QSpinBox()
        self.concurrent_downloads.setRange(1, 10)
        general_layout.addRow("التحميلات المتزامنة:", self.concurrent_downloads)
        
        # اللغة
        self.language_combo = QComboBox()
        self.language_combo.addItems(["العربية", "English"])
        general_layout.addRow("اللغة:", self.language_combo)
        
        general_tab.setLayout(general_layout)
        tabs.addTab(general_tab, "عام")
        
        # التبويب الثاني: الأمان والخصوصية
        security_tab = QWidget()
        security_layout = QFormLayout()
        
        # تشفير الملفات
        self.encrypt_files = QCheckBox("تشفير الملفات تلقائياً")
        security_layout.addRow(self.encrypt_files)
        
        # فحص الفيروسات
        self.scan_files = QCheckBox("فحص الملفات بعد التحميل")
        security_layout.addRow(self.scan_files)
        
        # حماية بكلمة مرور
        self.use_password = QCheckBox("تفعيل حماية كلمة المرور")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        security_layout.addRow(self.use_password)
        security_layout.addRow("كلمة المرور:", self.password)
        
        security_tab.setLayout(security_layout)
        tabs.addTab(security_tab, "الأمان")
        
        # التبويب الثالث: الأداء
        performance_tab = QWidget()
        performance_layout = QFormLayout()
        
        # ضغط الملفات
        self.compress_files = QCheckBox("ضغط الملفات تلقائياً")
        performance_layout.addRow(self.compress_files)
        
        # مستوى الضغط
        self.compression_level = QSpinBox()
        self.compression_level.setRange(1, 9)
        self.compression_level.setValue(6)
        performance_layout.addRow("مستوى الضغط:", self.compression_level)
        
        # تحسين الأداء
        self.optimize_performance = QCheckBox("تحسين الأداء تلقائياً")
        performance_layout.addRow(self.optimize_performance)
        
        performance_tab.setLayout(performance_layout)
        tabs.addTab(performance_tab, "الأداء")
        
        # إضافة التبويبات إلى التخطيط الرئيسي
        layout.addWidget(tabs)
        
        # أزرار الإغلاق
        buttons = QHBoxLayout()
        save_btn = QPushButton("حفظ")
        cancel_btn = QPushButton("إلغاء")
        
        save_btn.clicked.connect(self.save_settings)
        cancel_btn.clicked.connect(self.reject)
        
        buttons.addWidget(save_btn)
        buttons.addWidget(cancel_btn)
        layout.addLayout(buttons)
        
        self.setLayout(layout)
    
    def browse_download_path(self):
        path = QFileDialog.getExistingDirectory(
            self,
            "اختر مجلد التحميل",
            ""
        )
        if path:
            self.download_path.setText(path)
    
    def save_settings(self):
        # حفظ الإعدادات
        settings = {
            'download_path': self.download_path.text(),
            'max_speed': self.max_speed.value(),
            'concurrent_downloads': self.concurrent_downloads.value(),
            'language': self.language_combo.currentText(),
            'encrypt_files': self.encrypt_files.isChecked(),
            'scan_files': self.scan_files.isChecked(),
            'use_password': self.use_password.isChecked(),
            'password': self.password.text() if self.use_password.isChecked() else None,
            'compress_files': self.compress_files.isChecked(),
            'compression_level': self.compression_level.value(),
            'optimize_performance': self.optimize_performance.isChecked()
        }
        # TODO: حفظ الإعدادات في ملف
        self.accept()
