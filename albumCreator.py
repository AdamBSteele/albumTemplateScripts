#!/usr/bin/python3

from bs4 import BeautifulSoup
import os
import re
import sys

DEBUG_TRANSCRIBE = 0
DEBUG_DICTIONARY = 0
DEBUG_IF_STATEMENT = 1
DEBUG_VAR_REPLACE = 0
DEBUG_EVALUATE = 0


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
	if "inux" in sys.platform:
		albumVars['albumTitle'] = os.getcwd().split('/')[-2]
		albumVars['title'] = os.getcwd().split('/')[-2]
	else:
		albumVars['albumTitle'] = os.getcwd().split('\\')[-2]
		albumVars['title'] = os.getcwd().split('\\')[-2]
	albumVars['level'] = '0'
	
	return albumVars


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
	if DEBUG_TRANSCRIBE:
		print("Transcribing if attributes")

	# Write final .html file
	if os.path.isfile('index.html'):
		os.remove('index.html')

	index_template = open('index.htt')
	our_html = open('index.html', 'w+')

	# Use regex to search for conditional in each line
	# Replaces quotations inside ("") with nothing --> ()
	# ^^ Problem with beautiful soup
	conditional_finder = re.compile('<%=.*%>')
	for line in index_template:
		conditional = conditional_finder.search(line)
		if conditional:
			inner_statement = conditional.group(0)[3:-2]
			if DEBUG_TRANSCRIBE:
				print("conditional = " + conditional.group(0))
				print("inner_statement = " + inner_statement)
			fixed_statement = inner_statement.replace('\"', '')
			line = line.replace(inner_statement, fixed_statement)
			if DEBUG_TRANSCRIBE:
				print("Wrote in: " + line)
			our_html.write(line)
		else:
			our_html.write(line)
	index_template.close()
	our_html.seek(0)

	if DEBUG_TRANSCRIBE:
		debug_file = open('debug.html', 'w+')
		for line in our_html:
			debug_file.write(line)
		our_html.seek(0)
		soup = BeautifulSoup(debug_file)
		debug_file.write(soup.prettify())

	return our_html


def handling_if_tags(albumVars, soup):

	if DEBUG_IF_STATEMENT:
		print("\nSearching index.htt for if tags")

	for tag in soup.find_all('ja:if', text=True):
		s = "<None></None>"
		if type(tag) != None:
			print(tag)
			if evaluate_if(tag, albumVars):
				tag.replaceWithChildren()
			else:
				# find else tags
				tag.decompose()
				pass
	return soup

def evaluate_if(tag, albumVars):
	"""
	There are three kinds of if tags:

	Exists:
		<ja:if exists="variableName">

	Test (Simple Boolean):
		<ja:if test="${showAlbumTitle}"

	Test (Complex Boolean)
		<ja:if test="<%=level==0 && !homepageAddress.equals("")%>">
	"""

	# Exists
	if tag.get('exists'):	
		if DEBUG_IF_STATEMENT:
			print("Exists? " + tag['exists'])
		try: 
			value = albumVars[tag['exists']]
			print("-----" + value + "----")
		except KeyError as e:
			if DEBUG_IF_STATEMENT:
				print('   KeyError: %s' % str(e))
				print('removing line')

			return False

		return True

	# Test
	'''if tag.get('test'):

		# Test (Simple Boolean)
		if tag['test'][0] == '$':
			testVar = re.sub('[${}]', '', str(tag.get('test')))			
			if DEBUG_IF_STATEMENT:
				print("Bool: " + testVar)

			try: 
				value = albumVars[testVar]
			except KeyError as e:'''
				#print('   KeyError:  %s' % str(e))
'''				return False

			if value == 'true':
				if DEBUG_IF_STATEMENT:
					print("   true")
				return True
			if value == 'false':
				if DEBUG_IF_STATEMENT:
					print("   false")
				return False

			else:
				if DEBUG_IF_STATEMENT:'''
					#print("   Non boolean value: \"" + value + "\"") 

		# Testing (Complex Boolean):
'''		else:
			re_conditionals = re.compile('<%=.*%>')
			#Get text within test
			conditional_text = re_conditionals.match(tag['test'])
			if conditional_text:
				if DEBUG_IF_STATEMENT:
					print("Evaluate: " + conditional_text.group(0))
				if evaluate_complex_boolean(conditional_text.group(0), albumVars):
					if DEBUG_IF_STATEMENT:
						print("   True")
					return True
				else:
					if DEBUG_IF_STATEMENT:
						print("   False")
					return False'''


