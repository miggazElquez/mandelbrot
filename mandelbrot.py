import argparse
from multiprocessing import Process, Queue
import os

import numpy as np
import PIL.Image

from color import color

MULTI = True

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


def mandelbrot(shape,nb_iteration,zone=((-2,2),(-2,2))):
	"""On passe la dimension de l'image (x,y) et le nombre d'itération"""
	taille_x = zone[0][1] - zone[0][0]
	taille_y = zone[1][1] - zone[1][0]
	delta_x = taille_x / shape[0]
	delta_y = taille_y / shape[1]
	result = []
	val = val_start = complex(zone[0][0],zone[1][1])
	for y in range(shape[1]):
		result.append([])
		for x in range(shape[0]):
			val += delta_x
			result[-1].append(divergence(val,nb_iteration))
		val = val_start - complex(0,delta_y*(y+1))
	return result


def valeurs_to_array(val,no_color=False):
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
	return array


def make_img(shape,nb_iteration,zone=((-2,2),(-2,2)),no_color=False):
	if MULTI:
		x,y = shape
		cpus = os.cpu_count()
		chunk_size = x//cpus
		last_chunk_size = x - chunk_size * (cpus-1)
		(x_min,x_max),y_ = zone
		delta_x = x_max - x_min
		pixel_x = delta_x / x
		chunk_size_value = chunk_size * pixel_x

		result = Queue()
		processes = []
		for i in range(cpus-1):
			zone_x = (i * chunk_size_value + x_min, (i+1) * chunk_size_value + x_min)
			process = Process(target=_worker,args=
				((chunk_size,y),
				nb_iteration,
				(zone_x,y_),
				no_color,result,i
				))
			process.start()
			processes.append(process)
		last_zone = (cpus-1) * chunk_size_value + x_min, x_max
		process = Process(target=_worker,
			args=((last_chunk_size,y),
			nb_iteration,
			(last_zone,y_),
			no_color,result,cpus-1
			))
		process.start()
		processes.append(process)
		vals = [result.get() for i in processes]
		for process in processes:
			process.join()
		final_array = np.hstack([i[0] for i in sorted(vals,key = lambda i:i[1])])
		return PIL.Image.fromarray(final_array)


	else:
		valeurs = mandelbrot(shape,nb_iteration,zone)
		array = valeurs_to_array(valeurs,no_color)
		return PIL.Image.fromarray(array)

def _worker(shape,nb_iteration,zone,no_color,result,n):
	valeurs = mandelbrot(shape,nb_iteration,zone)
	array = valeurs_to_array(valeurs,no_color)
	result.put((array,n))



def show(size,nb):
	"""for use in an interactive session"""
	make_img(size,nb).show()

def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('-i','--interactive',help="launch an interactive session in pygame",action="store_true")

	parser.add_argument("-x",help="number of pixels in x of the picture (-1 : default)",type=int,default=-1)
	parser.add_argument("-y",help="number of pixels in y of the picture (-1 : default)",type=int,default=-1)
	parser.add_argument("-n",help="number of iteration to determine if the series is divergent",type=int,default=400)

	parser.add_argument('--no-color',help="Picture in black and white only",action="store_true")

	parser.add_argument("-s","--show",help="Show the computed image", action="store_true")
	parser.add_argument("-f","--files",help="name of the files where you want to store the picture",action="append",default=[])

	args = parser.parse_args()
	if not args.interactive:
		if args.x == -1:
			args.x = 1000
		if args.y == -1:
			args.y = 1000
		if not args.files and not args.show:
			parser.error("If you're not in interactive mode, you don't want to see the picture, and you don't save it to a file, why are you running this program ?")
		image = make_img((args.x,args.y),args.n,no_color=args.no_color)
		for file in args.files:
			image.save(file)
		if args.show:
			image.show()
	else:
		if args.x == -1:
			args.x = 500
		if args.y == -1:
			args.y = 500

		import interactive
		interactive.main(args.x,args.y,args.n,args.no_color)

if __name__ == '__main__':
	main()



