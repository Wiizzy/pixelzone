# Инструкция - https://github.com/Wiizzy/pixelzone/tree/main?tab=readme-ov-file#%D0%B8%D0%BD%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%86%D0%B8%D1%8F
# Лицензия - https://github.com/Wiizzy/pixelzone/tree/main?tab=readme-ov-file#%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F-%D0%BD%D0%B0-%D0%B8%D1%81%D0%BF%D0%BE%D0%BB%D1%8C%D0%B7%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%BD%D0%BE%D0%B3%D0%BE-%D0%BE%D0%B1%D0%B5%D1%81%D0%BF%D0%B5%D1%87%D0%B5%D0%BD%D0%B8%D1%8F
# Приятной игры ^-^

import json
import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QComboBox, QDialog, QDialogButtonBox, QLabel, QMessageBox
from PyQt6.QtCore import Qt, QTimer, QRect, pyqtSignal, QThread
from PyQt6.QtGui import QIcon, QPainter, QPixmap, QImage
import mss
import numpy as np
from screeninfo import get_monitors
import cv2

class CaptureThread(QThread):
    update_image = pyqtSignal(QPixmap)  


    def __init__(self, rect, frame_rate):
        super().__init__()
        self.rect = rect
        self.frame_rate = frame_rate
        self.running = True


    def run(self):
        while self.running:
            self.capture_frame()
            self.msleep(int(1000 / self.frame_rate))

    def stop(self):
        self.running = False

    def capture_frame(self):
        with mss.mss() as sct:
            monitor = {
                "top": self.rect.y(),
                "left": self.rect.x(),
                "width": self.rect.width(),
                "height": self.rect.height(),
            }
            screenshot = sct.grab(monitor)
            img = np.array(screenshot)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)


            
            height, width, _ = img_rgb.shape
            if width < 1920 or height < 1080:
                img_rgb = cv2.resize(img_rgb, (1920, 1080), interpolation=cv2.INTER_CUBIC)


            
            height, width, channel = img_rgb.shape
            q_image = QImage(img_rgb.data, width, height, 3 * width, QImage.Format.Format_RGB888)
            img_qpixmap = QPixmap.fromImage(q_image)


            self.update_image.emit(img_qpixmap) 



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PixelZone")
        self.setGeometry(200, 200, 600, 400)
        self.frame_rate = 144 
        self.capture_monitor = 0  
        self.output_monitor = 0  
        self.selected_rect = None 
        self.display_mode = 0  
        self.setWindowIcon(QIcon("F:/ico.png"))

        self.load_settings()

        self.initUI()


    def load_settings(self):
        settings_file = 'settings.json'
        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                settings = json.load(f)
                print(f"Settings loaded: {settings}")
                self.frame_rate = settings.get('frame_rate', 144)
                self.capture_monitor = settings.get('capture_monitor', 0)
                self.output_monitor = settings.get('output_monitor', 0)
                self.display_mode = settings.get('display_mode', 0)
        else:
            print("Settings file not found.")


    def save_settings(self):
        """Сохраняет настройки в файл."""
        settings = {
            'frame_rate': self.frame_rate,
            'capture_monitor': self.capture_monitor,
            'output_monitor': self.output_monitor,
            'display_mode': self.display_mode
        }
        with open('settings.json', 'w') as f:
            json.dump(settings, f)


    def closeEvent(self, event):
        """Сохраняет настройки перед закрытием программы."""
        self.save_settings()
        event.accept()


    def initUI(self):
        self.select_area_button = QPushButton("Выбрать область", self)
        self.select_area_button.clicked.connect(self.open_selection_mode)


        self.settings_button = QPushButton("Настройки", self)
        self.settings_button.clicked.connect(self.open_settings)


        self.show_button = QPushButton("Транслировать", self)
        self.show_button.clicked.connect(self.show_fullscreen)


        self.contact_button = QPushButton("Контакты разработчика", self)
        self.contact_button.clicked.connect(self.contact_developer)


        layout = QVBoxLayout()
        layout.addWidget(self.select_area_button)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.show_button)
        layout.addWidget(self.contact_button)
        
        self.contact_button = QPushButton("Contact Developer", self)
        self.contact_button.clicked.connect(self.contact_developer)
        
        self.setStyleSheet("""
            QWidget {
                font-family: 'Arial', sans-serif;
                background-color: #1e1e2f;
                color: #f5f5f5;
            }


            QPushButton {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #4a90e2, stop:1 #0056d2);
                color: white;
                padding: 10px 20px;
                font-size: 15px;
                margin: 10px 5px;
                border-radius: 8px;
                border: 1px solid #337ab7;
            }


            QPushButton:hover {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #5eaaf2, stop:1 #337ab7);
                border: 1px solid #5eaaf2;
            }


            QPushButton:pressed {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #337ab7, stop:1 #1d4e89);
            }


            QPushButton#contact_button {
                color: #4a90e2;
                font-size: 14px;
                font-style: italic;
                border: none;
                background: none;
                text-decoration: underline;
                margin: 15px 0;
            }


            QPushButton#contact_button:hover {
                color: #5eaaf2;
                text-decoration: none;
            }


            QLabel {
                font-size: 14px;
                margin-bottom: 10px;
                color: #e0e0e0;
            }


            QComboBox {
                background-color: #2c3e50;
                color: white;
                border: 1px solid #3498db;
                border-radius: 6px;
                padding: 5px;
                font-size: 13px;
            }


            QComboBox:hover {
                border-color: #5eaaf2;
            }


            QComboBox::drop-down {
                background-color: #3498db;
                border: none;
                border-radius: 0px 6px 6px 0px;
            }


            QMessageBox {
                background-color: #1E1E2F;
                color: #f5f5f5;
                font-size: 14px;
                border-radius: 10px;
            }


            a {
                color: #5eaaf2;
                text-decoration: none;
                font-weight: bold;
            }


            a:hover {
                color: #72d0ff;
                text-decoration: underline;
            }
        """)




        
        self.contact_button = QPushButton("Контакты с разработчиком")
        self.contact_button.setObjectName("contact_button")




        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)


    def open_selection_mode(self):
        monitor = get_monitors()[self.capture_monitor]
        self.selection_window = SelectionWindow(monitor)
        self.selection_window.finished.connect(self.update_selected_rect)
        self.selection_window.showFullScreen()


    def update_selected_rect(self, rect):
        if rect:
            self.selected_rect = rect


    def open_settings(self):
        settings_dialog = SettingsDialog(
            self.frame_rate, self.capture_monitor, self.output_monitor, self.display_mode, self
        )
        if settings_dialog.exec():
            self.frame_rate = settings_dialog.selected_fps
            self.capture_monitor = settings_dialog.capture_monitor
            self.output_monitor = settings_dialog.output_monitor
            self.display_mode = settings_dialog.display_mode
            self.save_settings()



    def show_fullscreen(self):
        if self.selected_rect:
            if hasattr(self, "fullscreen_window") and self.fullscreen_window.isVisible():
                self.fullscreen_window.update_settings(
                    self.frame_rate, self.output_monitor, self.display_mode
                )
            else:
                self.fullscreen_window = FullscreenWindow(
                    self.selected_rect, self.frame_rate, self.output_monitor, self.display_mode
                )
                self.fullscreen_window.show()
        else:
            print("Please select an area first!")


    def contact_developer(self):
        info_message = '''
        <h2 style="color: #5eaaf2; font-size: 18px;">Связаться с разработчиком</h2>
        <ul>
            <li><a href="https://t.me/pgryo" style="color: #5eaaf2; font-weight: bold;">Telegram</a></li>
            <li><a href="https://github.com/Wiizzy" style="color: #5eaaf2; font-weight: bold;">GitHub</a></li>
            <li><a href="https://github.com/Wiizzy/pixelzone/releases" style="color: #5eaaf2; font-weight: bold;">Check Updates</a></li>
        </ul>
        <h3 style="color: #5eaaf2; font-size: 16px;">Поддержите разработку</h3>
        <ul>
            <li><a href="https://www.tbank.ru/cf/7AzbVM85gzc" style="color: #5eaaf2; font-weight: bold;">T-bank</a></li>
            <li><a href="https://yoomoney.ru/to/4100118174208286" style="color: #5eaaf2; font-weight: bold;">YooMoney</a></li>
        </ul>
        '''


        
        msg = QMessageBox(self)
        msg.setWindowTitle("Связаться с разработчиком")
        msg.setText(info_message)
        msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        
        
        msg.setStyleSheet("""
            QMessageBox {
                background-color: #1E1E2F;
                color: #f5f5f5;
                font-size: 14px;
                border-radius: 10px;
                padding: 15px;
            }
            QLabel {
                color: #e0e0e0;
                font-size: 14px;
            }
            a {
                color: #5eaaf2;
                text-decoration: none;
                font-weight: bold;
            }
            a:hover {
                color: #72d0ff;
                text-decoration: underline;
            }
        """)


        
        msg.exec()