def evaluate_complex_boolean(conditional, albumVars):
	"""
	Evaluates <ja if> conditionals:
		i.e. <%= conditonal =>

	Works on:
		Anded conditionals:
			x && y && z	

		Orred conditionals:	
			x || y || z

	Does not work on:
		x && y || z
		x || y && z


	Step 1) Remove all the <%= => crap
	Step 2) Split by && or ||
	Step 3) Evaluate each inner statement
	"""

	# This line gets rid of the '<%='' and '=>' around conditionals
	inner_text = conditional.split('%')[1][1:]

	if DEBUG_EVALUATE:
		print(" Evaluating: " + inner_text)

	# Anded conditionals:
	for anded_term in re.split('&&', inner_text):
		#   !=   <-- Bang equals
		bang_equals = False

		#  x==y  + x!=y
		if '=' in anded_term:
			left_side = anded_term.split('=')[0].strip()
			right_side = anded_term.split('=')[-1].strip()
			if '!' in anded_term:
				bang_equals = True

		#  x.equals(y) + !x.equals(y)
		if '.equals' in anded_term:
			left_side = anded_term.split('.')[0].strip()
			right_side = anded_term.split('()')[-1].strip()
			# Is this '!x.equals()' or 'x.equals()'
			if '!' in anded_term:
				left_side = left_side[1:]
				bang_equals = True

		try: 
			value = albumVars[left_side]
		except KeyError as e:
			if DEBUG_EVALUATE:
				print('   KeyError:  %s' % str(e))
			return False
		
		if DEBUG_EVALUATE:
			print(" albumVars[" + left_side + "] = " + str(value))

		if value == right_side:
			if bang_equals:
				return False
			else: continue
		
		else:
			if bang_equals:
				continue
			return False
		
	# Default is false right now
	return False
				

def replace_vars_in_text(albumVars, soup):
	"""
	Looks at all text inside html document
	Replaces found variable with value from albumVars dictionary
	"""

	if DEBUG_VAR_REPLACE:
		print("\nSearching for variables in text")

	# Take each match, then call .replace() on the contained text 
	#    and replace the $(VARIABLE) with variable from dict
	find_variables = soup.find_all(text = re.compile('\$\{\w+\}'))
	for template_variable in find_variables:
		var_name = re.sub('[${}]', '', str(template_variable))

		try: 
			value = albumVars[var_name]
		except KeyError as e:
			if DEBUG_VAR_REPLACE:
				print('   KeyError:  %s' % str(e))
			continue

		if DEBUG_VAR_REPLACE:
			print("Replacing " + template_variable + " with \"" + value + "\"")

		fixed_text = str(template_variable).replace(template_variable, value)
		template_variable.replace_with(fixed_text)

	return soup

def replace_vars_in_tags(albumVars, soup):
	"""	
		Looks at every attribute of every tag

		If a variable is found, replaces variable with value
		  from albumVars dictionary
	"""
	if DEBUG_VAR_REPLACE:
		print("\nSearching for variables in tags")
	var_match = re.compile('\$\{\w+\}')
	for tags in soup.find_all():
		for attr in tags.attrs.keys():
			if var_match.match(str(tags[attr])):
				var_name = re.sub('[${}]', '', str(tags[attr]))

				try: 
					value = albumVars[var_name]
				except KeyError as e:
					if DEBUG_VAR_REPLACE:
						print('   KeyError:  %s' % str(e))
					continue

				if DEBUG_VAR_REPLACE:
					print("Replacing " + tags[attr] + " with " + value)

				fixed_text = albumVars[var_name]
				tags[attr] = fixed_text

	return soup


if __name__ == "__main__":

	albumVars = grabAlbumVars()

	if DEBUG_DICTIONARY:
		print("\nFound the following variables:")
		for x in albumVars.keys():
			print(str(x) + ": " + str(albumVars[x]))

	#removes parentheses
	our_html = transcribe_if_attrs()

	#parses the file
	soup = BeautifulSoup(our_html)

	#handles the if tags
	soup = handling_if_tags(albumVars, soup)

	# Search for template vars in text
	'''soup = replace_vars_in_text(albumVars, soup)

	# Search for template vars in tags
	soup = replace_vars_in_tags(albumVars, soup)

	# Write final .html file
	if os.path.isfile('index.html'):
		os.remove('index.html')

<<<<<<< HEAD
	our_html.write(soup.prettify())'''
=======
	our_html = open('index.html', 'w+')

	print("Writing HTML")
	our_html.write(soup.prettify())
>>>>>>> bd8df1dc9e1937b39f369ef907b0951193ba24fc
