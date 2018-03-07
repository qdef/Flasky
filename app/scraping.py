"""README:
This class is now obsolete: the temperatures are now retrieved from an API instead of a weather website.
This enables the data page loading to be way faster, without any connection issues.
We kept this file for information on how to do web scraping if need be.
"""

import requests
from lxml import html

class Scraping:
	#Svalbard
	def Longyearbyen(self):
		website = requests.get('https://weather.com/fr-FR/temps/aujour/l/733d1f96d0c824d15364f14d1c4df70eb8b2251b892545bbd897ae407f55b8e8')
		tree=html.fromstring(website.content)
		temperature_longyearbyen=tree.xpath('//div[@class="today_nowcard-temp"]/span/text()')
		if temperature_longyearbyen:
			temperature_longyearbyen=temperature_longyearbyen[0]
		else:
			temperature_longyearbyen="[Data not available]"
		return temperature_longyearbyen
	
	#Canadian cities	
	def Yellowknife(self):
		website = requests.get('https://weather.gc.ca/city/pages/nt-24_metric_e.html')
		tree=html.fromstring(website.content)
		temperature_yellowknife=tree.xpath('//p[@class="text-center mrgn-tp-md mrgn-bttm-sm lead"]/span[@class="wxo-metric-hide"]/text()')
		if temperature_yellowknife:
			temperature_yellowknife=temperature_yellowknife[0]
			temperature_yellowknife=temperature_yellowknife[:-1]
		else:
			temperature_yellowknife="[Data not available]"		
		return temperature_yellowknife 
	
	def Iqaluit(self):
		website = requests.get('https://weather.gc.ca/city/pages/nu-21_metric_e.html')
		tree=html.fromstring(website.content)
		temperature_iqaluit=tree.xpath('//p[@class="text-center mrgn-tp-md mrgn-bttm-sm lead"]/span[@class="wxo-metric-hide"]/text()')
		if temperature_iqaluit:
			temperature_iqaluit=temperature_iqaluit[0]
			temperature_iqaluit=temperature_iqaluit[:-1]
		else:
			temperature_iqaluit="[Data not available]"
		return temperature_iqaluit 	
	
	#Greenland cities
	def Qaanaaq(self):
		website = requests.get('https://weather.com/fr-FR/temps/aujour/l/eb24e43d169ddf7aab0fc00629b0edaeff04c5ee04b378a337f72df8c4e89ead8f73236d73500562b476c5e7e3e63732')
		tree=html.fromstring(website.content)
		temperature_qaanaaq=tree.xpath('//div[@class="today_nowcard-temp"]/span/text()')
		if temperature_qaanaaq:
			temperature_qaanaaq=temperature_qaanaaq[0]
		else:
			temperature_qaanaaq="[Data not available]"			
		return temperature_qaanaaq 
	
	def Nuuk(self):
		website = requests.get('https://weather.com/fr-FR/temps/aujour/l/201821a57b460f0cb6b1f90c273b16b5f67f5439f70ab5f7e194437c04206235')
		tree=html.fromstring(website.content)
		temperature_nuuk=tree.xpath('//div[@class="today_nowcard-temp"]/span/text()')
		if temperature_nuuk:
			temperature_nuuk=temperature_nuuk[0]
		else:
			temperature_nuuk="[Data not available]"			
		return temperature_nuuk
	
	#Russia	
	def Khatanga(self):
		website = requests.get('https://weather.com/fr-FR/temps/aujour/l/5c8957dabce679465ff145b7497a32654e0b6a4ae2de77df1b0ce639c03cd6b2')
		tree=html.fromstring(website.content)
		temperature_khatanga=tree.xpath('//div[@class="today_nowcard-temp"]/span/text()')
		if temperature_khatanga:
			temperature_khatanga=temperature_khatanga[0]
		else:
			temperature_khatanga="[Data not available]"			
		return temperature_khatanga 	


	



