import pygame, sys
from pygame.locals import *
from random import randint
import copy

"""
Spaceship generator

Part of the Automatic Pixel Art Generator or APAG

Version 0.0.2 as of 18 January 2012

"""

class SpaceShipGenerator():

	def __init__(self):	
		pass
	
	def proc_gen(self, key_surface):
		"""
		create image from the key
		"""
	
		# create pixel arrays from surface for work
		width = key_surface.get_width()
		height = key_surface.get_height()
		output_surface = pygame.Surface((width, height))
		key_array = pygame.PixelArray(key_surface)
		output_array = pygame.PixelArray(output_surface)
		for row in range(0, height):
			for col in range(0, width):
				pixel = (0, 0, 0)
				# White
				if key_array[col][row] == key_surface.map_rgb ((255, 255, 255)):
					#100%
					pixel = (255, 255, 255)
				# Green
				elif key_array[col][row] == key_surface.map_rgb ((0, 255, 0)):
					r = randint(0, 3) # 75%
					if r in (0, 1, 2) :
						pixel = (0, 255, 0)
				# Red
				elif key_array[col][row] == key_surface.map_rgb ((255, 0, 0)):
					r = randint(0, 3) # 50%
					if r in (0, 1) :
						pixel = (255, 0, 0)
				# Blue
				elif key_array[col][row] == key_surface.map_rgb ((0, 0, 255)):
					r = randint(0, 3) # 25%
					if r == 0 :
						pixel = (0, 0, 255)
				output_array[col][row] = pixel
	
		# copy pixel array to surface and delete pixel arrays
		display_surface = output_array.make_surface()
		del key_array
		del output_array
		return display_surface

	def get_count_of_surrounding_black_pixels(self, input_array, row, col, width, height, BLACK):
	
		#        col-1 col col+1
		# row - 1  +   +   +
		# row      +   +   +
		# row + 1  +   +   +
	
		# because SDL Pixel Arrays are zero indexed width and height are too big by one
		width -= 1
		height -= 1
	
		count = 0
		if row > 1 and col > 1:
			if input_array[col-1][row-1] == BLACK: count += 1
		else: count += 1
		if row > 1:
			if input_array[col][row-1] == BLACK: count += 1
		else: count += 1
		if col < width and row > 1:
			if input_array[col+1][row-1] == BLACK: count += 1
		else: count += 1
		if col > 1:
			if input_array[col-1][row] == BLACK: count += 1
		else: count += 1
		if col < width:
			if input_array[col+1][row] == BLACK: count += 1
		else: count += 1
		if col > 1 and row < height:
			if input_array[col-1][row+1] == BLACK: count += 1
		else: count += 1
		if row < width:
			if input_array[col][row+1] == BLACK: count += 1
		else: count += 1
		if col < width and row < height:
			if input_array[col+1][row+1] == BLACK: count += 1
		else: count += 1
		return count

	def get_count_of_surrounding_non_black_pixels(self, input_array, row, col, width, height, BLACK):
	
		#        col-1 col col+1
		# row - 1  +   +   +
		# row      +   +   +
		# row + 1  +   +   +
	
		# because SDL Pixel Arrays are zero indexed width and height are too big by one
		width -= 1
		height -= 1
	
		count = 0
		if row > 1 and col > 1:
			if input_array[col-1][row-1] is not BLACK: count += 1
		if row > 1:
			if input_array[col][row-1] is not BLACK: count += 1
		if col < width and row > 1:
			if input_array[col+1][row-1] is not BLACK: count += 1
		if col > 1:
			if input_array[col-1][row] is not BLACK: count += 1
		if col < width:
			if input_array[col+1][row] is not BLACK: count += 1
		if col > 1 and row < height:
			if input_array[col-1][row+1] is not BLACK: count += 1
		if row < height:
			if input_array[col][row+1] is not BLACK: count += 1
		if col < width and row < height:
			if input_array[col+1][row+1] is not BLACK: count += 1
		return count
	
	

	def clean_pixels(self, input_surface):
		"""
		Remove unwanted pixels from the created image
		"""
		# create pixel arrays from surface for work
		width = input_surface.get_width()
		height = input_surface.get_height()
		input_array = pygame.PixelArray(input_surface)
		output_surface = pygame.Surface((width, height))
		output_array = pygame.PixelArray(output_surface)
	
		BLACK = input_surface.map_rgb ((0, 0, 0))
		WHITE = input_surface.map_rgb ((255, 255, 255))
		
		for i in range(3):
			# Remove coloured pixels without enough surrounding coloured pixels
			for row in range(0, height):
				for col in range(0, width):
					if input_array[col][row] is not BLACK:
						count = self.get_count_of_surrounding_black_pixels(input_array, row, col, width, height, BLACK)
						
						if count > 5:
							output_array[col][row] = BLACK
						else:
							output_array[col][row] = input_array[col][row]
			
			
			# copy the output array to the input array * can't use pythons copy.copy()
			input_array = pygame.PixelArray(output_array.make_surface())
	
		# remove black pixels with too many surrounding coloured pixels
		for row in range(0, height):
			for col in range(0, width):
				if input_array[col][row] == BLACK:
					count = self.get_count_of_surrounding_non_black_pixels(input_array, row, col, width, height, BLACK)
					
					if count > 5:
						output_array[col][row] = WHITE
					else:
						output_array[col][row] = input_array[col][row]
		
		# copy pixel array to surface and delete pixel arrays
		output_surface = output_array.make_surface()	
		del input_array
		del output_array
		
		return output_surface
	
	def mirror_image_left_to_right(self, input_surface):
	
		# create pixel arrays from surface for work
		width = input_surface.get_width()
		height = input_surface.get_height()
		output_surface = pygame.Surface((width*2, height))
		input_array = pygame.PixelArray(input_surface)
		output_array = pygame.PixelArray(output_surface)
	
		for row in range(0, height):
	
			for col in range(0, width):
				output_array[col][row] = input_array[col][row]
				output_array[(width*2)-col-1][row] = input_array[col][row]
	
		# copy pixel array to surface and delete pixel arrays
		output_surface = output_array.make_surface()
		del input_array
		del output_array
		return output_surface
	
	def skin_image(self, input_surface):
		"""
		add a 1 pixel skin to the edge of the image
		"""
		# create pixel arrays from surface for work
		width = input_surface.get_width()
		height = input_surface.get_height()
		input_array = pygame.PixelArray(input_surface)
		output_surface = pygame.Surface((width, height))
		output_array = pygame.PixelArray(output_surface)
	
		BLACK = input_surface.map_rgb ((0, 0, 0))
		WHITE = input_surface.map_rgb ((255, 255, 255))	
		# Add an outer skin and convert remaining black pixels to white
	
		for row in range(0, height):
			for col in range(0, width):
				if input_array[col][row] == BLACK:
					count = self.get_count_of_surrounding_non_black_pixels(input_array, row, col, width, height, BLACK)
					
					if count > 0:
						output_array[col][row] = pygame.color.Color('black')
					else:
						output_array[col][row] = pygame.color.Color('white')
				
				elif input_array[col][row] == WHITE:
					output_array[col][row] = pygame.color.Color('black')	
				else:
					output_array[col][row] = input_array[col][row] 
		# copy pixel array to surface and delete pixel arrays
		output_surface = output_array.make_surface()	
		del input_array
		del output_array
		
		return output_surface
	
	def colour_pixels(self, input_surface):
		"""
		change the colours of the created image from the ones used in the key image
		"""
	
		# create pixel arrays from surface for work
		width = input_surface.get_width()
		height = input_surface.get_height()
		input_array = pygame.PixelArray(input_surface)
		output_surface = pygame.Surface((width, height))
		output_array = pygame.PixelArray(output_surface)
	
		BLACK = input_surface.map_rgb ((0, 0, 0))
		GREEN = input_surface.map_rgb ((0, 255, 0))
		RED = input_surface.map_rgb ((255, 0, 0))
		BLUE = input_surface.map_rgb ((0, 0, 255))
		WHITE = input_surface.map_rgb ((255, 255, 255))
		
		colour1 = None
		
		r = randint(0, 11)
	
		for row in range(0, height):
			for col in range(0, width):
				if r==0:
					colour1 = pygame.color.Color(16*col, 16*col, 255)
				elif r==1:
					colour1 = pygame.color.Color(16*col, 255, 16*col)
				elif r==2:
					colour1 = pygame.color.Color(255, 16*col, 16*col)
				elif r==3:
					colour1 = pygame.color.Color(255, 16*col, 255)
				elif r==4:
					colour1 = pygame.color.Color(255, 255, 16*col)
				elif r==5:
					colour1 = pygame.color.Color(16*col, 255, 255)
				elif r==6:
					colour1 = pygame.color.Color(16*col, 16*col, 0)
				elif r==7:
					colour1 = pygame.color.Color(16*col, 0, 16*col)
				elif r==8:
					colour1 = pygame.color.Color(0, 16*col, 16*col)
				elif r==9:
					colour1 = pygame.color.Color(0, 16*col, 0)
				elif r==10:
					colour1 = pygame.color.Color(0, 0, 16*col)
				elif r==11:
					colour1 = pygame.color.Color(16*col, 0, 0)
					
				
	
				if input_array[col][row] == GREEN:
					output_array[col][row] = colour1
				elif input_array[col][row] == RED:
					output_array[col][row] = colour1
				elif input_array[col][row] == BLUE:
					output_array[col][row] = colour1
				elif input_array[col][row] == WHITE:
					output_array[col][row] = BLACK	
				elif input_array[col][row] == BLACK:
					output_array[col][row] = WHITE	
		
		
		
		# copy pixel array to surface and delete pixel arrays
		output_surface = output_array.make_surface()	
		del input_array
		del output_array
		
		return output_surface
	
	def paste_onto_final(self, display_surface, final_surface, x, y):
		"""
		paste the created image on the final image so that multiple images can be in the final
		"""
		final_surface.blit(display_surface, (x, y))
		return final_surface
	
	


