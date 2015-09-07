import urllib
import urllib2
import re
import urlparse
import cookielib
from urlparse import urlsplit
#from publicsuffix import PublicSuffixList
import mechanize
from bs4 import BeautifulSoup

#read LICENSE.txt before you use this code

def getGoogleLinks(link,depth):

	i = 0
	results_array = []
	while i<depth:
	
		br = mechanize.Browser()
		br.set_handle_robots(False)
		br.addheaders= [('User-agent','chrome')]

		term = link.replace(" ","+")
		query = "http://www.google.com/search?num=100&q="+term+"&start="+str(i*100)
		
		try:
			htmltext = br.open(query,timeout=5).read()
		except:
			print "Fehler 1.1"
		
		soup = BeautifulSoup(htmltext)
		search = soup.findAll('div',attrs={'id':'search'})
		searchtext = str(search[0])
		soup1 = BeautifulSoup(searchtext)
		list_items = soup1.findAll('li')
		regex = "q(?!.*q).*?&amp"
		pattern = re.compile(regex)


		for li in list_items:
    			soup2 = BeautifulSoup(str(li))
    			links = soup2.findAll('a')
    			source_link = links[0]
    			source_url = re.findall(pattern,str(source_link))
    			if len(source_url)>0:
       				results_array.append(str(source_url[0].replace("q=","").replace("&amp","").replace("related:","").replace("q%3Dcache:","").replace("'","")))
		urls2 = re.findall('www(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', str(results_array))
		
		i+=1

	return urls2

def getYahooLinks(link,depth):
	
	i = 0
	link = link.replace(" ","+")
	urls2 = []
	results_array = []
	while i<depth:	
		br = mechanize.Browser()
		br.set_handle_robots(False)
		br.addheaders = [('User-agent','chrome')]

		query = "http://search.yahoo.com/search;_ylt=Agm6_o0evxm18v3oXd_li6bvzx4?p="+link+"&b="+str((i*10)+1)
		i = i+1
		htmltext = br.open(query,timeout=5).read()
		soup = BeautifulSoup(htmltext)
		search = soup.findAll('div',attrs={'id':'web'})
		searchtext = str(search[0])
		soup1 = BeautifulSoup(searchtext)
		list_items = soup1.findAll('li')
		
		for li in list_items:
			soup2 = BeautifulSoup(str(li))
			links = soup2.findAll('a')
			if len(links)>0:
				results_array.append(links)
		urls2 = (re.findall('www(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',str(results_array)))
	
	return urls2


def getImp(vor_link):
	br = mechanize.Browser()
	cj = cookielib.LWPCookieJar()
	br.set_cookiejar(cj)
	br.set_handle_robots(False)
	br.set_handle_equiv(False)
	br.set_handle_redirect(True)
	br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(),max_time=1)
	br.addheaders = [('User-agent','chrome')]

	page = br.open(vor_link, timeout=5)

	htmlcontent = page.read()
	soup = BeautifulSoup(htmlcontent)
	
	newurlArray = []
	for link  in br.links(text_regex=re.compile('^((?!IMG).)*$')):
		newurl = urlparse.urljoin(link.base_url,link.url)
		if newurl not in newurlArray:
			newurlArray.append(newurl)
			if 'kontakt' in newurl:
				#return  newurl
				finalunderlinks.append(newurl)			

			if 'impressum' in newurl:
				#return  newurl
				finalunderlinks.append(newurl)		
			
			if 'Impressum' in newurl:
				#return  newurl
				finalunderlinks.append(newurl)

			if 'Kontakt' in newurl:
				#return  newurl
				finalunderlinks.append(newurl)
			if 'kontakt-impressum' in newurl:
				#return newurl		
				finalunderlinks.append(newurl)


def getEmail(link):
	request = urllib2.Request(str(link))
	request.add_header('UserAgent','Ruel.ME Sample Scraper')
	response = urllib2.urlopen(request)
	for line in response.read().split('\n'):
		match = re.search(r'([A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4})',line,re.I)
		if match:
			return match.group(1)


term = "fast cars" #searchterm
depth = 2 
finallinks = [] #links
finalunderlinks = []

#-----------------------------------------------
# google 

print "Google..."
try:
	google = getGoogleLinks(term,depth)
except: 
	print "Error 1"

#Yahoo 
print "Yahoo..."
try:
	yahoo = getYahooLinks(term,10)
except:
	print "Error 1.1"


#---------------------------------------------------------
# cut off all unneded things
f = []
print "WOrking on the links..."
for i in google:
	test2 = i.split("/")
	finallinks.append(test2[0])
for j in yahoo:
	test2 = j.split("/")
	finallinks.append(test2[0])

finallinks = dict(map(lambda i: (i,1),finallinks)).keys()


# --------------------------------------------------------------------
# Searching for impressum,contact,..

print "Searching for impressum..."

for j in finallinks:

	try:
		#j = str(j).replace("[","")
		#j = str(j).replace("'","")
		getImp("http://"+j)
	except:
		print "    Error while opening a link"
# --------------------------------------------------------------------
# Searching for the Email
print "Searching for the Email..."

finalunderlinks = dict(map(lambda i: (i,1),finalunderlinks)).keys()
for i in finalunderlinks:
	
	try:
		temp = getEmail(i)
		print temp
	except: 
		print "Error 3"
