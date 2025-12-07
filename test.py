import sys
import requests
from PyQt5.QtWidgets import (QApplication,QPushButton,QWidget,QLabel,QLineEdit,QVBoxLayout)
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city=QLabel("Enter the city name :",self)
        self.city_input=QLineEdit(self)
        self.get_weather=QPushButton("Get Weather",self)
        self.temperature=QLabel(self)
        self.emoji=QLabel(self)
        self.descrption=QLabel(self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App By SUHAS🤞")

        box = QVBoxLayout()

        box.addWidget(self.city)
        box.addWidget(self.city_input)
        box.addWidget(self.get_weather)
        box.addWidget(self.temperature)
        box.addWidget(self.emoji)
        box.addWidget(self.descrption)

        self.setLayout(box)

        self.city.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.get_weather.setAlignment(Qt.AlignCenter)
        self.temperature.setAlignment(Qt.AlignCenter)
        self.emoji.setAlignment(Qt.AlignCenter)
        self.descrption.setAlignment(Qt.AlignCenter)

        self.city.setObjectName("CITY")
        self.city_input.setObjectName("CITY_INPUT")
        self.get_weather.setObjectName("GET_WEATHER")
        self.temperature.setObjectName("TEMPERATURE")
        self.emoji.setObjectName("EMOJI")
        self.descrption.setObjectName("DES")

        self.setStyleSheet("""
            QLabel,QPushButton,QLineEdit{
                           font-family:calibri;
                           font-size:30px;
                           }
            #CITY{      
                            }
            #CITY_INPUT{
                           font-size:40px;
                           font:bold;
                           }
            #TEMPERATURE{
                           font-size:40px;
                           font:bold;
                           }
            #EMOJI{
                           font-family: Segeo UI emoji;
                           font-size:100px;
                           }
            #DES{
                           font-size:40px;}


        """)
        self.get_weather.clicked.connect(self.getweather)

        
    
    def getweather(self):
        
        apikey="4e9180cafa223332ce1801e4046485e4"
        citys=self.city_input.text()
        url=f"https://api.openweathermap.org/data/2.5/weather?q={citys}&appid={apikey}"

        try:
            response=requests.get(url,timeout=5)
            response.raise_for_status()
            data=response.json()
            
            if data["cod"]==200:
                self.display_weather(data)
            
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Bad Request\nplease check your input")
                case 401:
                    self.display_error("Unauthorized\ninvaild ap key")
                case 403:
                    self.display_error("Forbiden\nacces denined")
                case 404:
                    self.display_error("Not found\nplease check your input")
                case 500:
                    self.display_error("internal server Error\nplease check your input")
                case 502:
                    self.display_error("Bad gateway\nplease check your input")
                case 503:
                    self.display_error("service unavailabel\nplease check your input")
                case _:
                    self.display_error(f"HTTP Error\n{http_error}")
                
        except requests.exceptions.Timeout:
            self.display_error("Time is Out\nPlease try again")
        except requests.exceptions.ConnectionError:
            self.display_error("internet Is Not Connected\ncheck internet")
        except requests.exceptions.TooManyRedirects:
            self.display_error("check the URl\ncheck the link.")
        except requests.exceptions.RequestException as req_error:
            self.display_error(req_error)

    def display_error(self,message):
        self.temperature.setText(message)
        self.emoji.clear()
        self.descrption.clear()

    def display_weather(self,data):
        temperature_k=data["main"]["temp"]
        temperature_c=temperature_k - 273.15
        weather_id=data["weather"][0]["id"]
        descrption_data=data["weather"][0]["description"]

        
        self.temperature.setText(f"{temperature_c:.0f}^C")
        self.emoji.setText(self.weather_emoji(weather_id))
        self.descrption.setText(descrption_data)
        print(data)

    @staticmethod
    def weather_emoji(weather_id):

            if 200 <= weather_id <= 232:
                return "⚡"
            elif 300<=weather_id<= 321:
                return "🌦️"
            elif 500<=weather_id<=531:
                return "☀️ "
            elif 600 <= weather_id<=622:
                return "❄️"
            elif 700<= weather_id<= 781:
                return "🌨️"
            elif weather_id == 800:
                return "⛅"
            else:
                return "😁"

if __name__ =="__main__":
    app = QApplication(sys.argv)
    weather_app=WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

