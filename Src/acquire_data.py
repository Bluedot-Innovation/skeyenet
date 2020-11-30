"""
Filename: acquire_data.py

Function:  Downloads the Massachusetts Roads Dataset or the Massachusetts Buildings Dataset. By changing "link_file" to point at a custom list of links, you can download any other dataset too.

Author: Jerin Paul (https://github.com/Paulymorphous)
Website: https://www.livetheaiexperience.com/
"""

import urllib.request
import os
# import clickpip
import time
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from urllib.parse import urlparse

def download_images(urls, outpit_directory, image_type):
	"""
	Scraps all images from the provided urls and stores them in one location.

	Paremeters
	----------
	>urls ([str]): urls to be scrapped
	>output_directory (str): path to target directory.
	>image_type (str): Whether the images are target masks or satellite images.
	"""

	links = []

	for url in urls:
		html = urlopen(url).read()
		html_page = bs(html, features="lxml")
		og_url = html_page.find("meta",  property = "og:url")
		base = urlparse(url)
		print("base",base)
		for link in html_page.find_all('a'):
			current_link = link.get('href')
			if current_link.endswith('.tiff') or current_link.endswith('.tif'):
				print(current_link)
				if og_url:
					print("currentLink",current_link)
					links.append(og_url["content"] + current_link)
				else:
					links.append(current_link)
		
	print("links to download: {}".format(len(links)))
	counter = 0

	for image_link in links:
		image_path = output_directory + image_type + "/" + os.path.basename(image_link)
		print("downloading {}: {}".format(counter, image_link))
		
		urllib.request.urlretrieve(image_link, image_path)
		
		counter += 1

	print("{} images downloaded to {}\n".format(counter, output_directory+image_type))

def clean_images(images, output_directory):
	"""
	Remove incomplete images from both Images and Targets folder

	Paremeters
	----------
	>images ([str]): list of image names (without extension) to be deleted
	>output_directory (str): path with Images and Targets.
	"""

	images_dir = output_directory + "/Images/"
	targets_dir = output_directory + "/Targets/"

	print("images to delete: {}".format(len(images)))

	counter = 0
	for image in images:
		print("deleting {}: {}".format(counter, image))
		os.remove(images_dir + image + ".tiff")
		os.remove(targets_dir + image + ".tif")
		counter += 1

if __name__ == '__main__':
	
	dataset_name = "MassachusettsBuildings"
	link_file_images = [
						"https://www.cs.toronto.edu/~vmnih/data/mass_buildings/train/sat/index.html",
						 "https://www.cs.toronto.edu/~vmnih/data/mass_buildings/valid/sat/index.html",
						 "https://www.cs.toronto.edu/~vmnih/data/mass_buildings/test/sat/index.html"
						 ]
	link_file_targets = ["https://www.cs.toronto.edu/~vmnih/data/mass_buildings/train/map/index.html",
						"https://www.cs.toronto.edu/~vmnih/data/mass_buildings/valid/map/index.html",
						"https://www.cs.toronto.edu/~vmnih/data/mass_buildings/test/map/index.html"]
	output_directory = "./Data/{}/".format(dataset_name)

	if not os.path.exists(output_directory):
		os.mkdir(output_directory)
		os.mkdir(output_directory + "Images/")
		os.mkdir(output_directory + "Targets/")

	start_time = time.time()
	# download_images(link_file_images, output_directory, "Images")
	# download_images(link_file_targets, output_directory, "Targets")
	faulty_images = ["23129065_15",
					 "23129125_15",
					 "23129140_15",
					 "23129155_15",
					 "23129170_15",
					 "23278885_15",
					 "23279035_15",
					 "23279050_15",
					 "23279080_15",
					 "23279095_15",
					 "23428900_15",
					 "23429035_15",
					 "23429050_15",
					 "23429065_15",
					 "23429170_15",
					 "23579110_15",
					 "23579125_15",
					 "23579140_15",
					 "23729110_15",
					 "23878915_15",
					 "23878930_15",
					 "23878945_15",
					 "24029110_15",
					 "24328870_15",
					 "24478900_15"]

	clean_images(faulty_images, output_directory)
	print("TOTAL TIME: {} minutes".format(round((time.time() - start_time)/60, 2)))