def main():
	pygame.init()

	# optional flags
	skinning = True
	coloured = True
	background_colour = pygame.color.Color('white')
	skinning_colour = pygame.color.Color('black')

	key_surface = []
	for num in range(7):
		file_name = "key" + str(num+1) + ".png"
		key_surface.append(pygame.image.load(file_name))
	
	final_surface = pygame.Surface((800, 600))
	final_surface.fill(pygame.color.Color('white'))
	
	# calculate number of images to generate
	rows = 12
	columns = 9
	# 800 * 600 fits 18 * 25 (32*32) images on a sheet
	count = 1
	total = rows * columns
	total = total * 1.0
	
	# values for random number generation
	previous = 0
	r = 0

	# create multiple images
	for y in range(0,columns):
		for x in range(0,rows):
			spaceship = SpaceShipGenerator()
			percent = (count / total) * 100
			print ("generating image %s of %s | %.2f%%" % (count, total, percent) )
			count += 1
			while (r == previous):
				r = randint(0, 3)
			display_surface = spaceship.proc_gen(key_surface[6])
			previous = r
			display_surface = spaceship.clean_pixels(display_surface)
			if skinning:
				display_surface = spaceship.skin_image(display_surface)

			if coloured:
				display_surface = spaceship.colour_pixels(display_surface)
			display_surface = spaceship.mirror_image_left_to_right(display_surface)
			final_surface = spaceship.paste_onto_final(display_surface, final_surface, x*32, y*32)
	
	pygame.image.save(final_surface, "output.png")
	
if __name__ == '__main__':
	from timeit import Timer
	t = Timer("main()", "from __main__ import main")
	print (t.timeit(number=1))
