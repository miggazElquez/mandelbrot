#! python -3.7-32
import pygame
from mandelbrot import mandelbrot, make_img



def update_image(fen,x,y,n,no_color,size):
	image = make_img((x,y),n,size,no_color)
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
	

def mouse_infos(pos,x,y,x_size,y_size):
	x_min, x_max = x_size
	y_min, y_max = y_size
	delta_x = x_max - x_min
	pixel_x = delta_x / x
	delta_y = y_max - y_min
	pixel_y = delta_y / y
	x_m, y_m = pos
	x_m = x_m * pixel_x + x_min
	y_m = (y - y_m) * pixel_y + y_min	#les x vont en croissant, les y en décroissant (oui, j'ai Ctrl+c, Ctrl+v)
	return _font.render(f"{x_m:e}, {y_m:e}",False,(0,0,0))



def main(x=500,y=500,n=400,no_color=False):
	pygame.init()
	fen = pygame.display.set_mode((x+105,y+40))
	pygame.key.set_repeat(500,15)

	marqueur = pygame.Surface((20,20))
	marqueur.fill((255,255,255))
	marqueur.set_colorkey((255,255,255))
	pygame.draw.rect(marqueur,(0,0,0),(9,0,2,20))
	pygame.draw.rect(marqueur,(0,0,0),(0,9,20,2))
	marqueur_rect = marqueur.get_rect()

	global _font
	_font = pygame.font.Font(None,21)

	continuer = True
	x_size = [-2,2]
	y_size = [-2,2]
	changed = True
	pos = [0,0]

	step_x = x//100
	step_y = y//100
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
				image = update_image(fen,x,y,n,no_color,(x_size,y_size))
				texte = f"""\
x :
 {x_size[0]: e},
 {x_size[1]: e}
y :
 {y_size[0]: e},
 {y_size[1]: e}

taille :
 {x_size[1] - x_size[0]: e},
 {y_size[1] - y_size[0]: e}
"""
				textes = [_font.render(line,True,(0,0,0)) for line in texte.split('\n')]
				size_infos = pygame.Surface((105,21*len(textes)))
				size_infos.fill((255,255,255))
				size_infos.set_colorkey((255,255,255))
				for ind, surf in enumerate(textes,start=1):
					size_infos.blit(surf,(0,21*ind))
				changed = False

			fen.fill((255,255,255))
			fen.blit(image,(0,0))
			marqueur_rect.center = pos
			fen.blit(marqueur,marqueur_rect)
			fen.blit(mouse_infos(pos,x,y,x_size,y_size),(10,y+10))
			fen.blit(size_infos,(x,0))

			pygame.display.flip()


if __name__ == '__main__':
	main()