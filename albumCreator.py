#!/usr/bin/python3

from bs4 import BeautifulSoup
import os
import re

DEBUG_TRANSCRIBE = 1
DEBUG_DICTIONARY = 0
DEBUG_IF_STATEMENT = 1
DEBUG_VAR_REPLACE = 0

def transcribe_if_attrs():
	"""
	Backstory:
	The if statements withing <ja if test> tags contain quotation characters
	in their attributes.  This is not HTML-compliant, and it causes
	BeautifulSoup to not read the full tag (it stops at quote chars).

	Bad:
		<ja:if test="<%=!homepageAddress.equals("someValue")%>">

	Good:
		<ja:if test="<%=!homepageAddress.equals(someValue)%>">
	
	This function:
		1) Reads a line from index.htt
		2) Changes the line if it contains a malformed attribute
		3) Writes the line to index.html
	"""

	index_template = open('index.htt')
	index_final = open('index.html', 'w+')
	print("Transcribing if attributes")

	# Use regex to search for conditional in each line
	conditional_finder = re.compile('<%=.*%>')
	for line in index_template:
		conditional = conditional_finder.search(line)
		if conditional:
			inner_statement = conditional.group(0)[3:-2]
			if DEBUG_TRANSCRIBE:
				print("conditional = " + conditional.group(0))
				print("innter_statement = " + inner_statement)
			fixed_statement = inner_statement.replace('\"', '')
			line = line.replace(inner_statement, fixed_statement)
			if DEBUG_TRANSCRIBE:
				print("Wrote in: " + line)
			index_final.write(line)
		else:
			index_final.write(line)
	index_template.close()
	index_final.seek(0)

	if DEBUG_TRANSCRIBE:
		debug_file = open('debug.html', 'w+')
		for line in index_final:
			debug_file.write(line)
		index_final.seek(0)

	return index_final


def tags_if(albumVars, soup):
	if DEBUG_IF_STATEMENT:
		print("\nSearching index.htt for if tags")

	for tag in soup.find_all('ja:if'):
		if tag.get('exists'):
			if albumVars.get(tag['exists']):
				tag.replaceWithChildren()
				if DEBUG_IF_STATEMENT:
					print("Exists: " + str(tag['exists']) + " YES = " + albumVars[tag['exists']])
			else:
				tag.extract()
				if DEBUG_IF_STATEMENT:
					print("Exists: " + str(tag['exists']) + " NO ")

		if tag.get('test'):
			# Testing boolean values:
			if tag['test'][0] == '$':
				testVar = re.sub('[${}]', '', str(tag.get('test')))
				if albumVars.get(testVar) == 'true':
					tag.replaceWithChildren()
				if DEBUG_IF_STATEMENT:
					print("Bool test: " + testVar + " = " + albumVars[testVar])

			# Testing conditionals:
			else:
				re_conditionals = re.compile('<%=.*%>')
				conditionals = re_conditionals.match(tag['test'])
				if conditionals:
					print("Found conditionals: " + conditionals.group(0))
				if DEBUG_IF_STATEMENT:
					print("IF: " +  "\"" + tag['test'] + "\" has failed" )
					print("TAG IS:")
					print(tag.attrs)
				
	return soup

def grabAlbumVars():

	albumVars = {}
	if DEBUG_DICTIONARY:
		print("Grabbing vars from meta.properties:")
	# Grab meta variables:
	for line in open('meta.properties'):
		line = line.strip().split('=')
		albumVars[line[0]] = line[1]

	# Grab skin variables
	if DEBUG_DICTIONARY:
		print("\nGrabbing vars from skin.properties:")
	for line in open('skin.properties'):
		line = line.strip().split('=')
		albumVars[line[0]] = line[1]

	# Grab creation variables
	if DEBUG_DICTIONARY:
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

	# Grabbing path variables
	albumVars['albumTitle'] = os.getcwd().split('/')[-2]
	albumVars['title'] = os.getcwd().split('/')[-2]

	
	return albumVars


def replace_vars_in_text(albumVars, soup):

	if DEBUG_VAR_REPLACE:
		print("\nSearching for variables in text")

	# Take each match, then call .replace() on the contained text 
	#    and replace the $(VARIABLE) with variable from dict
	find_variables = soup.find_all(text = re.compile('\$\{\w+\}'))
	for template_variable in find_variables:
		var_name = re.sub('[${}]', '', str(template_variable))
		if albumVars.get(var_name):
			if DEBUG_VAR_REPLACE:
				print("Replacing " + template_variable + " with \"" + var_name + "\"")
			fixed_text = str(template_variable).replace(template_variable, albumVars[var_name])
			template_variable.replace_with(fixed_text)
		else:
			print("Couldnt find " + template_variable + " with key \"" + var_name + "\"")


	return soup

def replace_vars_in_tags(albumVars, soup):
	if DEBUG_VAR_REPLACE:
		print("\nSearching for variables in tags")
	var_match = re.compile('\$\{\w+\}')
	for tags in soup.find_all():
		for attr in tags.attrs.keys():
			if var_match.match(str(tags[attr])):
				var_name = re.sub('[${}]', '', str(tags[attr]))
				if albumVars.get(var_name):
					if DEBUG_VAR_REPLACE:
						print("Replacing " + tags[attr] + " with " + albumVars[var_name])
					fixed_text = albumVars[var_name]
					tags[attr] = fixed_text
				else:
					if DEBUG_VAR_REPLACE:
						print("Couldn't find value for " + tags[attr] + " KEY: " + var_name)

	return soup


if __name__ == "__main__":
	albumVars = grabAlbumVars()

	if DEBUG_DICTIONARY:
		print("\nFound the following variables:")
		for x in albumVars.keys():
			print(str(x) + ": " + str(albumVars[x]))


	# Rewrite complex if tags because they aren't parsed properly
	# by beautifulSoup
	index_final = transcribe_if_attrs()

	soup = BeautifulSoup(index_final)

	# Search for if tags
	soup = tags_if(albumVars, soup)

	# Search for template vars in text
	soup = replace_vars_in_text(albumVars, soup)

	# Search for template vars in tags
	soup = replace_vars_in_tags(albumVars, soup)

	# Write final .html file
	if os.path.isfile('index.html'):
		os.remove('index.html')

	index_final.write(soup.prettify())
