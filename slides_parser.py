import sys
import argparse
import shutil
import os
from bs4 import BeautifulSoup
from folder_structure import create_folder_structure
from slides_maker import slides_image_urls
import re
import threading

def image_retrieve(dir, selection):
	images = []
	threads = []
	album_name = (os.path.dirname(dir)).split('\\')[-1]
	slides_path = create_folder_structure(dir, selection)
	for file in os.listdir(dir):
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
		

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--directory", help="Creates html pages for the images in the given argument(directory)",
	type=str, nargs = '+')
	args = parser.parse_args()
	if args.directory != None:
		if os.path.isdir(args.directory[0]) == True:
			image_retrieve(args.directory[0], args.directory[1])
		else:
			print ("You haven't entered any valid directory path")	
			sys.exit()