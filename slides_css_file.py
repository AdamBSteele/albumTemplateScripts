import sys
import re
import os

class modify_css_file:
	def __init__(self, css_path):
		self.css_light_file = "light.css"
		self.css_dark_file = "dark.css"
		self.css_file = "styles.css"
		self.border_width = 0
		self.css_path = css_path

	def light(self):
		if os.path.isdir(self.css_path) == True:
			if os.path.isfile(os.path.join(self.css_path, self.css_light_file)) == True:
				new_file = open(os.path.join(self.css_path, self.css_light_file), 'r')
				final_css_file = open((os.path.join(self.css_path, self.css_file)), 'w')
				for line in new_file:
					line = re.sub(r"\${borderWidth}", str(self.border_width) , str(line))
					final_css_file.write(line)
				final_css_file.close()
				new_file.close()
				os.remove(os.path.join(self.css_path, self.css_light_file))

	def dark(self):
		if os.path.isdir(self.css_path) == True:
			if os.path.isfile(os.path.join(self.css_path, self.css_dark_file)) == True:
				new_file = open(os.path.join(self.css_path, self.css_dark_file), 'r')
				border_width = 0
				final_css_file = open((os.path.join(self.css_path, self.css_file)), 'w')
				for line in new_file:
					line = re.sub(r"\${borderWidth}", str(self.border_width) , str(line))
					final_css_file.write(line)
				final_css_file.close()
				new_file.close()
				os.remove(os.path.join(self.css_path, self.css_dark_file))