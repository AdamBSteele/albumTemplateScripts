import os
import shutil
from slides_css_file import modify_css_file

def copy_images(dir, s_path, th_path):
	image_list = []
	for image in os.listdir(dir):
		if image.endswith(".jpg"):
			image_list.append(os.path.join(dir, image))

	for im in image_list:
		shutil.copy(im, s_path)
		shutil.copy(im, th_path)


def create_folder_structure(directory, selection):
	album_path = os.path.join(directory, "album")
	res_path = os.path.join(album_path, "res")
	slides_path = os.path.join(album_path, "slides")
	thumbs_path = os.path.join(album_path, "thumbs")
	if os.path.isdir(album_path) == True:
		for f1 in os.listdir(album_path):
			if f1.endswith(".html"):
				os.remove(os.path.join(album_path, f1))
		for f2 in os.listdir(slides_path):
			if os.path.isdir(slides_path) == False:
				os.mkdir(slides_path)
			else:
				if f2.endswith(".jpg") or f2.endswith(".html"):
					os.remove(os.path.join(slides_path, f2))
		for f3 in os.listdir(thumbs_path):
			if f3.endswith(".jpg"):
				os.remove(os.path.join(thumbs_path, f3))
		copy_images(directory, slides_path, thumbs_path)
	else:
		current_dir = os.getcwd()
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
				elif selection == 'dark' and (f3.startswith("dark") and f3.endswith(".css")):
					shutil.copy((os.path.join(current_dir_styles_path, f3)), res_path)
			for f4 in os.listdir(current_dir_styles_light_path):
				if f4.endswith(".png"):
					shutil.copy((os.path.join(current_dir_styles_light_path, f4)), res_path)
		copy_images(directory, slides_path, thumbs_path)
		modify_css_file(res_path, selection)

	return slides_path
