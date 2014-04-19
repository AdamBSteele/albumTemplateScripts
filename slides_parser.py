import shutil
import os
from bs4 import BeautifulSoup
import re
import threading

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


def image_retrieve():
	images = []
	threads = []
	folder = "C:\\Users\\Public\\Pictures\\Sample Pictures\\"
	album_name = (os.path.dirname(folder)).split('\\')[-1]
	slides_path = create_folder_structure(folder)
	for file in os.listdir(folder):
		if file.endswith(".jpg"):
			images.append(file)

	for imageIndex, image in enumerate(images):
		'''The below file open operation takes place every time
		when the for loop iterates (I know doing this operation
		every time in a for loop is bad). I tried it by declaring
		it as global varibale. But the problem with global variable
		is -- BeautifulSoup is maintaining its state even though the
		global data is passed several times.

		Briefly, the result which comes in the first loop is repeating
		again and again through out the loop.

		For this reason, we have put up the open operation in the for 
		loop itself'''

		htt_file = open('slide.htt', 'r')
		soup = BeautifulSoup(htt_file)
		im = ""
		if imageIndex > 0 and imageIndex < (len(images) - 1):
			previousimage = images[imageIndex - 1]
			im = images[imageIndex]
			nextimage = images[imageIndex + 1]
		elif imageIndex > 0 and imageIndex == (len(images) - 1):
			previousimage = images[imageIndex - 1]
			im = images[imageIndex]
			nextimage = ""
		elif imageIndex > 0 and imageIndex > (len(images) - 1):
			break;
		else:
			previousimage = ""
			im = images[imageIndex]
			nextimage = images[imageIndex + 1]
		new_thread = slides_image_urls(soup, previousimage, im, nextimage, album_name, slides_path)
		new_thread.start()
		threads.append(new_thread)
	for t in threads:
		t.join()
		

def copy_images(dir, s_path, th_path):
	image_list = []
	for image in os.listdir(dir):
		if image.endswith(".jpg"):
			image_list.append(os.path.join(dir, image))

	for im in image_list:
		shutil.copy(im, s_path)
		shutil.copy(im, th_path)



def file_rename(file_path):
	for files in os.listdir(file_path):
		if files.startswith("light") and files.endswith(".css"):
			os.rename(os.path.join(file_path, files), os.path.join(file_path, "styles.css"))



def create_folder_structure(directory):
	album_path = os.path.join(directory, "album")
	res_path = os.path.join(album_path, "res")
	slides_path = os.path.join(album_path, "slides")
	thumbs_path = os.path.join(album_path, "thumbs")
	if os.path.isdir(album_path) == True:
		for f1 in os.listdir(album_path):
			if f1.endswith(".html"):
				os.remove(os.path.join(album_path, f1))
		for f2 in os.listdir(slides_path):
			if f2.endswith(".jpg") or f2.endswith(".html"):
				os.remove(os.path.join(slides_path, f2))
		for f3 in os.listdir(thumbs_path):
			if f3.endswith(".jpg"):
				os.remove(os.path.join(thumbs_path, f3))
		copy_images(directory, slides_path, thumbs_path)
	else:
		current_dir = os.getcwd()
		selection = "light"
		current_dir_res_path = os.path.join(current_dir, "res")
		current_dir_styles_path = os.path.join(current_dir, "styles")
		current_dir_styles_light_path = os.path.join(current_dir_styles_path, "light")
		current_dir_styles_dark_path = os.path.join(current_dir_styles_path, "dark")
		os.mkdir(album_path)
		os.mkdir(res_path)
		os.mkdir(slides_path)
		os.mkdir(thumbs_path)
		if os.path.isdir(current_dir) == True:
			for f1 in os.listdir(current_dir):
				if f1.startswith("common") and f1.endswith(".css"):
					shutil.copy((os.path.join(current_dir, f1)), res_path)
		if os.path.isdir(current_dir_res_path) == True:
			for f2 in os.listdir(current_dir_res_path):
				if f2.endswith(".js"):
					shutil.copy(os.path.join(current_dir_res_path, f2), res_path)
		if os.path.isdir(current_dir_styles_path) == True:
			for f3 in os.listdir(current_dir_styles_path):
				if selection == 'light' and (f3.startswith("light") and f3.endswith(".css")):
					shutil.copy((os.path.join(current_dir_styles_path, f3)), res_path)
			for f4 in os.listdir(current_dir_styles_light_path):
				if f4.endswith(".png"):
					shutil.copy((os.path.join(current_dir_styles_light_path, f4)), res_path)
		file_rename(res_path)
		copy_images(directory, slides_path, thumbs_path)
	return slides_path


if __name__ == "__main__":
	image_retrieve()