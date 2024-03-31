import sys
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class MapWindow(QMainWindow):
    def __init__(self, latitude, longitude, zoom):
        super().__init()

        self.setWindowTitle("Yandex Map")
        self.setGeometry(100, 100, 650, 450)

        self.latitude = latitude
        self.longitude = longitude
        self.zoom = zoom
        self.map_type = "map"

        self.api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 650, 450)

        self.update_map()

    def update_map(self):
        map_url = f"https://static-maps.yandex.ru/1.x/?ll={self.longitude},{self.latitude}&z={self.zoom}&l={self.map_type}&size=650,450&apikey={self.api_key}"
        response = requests.get(map_url)

        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        step = 0.1  # Шаг перемещения центра карты

        if event.key() == Qt.Key_PageDown:
            if self.zoom > 0:
                self.zoom -= 1
            self.update_map()

        if event.key() == Qt.Key_PageUp:
            if self.zoom < 23:
                self.zoom += 1
            self.update_map()

        if event.key() == Qt.Key_Left:
            if self.longitude - step >= -180:
                self.longitude -= step
                self.update_map()

        if event.key() == Qt.Key_Right:
            if self.longitude + step <= 180:
                self.longitude += step
                self.update_map()

        if event.key() == Qt.Key_Up:
            if self.latitude + step <= 85:
                self.latitude += step
                self.update_map()

        if event.key() == Qt.Key_Down:
            if self.latitude - step >= -85:
                self.latitude -= step
                self.update_map()

        if event.key() == Qt.Key_L:
            if self.map_type == "map":
                self.map_type = "sat"
            elif self.map_type == "sat":
                self.map_type = "sat,skl"
            else:
                self.map_type = "map"
            self.update_map()

if __name__ == "__main__":
    latitude = 55.7558
    longitude = 37.6176
    zoom = 10

    app = QApplication(sys.argv)
    window = MapWindow(latitude, longitude, zoom)
    window.show()
    sys.exit(app.exec_())
