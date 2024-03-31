import math
import sys
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QLineEdit, QPushButton, QCheckBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MapWindow(QMainWindow):
    def __init__(self, latitude, longitude, zoom):
        super().__init__()

        self.setWindowTitle("Yandex Map")
        self.setGeometry(100, 100, 650, 500)

        self.default_latitude = latitude
        self.default_longitude = longitude
        self.latitude = latitude
        self.longitude = longitude
        self.zoom = zoom
        self.map_type = "map"
        self.marker = []
        self.show_index = False

        self.api_key = "40d1649f-0493-4b70-98ba-98533de7710b"

        self.label = QLabel(self)
        self.label.setGeometry(0, 50, 650, 400)

        self.search_input = QLineEdit(self)
        self.search_input.setGeometry(10, 10, 520, 30)

        self.search_button = QPushButton("Искать", self)
        self.search_button.setGeometry(530, 10, 150, 30)
        self.search_button.clicked.connect(self.search_location)

        self.reset_button = QPushButton("Сброс поиска", self)
        self.reset_button.setGeometry(530, 450, 150, 30)
        self.reset_button.clicked.connect(self.reset_search)

        self.address_label = QLabel(self)
        self.address_label.setGeometry(10, 460, 630, 30)
        self.address_label.setText(" ")
        self.address_label.setStyleSheet("color: red; font-size: 10pt")

        self.index_checkbox = QCheckBox("Отображать почтовый индекс", self)
        self.index_checkbox.setGeometry(10, 440, 630, 30)
        self.index_checkbox.stateChanged.connect(self.toggle_index)

        self.update_map()

    def update_map(self, marker=None):
        if self.marker and not marker:
            marker = self.marker
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
            response = requests.get(search_url)
            if response.status_code == 200:
                data = response.json()
                feature_member = data["response"]["GeoObjectCollection"]["featureMember"]

                if len(feature_member) > 0:
                    coordinates = feature_member[0]["GeoObject"]["Point"]["pos"]
                    lon, lat = map(float, coordinates.split())
                    self.latitude = lat
                    self.longitude = lon
                    self.update_map()
                    self.add_marker(lat, lon)

                    formatted_address = feature_member[0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"]["text"]
                    if self.show_index:
                        postal_code = feature_member[0]["GeoObject"]["metaDataProperty"]["GeocoderMetaData"].get(
                            "Address", {}).get("postal_code", "")
                        if postal_code:
                            formatted_address += f", {postal_code}"
                    self.address_label.setText(formatted_address)

    def reset_search(self):
        self.latitude = self.default_latitude
        self.longitude = self.default_longitude
        self.marker = []
        self.update_map()
        self.address_label.setText("")

    def add_marker(self, lat, lon):
        self.update_map(marker=(lon, lat))

    def keyPressEvent(self, event):
        print(event)
        step = 0.1

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

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton or event.button() == Qt.RightButton:
            x = event.pos().x()
            y = event.pos().y()

            dy = 250 - y
            dx = x - 325
            lon = self.longitude + dx * 0.0000428 * 2 ** (15 - self.zoom)
            lat = self.latitude + dy * 0.0000428 * math.cos(math.radians(self.latitude)) * 2 ** (15 - self.zoom)

            self.latitude = round(lat, 6)
            self.longitude = round(lon, 6)
            self.update_map()
            self.add_marker(lat, lon)
            if event.button() == Qt.LeftButton:
                self.search_location()
            elif event.button() == Qt.RightButton:
                self.search_organization(lat, lon)

    def search_organization(self, lat, lon):
        print('YES')
        search_url = f"https://search-maps.yandex.ru/v1/?ll={lon},{lat}&spn=0.001,0.001&&lang=ru_RU&type=biz&results=10&apikey={self.api_key}"
        response = requests.get(search_url)
        print(response.status_code, search_url)
        if response.status_code == 200:
            data = response.json()
            organizations = data["features"]
            print(organizations)
            for org in organizations:
                org_lon, org_lat = org["geometry"]["coordinates"]
                distance = math.sqrt((org_lat - lat) ** 2 + (org_lon - lon) ** 2)
                print(distance)
                if distance <= 0.0004:
                    print(org['properties']['name'])
                    self.address_label.setText(f"Организация: {org['properties']['name']}")
                    break

    def toggle_index(self):
        self.show_index = not self.show_index
        self.search_location()


if __name__ == "__main__":
    latitude = 55.7558
    longitude = 37.6176
    zoom = 10

    app = QApplication(sys.argv)
    window = MapWindow(latitude, longitude, zoom)
    window.show()
    sys.exit(app.exec_())
