import pprint
import sys
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QEvent


class MapWindow(QMainWindow):
    def __init__(self, latitude, longitude, zoom):
        super().__init__()

        self.setWindowTitle("Yandex Map")
        self.setGeometry(100, 100, 650, 500)

        self.latitude = latitude
        self.longitude = longitude
        self.zoom = zoom
        self.map_type = "map"
        self.marker = []

        self.api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

        self.label = QLabel(self)
        self.label.setGeometry(0, 50, 650, 400)

        self.search_input = QLineEdit(self)
        self.search_input.setGeometry(10, 10, 470, 30)

        self.search_button = QPushButton("Искать", self)
        self.search_button.setGeometry(490, 10, 150, 30)
        self.search_button.clicked.connect(self.search_location)

        self.update_map()

    def update_map(self, marker=None):
        if self.marker and not marker:
            marker = self.marker #Поторопился
        if not marker:
            map_url = f"https://static-maps.yandex.ru/1.x/?ll={self.longitude},{self.latitude}&z={self.zoom}&l={self.map_type}&size=650,400&"
        else:
            self.marker = marker
            map_url = f"https://static-maps.yandex.ru/1.x/?ll={self.longitude},{self.latitude}&pt={marker[0]},{marker[1]},pm2rdl&z={self.zoom}&l={self.map_type}&size=650,400&"
        response = requests.get(map_url)

        if response.status_code == 200:
            pixmap = QPixmap()
            pixmap.loadFromData(response.content)
            self.label.setPixmap(pixmap)

    def search_location(self):
        search_text = self.search_input.text()
        if search_text:
            search_url = f"https://geocode-maps.yandex.ru/1.x/?apikey={self.api_key}&format=json&geocode={search_text}"
            print(search_url)
            response = requests.get(search_url)
            if response.status_code == 200:
                data = response.json()
                pprint.pprint(data)
                feature_member = data["response"]["GeoObjectCollection"]["featureMember"]

                if len(feature_member) > 0:
                    coordinates = feature_member[0]["GeoObject"]["Point"]["pos"]
                    lon, lat = map(float, coordinates.split())
                    print(lon, lat)
                    self.latitude = lat
                    self.longitude = lon
                    self.update_map()
                    self.add_marker(lat, lon)

    def add_marker(self, lat, lon):
        self.update_map(marker=(lon, lat))

    def keyPressEvent(self, event):
        step = 0.1
        print(self.longitude, event.key())

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
