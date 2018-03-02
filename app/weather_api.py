import requests

class WeatherAPI:
	def api_call(self, lat, lon):
		lat=str(lat)
		lon=str(lon)
		call = 'http://api.openweathermap.org/data/2.5/weather?lat='+lat+'&lon='+lon+'&units=metric'
		call_and_token = call+'&APPID=5e087b669666e00e055234e599710347'
		response = requests.get(call_and_token)
		data = response.json()
		return int(data['main']['temp'])



