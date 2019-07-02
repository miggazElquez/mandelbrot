import argparse

import numpy as np
import PIL.Image

from color import color



def divergence(c,nb_iteration):
	z = 0
	for i in range(nb_iteration):
		z = z**2 + c
		if abs(z) > 2:
			return i+1
	return 0

try:
	from _mandelbrot import divergence
except ImportError:
	print("No cython version, the code will run slower")


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

def make_img(val,no_color):
	coef = 5
	result = []
	for y in val:
		result.append([])
		for val in y:
			if val:
				if no_color:
					result[-1].append((255,255,255))
				else:
					result[-1].append(color(val * coef))
			else:
				result[-1].append((0,0,0))
	array = np.array(result).astype(np.uint8)
	return PIL.Image.fromarray(array)

def show(size,nb):
	"""for use in an interactive session"""
	make_img1(mandelbrot(size,nb)).show()

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('-i','--interactive',help="launch an interactive session in pygame",action="store_true")

	parser.add_argument("-x",help="number of pixels in x of the picture",type=int,default=1000)
	parser.add_argument("-y",help="number of pixels in y of the picture",type=int,default=1000)
	parser.add_argument("-n",help="number of iteration to determine if the series is divergent",type=int,default=400)

	parser.add_argument('--no-color',help="Picture in black and white only",action="store_true")

	parser.add_argument("-s","--show",help="Show the computed image", action="store_true")
	parser.add_argument("-f","--files",help="name of the files where you want to store the picture",action="append",default=[])

	args = parser.parse_args()
	if not args.interactive:
		if not args.files and not args.show:
			parser.error("If you're not in interactive mode, you don't want to see the picture, and you don't save it to a file, why are you running this program ?")
		valeur = mandelbrot((args.x,args.y),args.n)
		image = make_img(valeur,args.no_color)
		for file in args.files:
			image.save(file)
		if args.show:
			image.show()

if __name__ == '__main__':
	main()