class SelectionWindow(QWidget):
    finished = pyqtSignal(QRect)


    def __init__(self, monitor):
        super().__init__()
        self.setWindowTitle("Select Area")
        self.setGeometry(monitor.x, monitor.y, monitor.width, monitor.height)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setWindowOpacity(0.5)
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.start_point = None
        self.end_point = None
        self.selected_rect = None


    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.start_point = event.globalPosition().toPoint() 


    def mouseMoveEvent(self, event):
        if self.start_point:
            self.end_point = event.globalPosition().toPoint()
            self.update()


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.start_point:
            self.end_point = event.globalPosition().toPoint() 
            self.selected_rect = QRect(self.start_point, self.end_point).normalized()
            
            if self.selected_rect.width() > 1920 or self.selected_rect.height() > 1080:
                self.selected_rect.setWidth(1920)
                self.selected_rect.setHeight(1080)
                QMessageBox.warning(self, "Warning", "The selected area is too large. The size is limited to 1920x1080.")
            self.finished.emit(self.selected_rect)
            self.close()



    def paintEvent(self, event):
        if self.start_point and self.end_point:
            painter = QPainter(self)
            painter.setPen(Qt.GlobalColor.red)
            painter.drawRect(QRect(self.mapFromGlobal(self.start_point), self.mapFromGlobal(self.end_point)))



