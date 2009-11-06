#!/usr/bin/python
# -*- coding: utf8 -*-

import math
from gimpfu import *

def prepare_image(img, tdrawable, bgcolor=(255, 255, 255)):
	print "Filling color selection"

	width = tdrawable.width
	height = tdrawable.height

	active = pdb.gimp_image_get_active_layer(img)
	pdb.gimp_image_set_active_layer(img, img.layers[3])
	pdb.gimp_selection_grow(img, 5)
	
	draw = pdb.gimp_image_get_active_drawable(img)
	pdb.gimp_edit_bucket_fill(draw, FG_BUCKET_FILL, NORMAL_MODE, 100, 255, False, 1, 1)

	pdb.gimp_image_set_active_layer(img, active)

	gimp.displays_flush( )


register(
	"frustrado_sel",
	"Grows the selection and fills it at a predetermined layer",
	"Grows the selection and fills it at a predetermined layer",
	"Fernando Michelotti",
	"Fernando Michelotti",
	"2007-2007",
	"<Image>/Filters/Frustrado/Selection",
	"RGB*, GRAY*",
	[
    ],
	[],
	prepare_image)

main()
