from PyQt5.QtWidgets import (QMainWindow, QTableWidget, QTableWidgetItem, 
                           QPushButton, QVBoxLayout, QWidget, QAction, QDockWidget,
                           QMessageBox, QInputDialog, QMenu, QSystemTrayIcon)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from .cloud_integration import CloudIntegration
from .settings_dialog import SettingsDialog
from .schedule_dialog import ScheduleDialog
from ..core.advanced_features import AdvancedFeatures

class DownloadManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("FastDownloadPro - مدير التحميلات المتقدم")
        self.setGeometry(100, 100, 1200, 800)
        self.advanced = AdvancedFeatures()
        self.setup_ui()

    def setup_ui(self):
        # إنشاء القوائم
        self.create_menu_bar()
        
        # إنشاء الجدول الرئيسي
        self.create_main_table()
        
        # إنشاء الشريط الجانبي
        self.create_side_panel()
        
        # إنشاء أيقونة النظام
        self.create_system_tray()

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        # قائمة الملف
        file_menu = menu_bar.addMenu("ملف")
        
        add_url_action = QAction("إضافة رابط", self)
        add_url_action.triggered.connect(self.add_url)
        file_menu.addAction(add_url_action)
        
        add_playlist_action = QAction("إضافة قائمة تشغيل", self)
        add_playlist_action.triggered.connect(self.add_playlist)
        file_menu.addAction(add_playlist_action)
        
        add_website_action = QAction("تحميل موقع", self)
        add_website_action.triggered.connect(self.add_website)
        file_menu.addAction(add_website_action)
        
        schedule_action = QAction("جدولة تحميل", self)
        schedule_action.triggered.connect(self.schedule_download)
        file_menu.addAction(schedule_action)

        # قائمة السحابة
        cloud_menu = menu_bar.addMenu("السحابة")
        connect_cloud_action = QAction("ربط حسابات السحابة", self)
        connect_cloud_action.triggered.connect(self.open_cloud_integration)
        cloud_menu.addAction(connect_cloud_action)

        # قائمة الأدوات
        tools_menu = menu_bar.addMenu("أدوات")
        
        encrypt_action = QAction("تشفير ملف", self)
        encrypt_action.triggered.connect(self.encrypt_file)
        tools_menu.addAction(encrypt_action)
        
        scan_action = QAction("فحص ملف", self)
        scan_action.triggered.connect(self.scan_file)
        tools_menu.addAction(scan_action)
        
        compress_action = QAction("ضغط ملف", self)
        compress_action.triggered.connect(self.compress_file)
        tools_menu.addAction(compress_action)

        # قائمة الإعدادات
        settings_menu = menu_bar.addMenu("إعدادات")
        settings_action = QAction("إعدادات البرنامج", self)
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)

    def create_system_tray(self):
        """إنشاء أيقونة النظام"""
        self.tray_icon = QSystemTrayIcon(self)
        # TODO: إضافة أيقونة للبرنامج
        # self.tray_icon.setIcon(QIcon("icon.png"))
        
        tray_menu = QMenu()
        show_action = tray_menu.addAction("عرض")
        show_action.triggered.connect(self.show)
        
        hide_action = tray_menu.addAction("إخفاء")
        hide_action.triggered.connect(self.hide)
        
        quit_action = tray_menu.addAction("خروج")
        quit_action.triggered.connect(self.close)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def add_playlist(self):
        """إضافة قائمة تشغيل يوتيوب"""
        url, ok = QInputDialog.getText(
            self,
            "إضافة قائمة تشغيل",
            "أدخل رابط قائمة التشغيل:"
        )
        if ok and url:
            try:
                self.advanced.download_playlist(url, "downloads")
                QMessageBox.information(
                    self,
                    "نجاح",
                    "تم بدء تحميل قائمة التشغيل"
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "خطأ",
                    f"حدث خطأ: {str(e)}"
                )

    def add_website(self):
        """إضافة موقع للتحميل"""
        url, ok = QInputDialog.getText(
            self,
            "تحميل موقع",
            "أدخل رابط الموقع:"
        )
        if ok and url:
            try:
                self.advanced.download_website(url, "downloads")
                QMessageBox.information(
                    self,
                    "نجاح",
                    "تم بدء تحميل الموقع"
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "خطأ",
                    f"حدث خطأ: {str(e)}"
                )

    def schedule_download(self):
        """فتح نافذة جدولة التحميل"""
        dialog = ScheduleDialog(self)
        dialog.exec_()

    def encrypt_file(self):
        """تشفير ملف"""
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "اختر الملف للتشفير",
            "",
            "All Files (*.*)"
        )
        if file_path:
            password, ok = QInputDialog.getText(
                self,
                "تشفير الملف",
                "أدخل كلمة المرور:",
                QLineEdit.Password
            )
            if ok and password:
                try:
                    encrypted_path = self.advanced.encrypt_file(file_path, password)
                    QMessageBox.information(
                        self,
                        "نجاح",
                        f"تم تشفير الملف وحفظه في:\n{encrypted_path}"
                    )
                except Exception as e:
                    QMessageBox.warning(
                        self,
                        "خطأ",
                        f"حدث خطأ أثناء التشفير: {str(e)}"
                    )

    def scan_file(self):
        """فحص ملف"""
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "اختر الملف للفحص",
            "",
            "All Files (*.*)"
        )
        if file_path:
            try:
                result = self.advanced.scan_file(file_path)
                info = f"""معلومات الملف:
                النوع: {result['type']}
                الحجم: {result['size']} bytes
                تاريخ الإنشاء: {result['created']}
                آخر تعديل: {result['modified']}"""
                
                QMessageBox.information(
                    self,
                    "نتائج الفحص",
                    info
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "خطأ",
                    f"حدث خطأ أثناء الفحص: {str(e)}"
                )

    def compress_file(self):
        """ضغط ملف"""
        from PyQt5.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "اختر الملف للضغط",
            "",
            "All Files (*.*)"
        )
        if file_path:
            try:
                compressed_path = self.advanced.compress_file(file_path)
                QMessageBox.information(
                    self,
                    "نجاح",
                    f"تم ضغط الملف وحفظه في:\n{compressed_path}"
                )
            except Exception as e:
                QMessageBox.warning(
                    self,
                    "خطأ",
                    f"حدث خطأ أثناء الضغط: {str(e)}"
                )

    def create_main_table(self):
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        headers = ["اسم الملف", "الحجم", "التقدم", "السرعة", 
                  "الوقت المتبقي", "الحالة"]
        self.table.setHorizontalHeaderLabels(headers)
        self.setCentralWidget(self.table)

    def create_side_panel(self):
        dock = QDockWidget("التصنيفات", self)
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # أزرار التصنيف
        categories = ["الكل", "فيديو", "صوت", "برامج", "ملفات مضغوطة", "أخرى"]
        for category in categories:
            btn = QPushButton(category)
            btn.clicked.connect(lambda c=category: self.filter_by_category(c))
            layout.addWidget(btn)

        dock.setWidget(widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def add_url(self):
        url, ok = QInputDialog.getText(self, "إضافة رابط", "أدخل رابط التحميل:")
        if ok and url:
            self.add_download_to_table(url)

    def add_download_to_table(self, url):
        row = self.table.rowCount()
        self.table.insertRow(row)
        
        # إضافة معلومات التحميل
        self.table.setItem(row, 0, QTableWidgetItem(url))
        self.table.setItem(row, 1, QTableWidgetItem("جاري الحساب..."))
        self.table.setItem(row, 2, QTableWidgetItem("0%"))
        self.table.setItem(row, 3, QTableWidgetItem("0 KB/s"))
        self.table.setItem(row, 4, QTableWidgetItem("--:--"))
        self.table.setItem(row, 5, QTableWidgetItem("في الانتظار"))

    def filter_by_category(self, category):
        # تنفيذ التصفية حسب الفئة
        pass

    def open_cloud_integration(self):
        dialog = CloudIntegration(self)
        dialog.exec_()

    def open_settings(self):
        dialog = SettingsDialog(self)
        dialog.exec_()
