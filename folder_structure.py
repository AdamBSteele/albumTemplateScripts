import os
import shutil
from slides_css_file import modify_css_file

class folder_structure:
	def __init__(self, directory, working_dir, selection):
		self.album_path = os.path.join(directory, "album")
		self.res_path = os.path.join(self.album_path, "res")
		self.slides_path = os.path.join(self.album_path, "slides")
		self.thumbs_path = os.path.join(self.album_path, "thumbs")
		self.directory = directory
		self.working_dir = working_dir
		self.selection = selection
		self.curr_dir = os.path.abspath(os.path.join(self.working_dir, os.pardir))
		self.current_dir = os.path.abspath(os.path.join(self.curr_dir, "Minimal"))
		self.current_dir_res_path = os.path.join(self.current_dir, "res")
		self.current_dir_styles_path = os.path.join(self.current_dir, "styles")
		self.current_dir_styles_light_path = os.path.join(self.current_dir_styles_path, "light")
		self.current_dir_styles_dark_path = os.path.join(self.current_dir_styles_path, "dark")

	def copy_images(self):
		image_list = []
		for image in os.listdir(self.directory):
			if image.endswith(".jpg"):
				image_list.append(os.path.join(self.directory, image))

		for im in image_list:
			shutil.copy(im, self.slides_path)
			shutil.copy(im, self.thumbs_path)

	def folder_exists(self):
		for f1 in os.listdir(self.album_path):
			if f1.endswith(".html"):
				os.remove(os.path.join(self.album_path, f1))
		for f2 in os.listdir(self.slides_path):
			if os.path.isdir(self.slides_path) == False:
				os.mkdir(self.slides_path)
			else:
				if f2.endswith(".jpg") or f2.endswith(".html"):
					os.remove(os.path.join(self.slides_path, f2))
		for f3 in os.listdir(self.thumbs_path):
			if f3.endswith(".jpg"):
				os.remove(os.path.join(self.thumbs_path, f3))
		self.copy_images()

	def folder_creation(self):
		os.mkdir(self.album_path)
		os.mkdir(self.res_path)
		os.mkdir(self.slides_path)
		os.mkdir(self.thumbs_path)

	def common_css(self):
		for f1 in os.listdir(self.current_dir):
			if f1.startswith("common") and f1.endswith(".css"):
				shutil.copy((os.path.join(self.current_dir, f1)), self.res_path)

	def js_file(self):
		for f2 in os.listdir(self.current_dir_res_path):
			if f2.endswith(".js"):
				shutil.copy(os.path.join(self.current_dir_res_path, f2), self.res_path)

	def res_files(self):
		for f3 in os.listdir(self.current_dir_styles_path):
			if self.selection == 'light' and (f3.startswith("light") and f3.endswith(".css")):
				shutil.copy((os.path.join(self.current_dir_styles_path, f3)), self.res_path)
			elif self.selection == 'dark' and (f3.startswith("dark") and f3.endswith(".css")):
				shutil.copy((os.path.join(self.current_dir_styles_path, f3)), self.res_path)
		for f4 in os.listdir(self.current_dir_styles_light_path):
			if f4.endswith(".png"):
				shutil.copy((os.path.join(self.current_dir_styles_light_path, f4)), self.res_path)

	def folder_not_exists(self):
		if os.path.isdir(self.current_dir) == True:
			self.common_css()			
		if os.path.isdir(self.current_dir_res_path) == True:
			self.js_file()
		if os.path.isdir(self.current_dir_styles_path) == True:
			self.res_files()	
		self.copy_images()
		css_file = modify_css_file(self.res_path)
		if self.selection == "light":
			css_file.light()
		else:
			css_file.dark()
			

	def create_folder_structure(self):
		if os.path.isdir(self.album_path) == True:
			self.folder_exists()
		else:
			self.folder_creation()
			self.folder_not_exists()
		return self.slides_path