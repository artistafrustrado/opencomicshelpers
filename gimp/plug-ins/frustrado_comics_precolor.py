#!/usr/bin/python
# -*- coding: utf8 -*-

import math
from gimpfu import *

class ComicPage:
	def __init__(self, img, tdrawable):
		self.img = img
		self.tdrawable = tdrawable
		
		self.width = tdrawable.width
		self.height = tdrawable.height

		self.layers = {}
		self.main()		
		gimp.displays_flush( )


	def main(self):
    		self.img.disable_undo()
		self.convertRGB()
		self.prepareLineart()
		self.createLayer('Hightlight')	
		self.createLayer('Shadow')	
		self.createLayer('Color')	
		self.img.enable_undo()

	def convertRGB(self):
		draw = pdb.gimp_image_get_active_layer(self.img)
		index = pdb.gimp_drawable_is_indexed(draw)
		gray  = pdb.gimp_drawable_is_gray(draw)
		if (index) or (gray):
			pdb.gimp_image_convert_rgb(self.img)


	def createLayer(self, name):
		layer = gimp.Layer(self.img, name, self.width, self.height, RGBA_IMAGE, 100,  NORMAL_MODE)
		pdb.gimp_drawable_fill(layer, TRANSPARENT_FILL)
		pdb.gimp_image_add_layer(self.img, layer, -1)
		pdb.gimp_image_lower_layer(self.img, layer)
		self.layers[name] = layer

	def prepareLineart(self):
		pdb.gimp_selection_all(self.img)
		draw = pdb.gimp_image_get_active_drawable(self.img)
		pdb.gimp_edit_cut(draw)

		layerLineart = gimp.Layer(self.img, "Line Art", self.width, self.height, RGB_IMAGE, 100,  MULTIPLY_MODE)
		self.img.add_layer(layerLineart, 0)

		draw = pdb.gimp_image_get_active_drawable(self.img)
		layerLineart = pdb.gimp_edit_paste(draw, True)
		pdb.gimp_floating_sel_anchor(layerLineart)
		self.layers['Line Art'] = layerLineart

def prepare_image(img, tdrawable, bgcolor=(255, 255, 255)):
	print "Preping Image"
	cp = ComicPage(img, tdrawable)

register(
	"frustrado_comics_precolor",
	"Prepare a bitmap or grayscale ilustration file to be colored",
	"Prepare a bitmap or grayscale ilustration file to be colored",
	"Fernando Michelotti",
	"Fernando Michelotti",
	"2007-2008",
	"<Image>/Filters/Frustrado/Comics Precolor Automation",
	"RGB*, GRAY*",
	[
	],
	[],
	prepare_image)

main()
