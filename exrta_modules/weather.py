import requests


api_url = "http://api.openweathermap.org/data/2.5/weather"
token_for_api = "95ebbbbeea6772572df3f8109e4ca0e7"


def weather_in_city(name_of_city):
    settings = {"q": name_of_city, "appid": token_for_api, "units": "metric" }

    try:
        data = requests.get(api_url, params=settings)
        info = data.json() # data.json() == json.loads(data.text)

        # Pressure in hPa (1 hPa = 100 Pa)
        # 1 мм.рт.ст. = 400/3 Pa
        pressure = info["main"]["pressure"]
        pressure *= 100 / (400 / 3)
        pressure = round(pressure, 2)

        result = '''
    Погода в городе "{}":
    * температура = {} °С
    * давление = {} мм.рт.ст.
    * скорость ветра = {} м/с
    * влажность = {} %
    * облачность = {} %'''.format(
            name_of_city, info["main"]["temp"],
            pressure, info["wind"]["speed"],
            info["main"]["humidity"], info["clouds"]["all"]
        )
        return result

    except:
        return "Город не найден"
