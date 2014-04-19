import sys
import re
import os

def modify_css_file(css_path, argument):
	css_light_file = "light.css"
	css_dark_file = "dark.css"
	css_file = "styles.css"
	data = ""
	line = ""
	
	if argument == "light":
		if os.path.isdir(css_path) == True:
			if os.path.isfile(os.path.join(css_path, css_light_file)) == True:
				new_file = open(os.path.join(css_path, css_light_file), 'r')
				border_width = 0
				final_css_file = open((os.path.join(css_path, css_file)), 'w')
				for line in new_file:
					line = re.sub(r"\${borderWidth}", str(border_width) , str(line))
					final_css_file.write(line)
				final_css_file.close()
				new_file.close()
				os.remove(os.path.join(css_path, css_light_file))