class SettingsDialog(QDialog):
    def __init__(self, current_fps, capture_monitor, output_monitor, display_mode, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.selected_fps = current_fps
        self.capture_monitor = capture_monitor
        self.output_monitor = output_monitor
        self.display_mode = display_mode


        layout = QVBoxLayout()


        
        self.label_fps = QLabel("Частота:")
        self.combo_box_fps = QComboBox()
        self.combo_box_fps.addItems(["15", "30", "60", "144"])
        self.combo_box_fps.setCurrentText(str(current_fps))
        layout.addWidget(self.label_fps)
        layout.addWidget(self.combo_box_fps)


        
        self.label_capture_monitor = QLabel("Монитор захвата:")
        self.combo_box_capture_monitor = QComboBox()
        self.monitors = get_monitors()
        for monitor in self.monitors:
            self.combo_box_capture_monitor.addItem(f"{monitor.name} ({monitor.width}x{monitor.height})")
        self.combo_box_capture_monitor.setCurrentIndex(capture_monitor)
        layout.addWidget(self.label_capture_monitor)
        layout.addWidget(self.combo_box_capture_monitor)


        
        self.label_output_monitor = QLabel("Монитор вывода:")
        self.combo_box_output_monitor = QComboBox()
        for monitor in self.monitors:
            self.combo_box_output_monitor.addItem(f"{monitor.name} ({monitor.width}x{monitor.height})")
        self.combo_box_output_monitor.setCurrentIndex(output_monitor)
        layout.addWidget(self.label_output_monitor)
        layout.addWidget(self.combo_box_output_monitor)


        
        self.label_display_mode = QLabel("Настройки вывода:")
        self.combo_box_display_mode = QComboBox()
        self.combo_box_display_mode.addItems([
            "Растянуть изображение",
            "Подогнать изображение",
            "Черный фон",
            "Плитка изображения"
        ])
        self.combo_box_display_mode.setCurrentIndex(display_mode)
        layout.addWidget(self.label_display_mode)
        layout.addWidget(self.combo_box_display_mode)


        
        self.button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.apply_settings)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)


        self.setLayout(layout)


    def apply_settings(self):
        self.selected_fps = int(self.combo_box_fps.currentText())
        self.capture_monitor = self.combo_box_capture_monitor.currentIndex()
        self.output_monitor = self.combo_box_output_monitor.currentIndex()
        self.display_mode = self.combo_box_display_mode.currentIndex()
        self.accept()



class FullscreenWindow(QWidget):
    def __init__(self, rect, frame_rate, monitor_index, display_mode):
        super().__init__()
        self.rect = rect
        self.frame_rate = frame_rate
        self.monitor_index = monitor_index
        self.display_mode = display_mode
        self.setWindowTitle("Fullscreen Mode")


        monitors = get_monitors()
        self.output_monitor = monitors[monitor_index]
        self.setGeometry(
            self.output_monitor.x, self.output_monitor.y,
            self.output_monitor.width, self.output_monitor.height
        )


        self.capture_thread = CaptureThread(self.rect, self.frame_rate)
        self.capture_thread.update_image.connect(self.update_image)
        self.capture_thread.start()


    def update_image(self, image):
        self.screenshot = image
        self.update()


    def update_settings(self, frame_rate, monitor_index, display_mode):
        self.frame_rate = frame_rate
        self.monitor_index = monitor_index
        self.display_mode = display_mode
        self.capture_thread.stop()
        self.capture_thread = CaptureThread(self.rect, self.frame_rate)
        self.capture_thread.update_image.connect(self.update_image)
        self.capture_thread.start()


    def paintEvent(self, event):
        if hasattr(self, "screenshot"):
            painter = QPainter(self)
            try:
                if self.display_mode == 0:  # Растянуть изображение
                    scaled_screenshot = self.screenshot.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio)
                    painter.drawPixmap(0, 0, scaled_screenshot)
                elif self.display_mode == 1:  # Замастить изображение
                    scaled_screenshot = self.screenshot.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
                    center_x = (self.width() - scaled_screenshot.width()) // 2
                    center_y = (self.height() - scaled_screenshot.height()) // 2
                    painter.drawPixmap(center_x, center_y, scaled_screenshot)
                elif self.display_mode == 2:  # (черный фон)
                    scaled_screenshot = self.screenshot.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
                    center_x = (self.width() - scaled_screenshot.width()) // 2
                    center_y = (self.height() - scaled_screenshot.height()) // 2
                    painter.drawPixmap(center_x, center_y, scaled_screenshot)
                elif self.display_mode == 3:  # Дублировать изображение
                    scaled_screenshot = self.screenshot.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio)
                    for x in range(0, self.width(), scaled_screenshot.width()):
                        for y in range(0, self.height(), scaled_screenshot.height()):
                            painter.drawPixmap(x, y, scaled_screenshot)
            finally:
                painter.end()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())