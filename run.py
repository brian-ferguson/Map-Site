#pip install lxml (required to encode the html response)
import argparse, requests, json, os, sys, csv
from bs4 import BeautifulSoup
import pandas as pd


def load_data(url):
	source = requests.get(url).text
	return source

def read_csv():
	urls = []
	data = pd.read_csv("urls.csv")
	#read each row and add the value to the urls list
	for index, row in data.iterrows():
		urls.append(row['urls'])
	#return the list of webstie urls if it is not empty
	if(urls):
		return urls
	else:
		return False	

def write_csv(list, url, column_name):
	#get the current directory
	current_directory = os.getcwd()
	path = current_directory + "\\" + url
	#if the directory doesnt exist
	if not(os.path.isdir(path)):
		#get the current directory of running file
		os.mkdir(path)
		#create a filename for the csv output (contained in the directory just created)
		#folder: haascnc.com > csvfile: haascnc.com.csv
		filename = path + "\\" +  url + ".csv"
		#write the information to the newly created csvfile
		with open(filename, 'w') as csvfile:
		#create a csv file in the folder named the base url and the date
			fieldnames = [column_name]
			writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
			writer.writeheader()
			for element in list:
				writer.writerow({column_name: element})	
	else:
		print("the folder has already been created")
	
def get_url_hrefs(url, keyword):

	routes = []
	soup = BeautifulSoup(load_data(url), 'lxml')
	#find all the a tags in the html
	links = soup.find_all('a')
	
	#for each a tag returned in the html
	for link in links:
		#get the href value from the a element
		href = link.get('href')
		
		#check if href is not empty and the keyword is contained in the href
		if(href and keyword in href):
			routes.append(href)

	#if the routes list is not empty return it
	if(routes):
		return routes
	else:
		False

def get_urls_hrefs(url_list, keyword):
#create a list to hold the list of each webpages routes
	route_list = []
	urls_list = []
	for url in url_list:
		#call the get_single_route for each url
		routes = get_url_hrefs(("https://" + url), keyword)
		#check if false is returned
		if(routes):
			#append the routes list to the route_list
			route_list.append(routes)
			urls_list.append(url)
	if(len(route_list) == len(urls_list)):
		return route_list, urls_list
	else:
		return False

if(__name__ == "__main__"):

	#set up the argument flags for user input
	parser = argparse.ArgumentParser(description='--url "url.xyz" --keyword "filter" --save')
	parser.add_argument('-url', action='store', type=str, help='The base url in the form someurl.xyz.')
	parser.add_argument('-keyword', action='store', type=str, help='The keyword you want to make sure the a href text contains before writing.', default="")
	parser.add_argument('--save', help='Print more data', action='store_true')
	
	args = parser.parse_args()
	
	#if the url was specified
	if(args.url):
	
		#combine the htt[://www. prefix with the entered url
		base_url = "http://www." + args.url
		#get the links from the specified url that contain the specified keyword
		routes = get_url_hrefs(base_url, args.keyword)
		
		#if the route is not empty
		if(routes):
			#print each link in the routes list
			for route in routes:
				print(args.url + " href: ", route)
		
			#print the number of routes returned
			print("returned hrefs: ", len(routes))
			
			#if the save arg is enabled
			if(args.save):
				#output the list as a csv
				write_csv(routes, args.url, "route")
			
	#if no url was specified
	else:
		#open the urls.csv from the current directory
		base_urls = read_csv()
		url_route_lists, urls_returned = get_urls_hrefs(base_urls, args.keyword)
		
		#check that the url_route_lists and urls_returned are not empty
		if(urls_returned):
			#iterate through the urls and routes concurrently
			for index in range(len(urls_returned)):
				print("website url: ", urls_returned[index])
				print("returned a hrefs: ", len(url_route_lists[index]))
				if(args.save):
					write_csv(url_route_lists[index], urls_returned[index], "route")