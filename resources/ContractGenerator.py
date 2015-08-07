import argparse, urllib, urllib2, cookielib, time, os, platform

class ArgsParser:
	def __init__(self):
		parser = argparse.ArgumentParser(description='Contract generator.')
		parser.add_argument('username', metavar='username', help='NSN-intra\username')
		parser.add_argument('password', metavar='password', help='NSN-intra\password')
		args = parser.parse_args()
		self.username = args.username
		self.password = args.password

class NewRise:
	URL_RISE = "http://rise.inside.nokiasiemensnetworks.com/rise/"
	URL_LOGIN = URL_RISE + "j_spring_security_check"
	URL_SEARCH = URL_RISE + "btsfault/export?product=540&productRelease=5548&releaseIncrement=3378&states=APPROVED&states=PUBLISHED&platformIncluded=false&searchType=LATEST_VERSIONS&exportTypeId=-1&exportProperties="

	def __init__(self, username, password):
		self.username = username
		self.password = password

	def login(self):
		print "Logging in."
		cookie = cookielib.CookieJar()
		self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
		login_data = urllib.urlencode({'j_username' : self.username, 'j_password' : self.password})
		self.opener.open(self.URL_LOGIN, login_data)
		
	def extract_excel(self):
		search = self.opener.open(self.URL_SEARCH)
		page = search.read()
		start = page.index("statusCheckUrl: \"") + 17 # offset for 'statusCheckUrl: "'
		end = page.index("\"", start) 
		excel_url = self.URL_RISE + page[start:end]
		print "Downloading."
		
		desktop = os.path.expanduser('~') + "/Desktop/"
		myfile = self.opener.open(excel_url)
		output = open(desktop + "downloaded.xlsx", 'wb')
		output.write(myfile.read())
		output.close()
		print "Done."
		
def main():
	parser = ArgsParser()
	rise = NewRise(parser.username, parser.password)
	rise.login()
	rise.extract_excel()

if __name__ == '__main__':
	main()