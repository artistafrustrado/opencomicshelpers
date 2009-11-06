#!/usr/bin/env python

import scribus
import Image
import re
import os.path

class ComicsMaker:

	def __init__(self):
		self.pageSize = (210,297)
		self.margins = (8,8,8,8)
		self.formats = 'jpg|jpeg|jpe|gif|tiff|tif|tga|eps|ps|psd|png|bmp|ico|xcf|xpm|pcx|svg'
		self.images = []

	def clean_up_and_queue(self, path, dirs, files):
		test = re.compile("\.(%s)$" % self.formats, re.IGNORECASE)
		files = filter(test.search, files)
		
		if len(files) > 0:
			for file in files:
				fpath = "%s/%s" % (path, file)
				self.images.append(fpath)

	def run(self):
		sourceDir = scribus.fileDialog("Comic Directory", isdir=True)
		scribus.newDoc( self.pageSize, self.margins, scribus.PORTRAIT, 0, scribus.UNIT_MILLIMETERS, scribus.FACINGPAGES, scribus.FIRSTPAGERIGHT)

		for resource in os.walk(sourceDir):
			self.clean_up_and_queue(resource[0], resource[1], resource[2])

		scribus.gotoPage(1)

		test = re.compile("[0-9]{1,}\.(%s)$" % self.formats, re.IGNORECASE)
		files = filter(test.search, self.images)
		files.sort()

		nImages = len(files)

		if nImages % 4 > 0:
			print "not"
			numPages = ( ((nImages / 4) +1 ) * 4 )
		else:
			print ":p"
			numPages = nImages
		print numPages

		for page in range(1, numPages):
			scribus.newPage(-1)
		i = 1
		for file in files:
			scribus.gotoPage(i)
			self.createImagePage(file, "image_%s" % i)
			i = i + 1

		if os.path.isfile("%s/front_cover.jpg" % sourceDir):
			file = "%s/front_cover.jpg" % sourceDir
			scribus.newPage(1)
			scribus.gotoPage(1)
			self.createImagePage(file, "front_cover")

		if os.path.isfile("%s/back_cover.jpg" % sourceDir):
			file = "%s/back_cover.jpg" % sourceDir
			scribus.newPage(-1)
			scribus.gotoPage(scribus.pageCount())
			self.createImagePage(file, "back_cover")

		if os.path.isfile("%s/logo_cover.svg" % sourceDir):
			file = "%s/logo_cover.svg" % sourceDir
			scribus.gotoPage(1)
			scribus.placeSVG(file, 0, 0)

#		result = scribus.messageBox('Debug', "%s" % self._comicInfo)

		scribus.setInfo("Fernando Michelotti", "Comics", "description")
		scribus.zoomDocument(-100)
		scribus.saveDoc()

	def createImagePage(self, file, name):
		scribus.createImage(0, 0, 210, 297, name)
		scribus.loadImage( file, name)
		scribus.setScaleImageToFrame(True, True, name)

if __name__ == '__main__':
	comics = ComicsMaker()
	comics.run()

