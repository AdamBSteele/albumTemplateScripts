from bs4 import BeautifulSoup
import re

album_tags = ""
album_description = ""
album_name = "Sample Pictures"
folder_level = ""
previous_page = ""
parent_index_page = ""
icon_path = ""
folder = ""
credit_text = ""
next_page = ""
google_maps = ""
homepage_address =""
comment = ""
total_indexes = ""

def soup_ja_if(soup):
	dict = {'${showAlbumTitle}' : album_name, '<%=level==0 && !homepageAddress.equals(' : folder_level, \
		'totalIndexes': total_indexes,'albumTags': album_tags, 'albumDescription': album_description, \
		'folder': folder, 'iconPath': icon_path, 'parentIndexPage': parent_index_page, 'comment': comment, \
		'homepageAddress': homepage_address, 'creditText': credit_text}
	dict1 = {'previousIndexPage': previous_page, 'nextIndexPage': next_page}
	for links in soup.find_all('ja:if'):
		if links.get('test') in dict.keys():
			if dict.get(links.get('test')):
				links.replaceWithChildren()
			else:
				links.extract()
		elif links.get('exists') in dict.keys():
			if dict.get(links.get('exists')):
				links.replaceWithChildren()
			else:
				links.extract()
		elif links.get('exists') in dict1.keys():
			if dict1.get(links.get('exists')):
				links.find_next_sibling("ja:else").extract()
				links.replaceWithChildren()
			else:
				links.extract()
	index_parser(soup)

def soup_ja_else(soup):
	for else_links in soup.find_all('ja:else'):
		else_links.replaceWithChildren()
	index_parser(soup)

def soup_include(soup):
	for include_links in soup.find_all('ja:include'):
		if include_links.get('page') == 'header.inc':
			include_links.extract()
		elif include_links.get('page') == 'footer.inc':
			include_links.extract()
	index_parser(soup)

def index_parser(soup):
	if soup.find('ja:if') != None:
		soup_ja_if(soup)
	elif soup.find('ja:else') != None:
		soup_ja_else(soup)
	elif soup.find('ja:include') != None:
		soup_include(soup)
		'''elif soup.find('ja:coliterator') != None:
			tag = soup.find('ja:coliterator')
			original_tag = soup.find('ja:coliterator').td
			print(original_tag.contents)
			new_tag = soup.new_tag("td", ("").join(original_tag.contents))
			tag.append(new_tag)
			print(soup)'''
	else:
		print(soup.prettify())

if __name__ == "__main__":
	htt_file = open('C:\\Users\\Bharadwaj\\Desktop\\Albums\\Minimal\\index.htt', 'r')
	soup = BeautifulSoup(htt_file)
	index_parser(soup)
	htt_file.close()