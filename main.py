import sys
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MapWindow(QMainWindow):
    def __init__(self, latitude, longitude, zoom):
        super().__init__()

        self.setWindowTitle("Yandex Map")
        self.setGeometry(100, 100, 800, 600)

        self.latitude = latitude
        self.longitude = longitude
        self.zoom = zoom

        self.api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 800, 600)

        self.update_map()

    def update_map(self):
        map_url = f"https://static-maps.yandex.ru/1.x/?ll={self.longitude},{self.latitude}&z={self.zoom}&l=map&size=650,450"
        print(map_url)
        response = requests.get(map_url)

        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.label.setPixmap(pixmap)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_PageDown:
            if self.zoom > 0:
                self.zoom -= 1
            self.update_map()

        if event.key() == Qt.Key_PageUp:
            if self.zoom < 23:
                self.zoom += 1
            self.update_map()


if __name__ == "__main__":
    latitude = 55.7558
    longitude = 37.6176
    zoom = 10

    app = QApplication(sys.argv)
    window = MapWindow(latitude, longitude, zoom)
    window.show()
    sys.exit(app.exec_())
