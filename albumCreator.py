#!/usr/bin/python

from bs4 import BeautifulSoup
import os
import re
#from os import path, remove
DEBUG = 1

def convert_exists_tag(tag):
	pass

def tags_if(albumVars, soup):
	if DEBUG:
		print("\nSearching index.htt for if tags")

	for tag in soup.find_all('ja:if'):
		if tag.get('exists'):
			if albumVars.get(tag['exists']):
				tag.replaceWithChildren()
				if DEBUG:
					print("Exists: " + str(tag['exists']) + " YES = " + albumVars[tag['exists']])
			else:
				tag.extract()
				if DEBUG:
					print("Exists: " + str(tag['exists']) + " NO ")

		if tag.get('test'):
			# Testing boolean values:
			if tag['test'][0] == '$':
				testVar = tag.get('test').translate(None, '${}')
				if albumVars.get(testVar) == 'true':
					tag.replaceWithChildren()
					if DEBUG:
						print("Bool test: " + testVar + " = " + albumVars[testVar])

			# Testing conditionals:
			else:
				pass
	return soup

def grabAlbumVars():

	albumVars = {}
	if DEBUG:
		print("Grabbing vars from meta.properties:")
	# Grab meta variables:
	for line in open('meta.properties'):
		line = line.strip().split('=')
		albumVars[line[0]] = line[1]

	# Grab skin variables
	if DEBUG:
		print("\nGrabbing vars from skin.properties:")
	for line in open('skin.properties'):
		line = line.strip().split('=')
		albumVars[line[0]] = line[1]

	# Grab creation variables
	if DEBUG:
		print("\nGrabbing vars from creationVariables: ")
	for line in open('creationVariables.txt'):
		if line[0:2] == "//" or line[0] == '\n':
			continue
		else:
			line = line.strip().split('=')
			albumVars[line[0]] = line[1]

	# jAlbum has two names for album description.
	# Note: albumDecription is "descript", skinDescription is "description"
	if albumVars.get('descript'):
		albumVars['albumDescription'] = albumVars['descript']

	albumVars['albumTitle'] = os.getcwd().split('/')[-1]
	return albumVars


def replace_vars_in_text(albumVars, soup):

	if DEBUG:
		print("\nSearching for variables in text")

	# Take each match, then call .replace() on the contained text 
	#    and replace the $(VARIABLE) with variable from dict

	find_variables = soup.find_all(text = re.compile('\$\{\w+\}'))
	for template_variable in find_variables:
		var_name = str(template_variable).translate(None, '${}')
		if albumVars.get(var_name):
			if DEBUG:
				print("Attempting to replace " + template_variable + " with \"" + var_name + "\"")
			fixed_text = unicode(template_variable).replace(template_variable, albumVars[var_name])
			template_variable.replace_with(fixed_text)

	return soup
	

if __name__ == "__main__":
	albumVars = grabAlbumVars()

	if DEBUG:
		print("\nFound the following variables:")
		for x in albumVars.keys():
			print(str(x) + ": " + str(albumVars[x]))


	index_template = open('index.htt')
	soup = BeautifulSoup(index_template)

	# Search for if tags
	soup = tags_if(albumVars, soup)

	# Search for template vars in text
	soup = replace_vars_in_text(albumVars, soup)

	# Write final .html file
	if os.path.isfile('index.html'):
		os.remove('index.html')
	index_final = open('index.html', 'w+')
	index_final.write(soup.prettify())