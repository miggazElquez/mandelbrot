import pygame
from mandelbrot import mandelbrot, make_img



def update_image(fen,x,y,n,no_color,size):
	valeurs = mandelbrot((x,y),n,size)
	image = make_img(valeurs,no_color)
	pygame_image = pygame.image.fromstring(image.tobytes(),(x,y),'RGB')
	return pygame_image

def new_size(pos,shape,x_size,y_size,up=True):
	x_min, x_max = x_size
	y_min, y_max = y_size
	delta_x = x_max - x_min
	pixel_x = delta_x / shape[0]
	delta_y = y_max - y_min
	pixel_y = delta_y / shape[1]
	x, y = pos
	x = x * pixel_x + x_min
	y = (shape[1] - y) * pixel_y + y_min	#les x vont en croissant, les y en décroissant

	if up:
		if x + delta_x/4 <= x_max:
			if x - delta_x/4 >= x_min:
				new_x_size = (x - delta_x/4,x + delta_x/4)
			else:
				new_x_size = (x_min,x_min + delta_x/2)
		else:
			new_x_size = (x_max - delta_x/2, x_max)

		if y + delta_y/4 <= y_max:
			if y - delta_y/4 >= y_min:
				new_y_size = (y - delta_y/4,y + delta_y/4)
			else:
				new_y_size = (y_min,y_min + delta_y/2)
		else:
			new_y_size = (y_max - delta_y/2, y_max)

		return new_x_size, new_y_size

	else:

		return (x_min - delta_x/2, x_max + delta_x/2), (y_min - delta_y/2, y_max + delta_y/2)
	





def main(x=500,y=500,n=400,no_color=False):
	pygame.init()
	fen = pygame.display.set_mode((x,y))
	pygame.key.set_repeat(500,30)

	marqueur = pygame.Surface((20,20))
	marqueur.fill((255,255,255))
	marqueur.set_colorkey((255,255,255))
	pygame.draw.rect(marqueur,(0,0,0),(9,0,2,20))
	pygame.draw.rect(marqueur,(0,0,0),(0,9,20,2))
	marqueur_rect = marqueur.get_rect()


	continuer = True
	x_size = [-2,2]
	y_size = [-2,2]
	changed = True
	pos = [0,0]

	step_x = x//50
	step_y = y//50
	image = None

	while continuer:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				continuer = False
				break

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_PAGEUP:
					x_size,y_size = new_size(pos,(x,y),x_size,y_size,True)
					changed = True
				elif event.key == pygame.K_PAGEDOWN:
					x_size,y_size = new_size(pos,(x,y),x_size,y_size,False)
					changed = True

				elif event.key == pygame.K_UP:
					pos[1] -= step_y
					if pos[1] < 0:
						pos[1] = 0
				elif event.key == pygame.K_DOWN:
					pos[1] += step_y
					if pos[1] > y:
						pos[1] = y
				elif event.key == pygame.K_RIGHT:
					pos[0] += step_x
					if pos[0] > x:
						pos[0] = x
				elif event.key == pygame.K_LEFT:
					pos[0] -= step_x
					if pos[0] < 0:
						pos[0] = 0

			elif event.type == pygame.MOUSEBUTTONDOWN:
				if event.button == pygame.BUTTON_LEFT:
					pos = list(event.pos)
				elif event.button == pygame.BUTTON_WHEELUP:
					x_size,y_size = new_size(event.pos,(x,y),x_size,y_size,True)
					changed = True
				elif event.button == pygame.BUTTON_WHEELDOWN:
					x_size,y_size = new_size(event.pos,(x,y),x_size,y_size,False)
					changed = True

			if changed:
				print("Updating...", end ="",flush=True)
				image = update_image(fen,x,y,n,no_color,(x_size,y_size))
				print('\b' * len("Updating..."),end="")
				print(' ' * len("Updating..."),end="")
				print('\b' * len("Updating..."),end="",flush=True)
				changed = False

			fen.blit(image,(0,0))
			marqueur_rect.center = pos
			fen.blit(marqueur,marqueur_rect)

			pygame.display.flip()


if __name__ == '__main__':
	main()