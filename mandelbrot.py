import numpy as np
import PIL.Image


def divergence(c,nb_iteration):
	z = 0
	for i in range(nb_iteration):
		z = z**2 + c
		if abs(z) >2:
			return i+1
	return 0



def mandelbrot(shape,nb_iteration):
	"""On passe la dimension de l'image (x,y) et le nombre d'itération"""
	delta_x = 4/shape[0]
	delta_y = 4/shape[1]
	result = []
	val = val_start = -2+2j
	for y in range(shape[1]):
		result.append([])
		for x in range(shape[0]):
			val += delta_x
			result[-1].append(divergence(val,nb_iteration))
		val = val_start - complex(0,delta_y*(y+1))
	return result

def make_img1(val):
	result = []
	for y in val:
		result.append([])
		for val in y:
			if not val:
				result[-1].append([0,0,0])
			else:
				result[-1].append([255,255,255])
	array = np.array(result).astype(np.uint8)
	return PIL.Image.fromarray(array)

def show(size,nb):
	make_img1(mandelbrot(size,nb)).show()