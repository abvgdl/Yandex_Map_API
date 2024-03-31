
import sys
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow
from PyQt5.QtGui import QPixmap

class MapWindow(QMainWindow):
    def __init__(self, latitude, longitude, zoom):
        super().__init__()

        self.setWindowTitle("Yandex Map")
        self.setGeometry(100, 100, 800, 600)

        api_key = "40d1649f-0493-4b70-98ba-98533de7710b"
        map_url = f"https://static-maps.yandex.ru/1.x/?ll={longitude},{latitude}&z={zoom}&l=map&size=650,450"

        response = requests.get(map_url)
        print(response.status_code, map_url)

        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            label = QLabel(self)
            label.setPixmap(pixmap)
            label.resize(650, 450)

if __name__ == "__main__":
    latitude = 55.7558
    longitude = 37.6176
    zoom = 10

    app = QApplication(sys.argv)
    window = MapWindow(latitude, longitude, zoom)
    window.show()
    sys.exit(app.exec_())
