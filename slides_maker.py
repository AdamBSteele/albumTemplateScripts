import os
import re
import threading
from bs4 import BeautifulSoup

class slides_image_urls(threading.Thread):
	'''
	This class is explicitly written for creating
	the html pages for the respective images in the
	slides folder that will be created in the folderpath
	which was mentioned (i.e which contains all the photos).
	This class creates number of threads for all the 
	images passed into it and they create html files
	in parallel and without any thread locking system.

	An images's data is entirely different from another.
	So, there is no need to implement thread locking
	system.
	'''

	def __init__(self, soup, previousimage, im, nextimage, album_name, slides_path):
		'''
		__init__ declares all the useful variables 
		to be used in constructing the web pages in 
		the slides folder
		'''

		threading.Thread.__init__(self)
		self.soup = soup
		self.previous_page = previousimage
		self.image = im
		self.next_page = nextimage
		self.album_name = album_name
		self.slides_path = slides_path
		self.res_path = "../res"
		self.style_path = "../res/style.css"
		self.index_page = "index.html"
		self.to_index_page = "To index page"
		self.to_previous_page = "Previous page"
		self.to_next_page = "Next Page"
		self.at_last_page = "At Last Page"
		self.at_first_page = "At First Page"
		self.image_width = 800
		self.image_height = 600
		self.google_maps = ""
		self.thumbnail_navigation = ""
		self.original_path = ""
		self.comment = ""
		self.homepage_address = ""
		self.credit_text = ""
		self.file_type = "image"
	
	def run(self):
		self.ja_tags_parser()


	def variable_constructor(self, data):
		'''
		The html_soup in this method contains
		parsed html data with the ${variable_names}.
		We change all those ${variable_names} using
		regular expression
		'''

		html_soup = BeautifulSoup(data)
		next_image_url = self.next_page.split('.')[0] + ".html"
		previous_image_url = self.previous_page.split('.')[0] + ".html"
		image_url = self.image.split('.')[0] + ".html"
		html_soup = re.sub(r"\${albumTitle}", self.album_name, str(html_soup))
		html_soup = re.sub(r"\${previousPage}", previous_image_url, str(html_soup))
		html_soup = re.sub(r"\${nextPage}", next_image_url, str(html_soup))
		html_soup = re.sub(r"\${imagePath}", self.image, str(html_soup))
		html_soup = re.sub(r"\${resPath}", self.res_path, str(html_soup))
		html_soup = re.sub(r"\${imageWidth}", str(self.image_width), str(html_soup))
		html_soup = re.sub(r"\${title}", self.image.split('.')[0], str(html_soup))
		html_soup = re.sub(r"\${imageHeight}", str(self.image_height), str(html_soup))
		html_soup = re.sub(r"\${stylePath}", self.style_path, str(html_soup))
		html_soup = re.sub(r"\${indexPage}", self.index_page, str(html_soup))
		html_soup = re.sub(r"\$text.indexPage", self.to_index_page, str(html_soup))
		html_soup = re.sub(r"\$text.previousPage", self.to_previous_page, str(html_soup))
		html_soup = re.sub(r"\$text.nextPage", self.to_next_page, str(html_soup))
		html_soup = re.sub(r"\$text.atLastPage", self.at_last_page, str(html_soup))
		html_soup = re.sub(r"\$text.atFirstPage", self.at_first_page, str(html_soup))
		dest_file = open((os.path.join(self.slides_path, image_url)), 'w')
		dest_file.write(html_soup)
		dest_file.close()
	

	def ja_tags_parser(self):
		'''
		Variables in slides.htt file from the source template
		category.video -- if the file is a video;
		${showalbumtitle} -- the title of the album 
		(i.e the name of the folder); 
		previouspage -- the before image;
		nextpage -- next image; 
		googlemaps -- google maps; 
		thumbnail navigation -- thumbnail navigation;
		originalPath -- Image, maybe with link to original;
		comment -- some sort of comment; 
		homepageaddress -- web site address of the owner 
		if exists; 
		credittext -- developer's own trademark

		Main functionality of this function:
		1) It takes in the the html data and
			does recursion on the data in order to 
			remove all the <ja> tags.

		2) In the first iteration it checks for the
			<ja:if> tags and parse them accordingly
			if the respective variables exist. There
			might be some cases where there can be
			inner <ja:if> tags. In order to parse the
			entire tags we apply recursion on the same
			data again. It check is there exists any <ja:if>
			tags and parses them accordingly.
			
		3) Once the recursion finds that there are no 
			<ja:if> tags, it goes to the next step; where
			it iterates through the whole data and parses out
			the <ja:else> tags in the same method which was
			mentioned above in the step 2.
		'''

		if self.soup.find('ja:if') != None:
			for links in self.soup.find_all('ja:if'):
				if links.get('test') == '${showAlbumTitle}':
					if self.album_name:
						links.replaceWithChildren()
					else:
						pass
				elif links.get('test') == '<%=fileCategory == Category.video%>':
					if self.file_type == "image":
						links.extract()
					else:
						links.replaceWithChildren()
				elif links.get('exists') == 'nextPage':
					if not self.next_page:
						links.extract()
					else:
						links.find_next_sibling("ja:else").extract()
						links.replaceWithChildren()
				elif links.get('exists') == 'previousPage':
					if not self.previous_page:
						links.extract()
					else:
						links.find_next_sibling("ja:else").extract()
						links.replaceWithChildren()
				elif links.get('test') == '${googleMaps}':
					if self.google_maps == "":
						links.extract()
					else:
						links.replaceWithChildren()
				elif links.get('test') == '${thumbnailNavigation}':
					if self.thumbnail_navigation == "":
						links.extract()
					else:
						links.replaceWithChildren()
				elif links.get('exists') == 'originalPath':
					if self.original_path == "":
						links.extract()
					else:
						links.replaceWithChildren
				elif links.get('exists') == 'comment':
					if self.comment == "":
						links.extract()
					else:
						links.replaceWithChildren
				elif links.get('exists') == 'homepageAddress':
					if self.homepage_address == "":
						links.extract()
					else:
						links.replaceWithChildren()
				elif links.get('exists') == 'creditText':
					if self.credit_text == "":
						links.extract()
					else:
						links.replaceWithChildren()
			self.ja_tags_parser()
		elif self.soup.find('ja:else') != None:
			for else_links in self.soup.find_all('ja:else'):
				else_links.replaceWithChildren()
			self.ja_tags_parser()
		else:
			self.variable_constructor(self.soup.prettify())
