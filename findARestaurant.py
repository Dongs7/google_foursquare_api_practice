from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "YOUR_CLIENT_ID"
foursquare_client_secret = "YOUR_CLIENT_SECRET"
foursquare_api_addr = "https://api.foursquare.com/v2/venues/"
pic_size = '300x300'


def findARestaurant(mealType,location):
	#1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.

	#2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
	#HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi

	#3. Grab the first restaurant
	#4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
	#5. Grab the first image
	#6. If no image is available, insert default a image url
	#7. Return a dictionary containing the restaurant name, address, and image url
	loc = getGeocodeLocation(location)
	lat = loc[0]
	lng = loc[1]

	# Remove comment below line to see the lat,lng of given location
	# print lat,lng

	# API query for getting restaurant near given latitude and longitude
	url1 = (foursquare_api_addr+"search?intent=browser&ll=%f,%f&query=%s&client_id=%s&client_secret=%s&v=20170621" %(lat,lng,mealType,foursquare_client_id, foursquare_client_secret))

	h = httplib2.Http()

	# Restaurant Info in json format
	result = json.loads(h.request(url1,'GET')[1])

	# Get Restaurant VENUE ID
	restaurant_id = result['response']['venues'][0]['id']

	# API query for getting images of restaurant
	url2 = (foursquare_api_addr+"%s/photos?client_id=%s&client_secret=%s&v=20170621" % (restaurant_id, foursquare_client_id, foursquare_client_secret))
	result2 = json.loads(h.request(url2,'GET')[1])

	# If there are images, save its save its url in the restaurant_img_url variable
	if result2['response']['photos']['count'] != 0:
		restaurant_img_url = result2['response']['photos']['items'][0]['prefix'] + pic_size + result2['response']['photos']['items'][0]['suffix']
	else:	# Else save 'no image url'
		restaurant_img_url = 'no image url'

	# Get Restaurant Name and Address
	restaurant_name = result['response']['venues'][0]['name']
	restaurant_address = result['response']['venues'][0]['location']['formattedAddress'][0]

	# Create dictionary for the restaurant
	restaurant_info = {'name':restaurant_name, 'address':restaurant_address, 'img_url':restaurant_img_url}

	print 'Restaurant Name : ' + restaurant_info['name']
	print 'Restaurant Address : ' + restaurant_info['address']
	print 'Restaurant Image Url : ' + restaurant_info['img_url'] + '\n'

if __name__ == '__main__':
	findARestaurant("Pizza", "Tokyo, Japan")
	findARestaurant("Tacos", "Jakarta, Indonesia")
	findARestaurant("Tapas", "Maputo, Mozambique")
	findARestaurant("Falafel", "Cairo, Egypt")
	findARestaurant("Spaghetti", "New Delhi, India")
	findARestaurant("Cappuccino", "Geneva, Switzerland")
	findARestaurant("Sushi", "Los Angeles, California")
	findARestaurant("Steak", "La Paz, Bolivia")
	findARestaurant("Gyros", "Sydney Australia")
