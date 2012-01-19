"""
Automatic Pixel Art Generator or apag. 

A set of functions to autmatically create pixel art for games.
"""

__author__ = "Richard James"
__copyright__ = "Copyright 2012, Richard James"
__license__ = "FreeBSD"
__version__ = "0.0.5"
__maintainer__ = "Richard James"
__email__ = "richardjam13@gmail.com"
__status__ = "Development"

import pygame, sys, os, glob, math
from pygame.locals import *
from random import randint
import copy
import argparse

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
        
        WHITE = key_surface.map_rgb ((255, 255, 255))
        RED = key_surface.map_rgb ((255, 0, 0))
        GREEN = key_surface.map_rgb ((0, 255, 0))
        BLUE = key_surface.map_rgb ((0, 0, 255))
        BLACK = key_surface.map_rgb ((0, 0, 0))
        
        for row in range(0, height):
            for col in range(0, width):
                pixel = BLACK
                # White
                if key_array[col][row] == WHITE:
                    #100%
                    pixel = WHITE
                # Green
                elif key_array[col][row] == GREEN:
                    r = randint(0, 3) # 75%
                    if r in (0, 1, 2) :
                        pixel = GREEN
                # Red
                elif key_array[col][row] == RED:
                    r = randint(0, 3) # 50%
                    if r in (0, 1) :
                        pixel = RED
                # Blue
                elif key_array[col][row] == BLUE:
                    r = randint(0, 3) # 25%
                    if r == 0 :
                        pixel = BLUE
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
                    if input_array[col][row] != BLACK:
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
        PINK = input_surface.map_rgb ((255, 0, 255))
        # Add an outer skin and convert remaining black pixels to white
    
        for row in range(0, height):
            for col in range(0, width):
                if input_array[col][row] == BLACK:
                    count = self.get_count_of_surrounding_non_black_pixels(input_array, row, col, width, height, BLACK)
                    
                    if count > 0:
                        output_array[col][row] = PINK
                    else:
                        output_array[col][row] = input_array[col][row]
                        
                
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
        PINK = input_surface.map_rgb ((255, 0, 255))
        
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
                elif input_array[col][row] == PINK:
                    output_array[col][row] = BLACK	
                
                else:
                    output_array[col][row] = input_array[col][row]
        
        
        
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
    

def load_key_image_files(mode, keys):
        # determine names of the key files to load and them load them    
        key_surfaces = []
        list_of_file_names = []

        for key_name in keys:
            list_of_file_names.append(glob.glob(os.path.join(mode,key_name)))
        
        for file_names in list_of_file_names:
            for file_name in file_names:
                key_surfaces.append(pygame.image.load(file_name))
        return key_surfaces
    
    
def main():
    
    parser = argparse.ArgumentParser(description='Automatic Pixel Art Generator'+__version__,version=__version__)
    parser.add_argument('--mode',default="spaceships", choices=('spaceships','planets'), help='one of (spaceships, planets). Default is spaceships')
    parser.add_argument('--format',default="sheet", choices=('sheet','hbar','vbar','single'), help='sheet gives you an ouput filled with x*y images, hbar gives you a \
        row of images and vbar a column, single gives only a single image')
    parser.add_argument('--format-use-fill-number', action='store_true', default=True, help='use a specific number of images instead of filling the whole output')
    parser.add_argument('--format-fill-number', default=300, help='how many copies of the image you want on the format')
    parser.add_argument('--copies', default=1, help='')
    parser.add_argument('--output-width',default=100,help='width of a hbar or sheet format')
    parser.add_argument('--output-height',default=127,help='height of a vbar or sheet format')
    parser.add_argument('--keys',default=['key*.png'],nargs='+',help='')
    parser.add_argument('--art-width',default=32,help='')
    parser.add_argument('--art-height',default=32,help='')
    parser.add_argument('--skin',action='store_true',default=False,help='')
    parser.add_argument('--post-colouring',action='store_true',default=False,help='')
    parser.add_argument('--backround-colour',nargs=3,help='The background colour for colouring in the format RED GREEN BLUE')
    parser.add_argument('--skin-colour',nargs=3,help='The skin colour for colouring in the format RED GREEN BLUE')
    
    args = parser.parse_args()
    print (args)
    pygame.init()
    
    if args.format == "sheet":    
        key_surfaces = load_key_image_files(args.mode, args.keys)
        
        # create the output sheet
        if not args.format_use_fill_number:
            sheet_width = args.output_width
            sheet_height = args.output_height
        else:
            square = int(math.ceil(math.sqrt(args.format_fill_number)))
            sheet_width =  square * args.art_width
            sheet_height = square * args.art_height

        final_surface = pygame.Surface((sheet_width, sheet_height))
        final_surface.fill(pygame.color.Color('white'))

        # calculate number of images to generate
        columns = sheet_width / args.art_width
        rows = sheet_height / args.art_height
        # 800 * 600 fits 18 * 25 (32*32) images on a sheet
        count = 1
        if not args.format_use_fill_number:
            total = rows * columns
        else:
            total = args.format_fill_number
        total = total * 1.0
        
        # values for random number generation
        previous = 0
        r = 0
        
        # create multiple images
        for y in range(0, rows):
            for x in range(0, columns):
                if args.format_use_fill_number and count > args.format_fill_number:
                    break

                spaceship = SpaceShipGenerator()

                print ("generating image %s of %s | %.2f%%" % (count, total, (count / total) * 100) )

                count += 1

                while (r == previous and len(key_surfaces) > 1):
                    r = randint(0, len(key_surfaces)-1)
                display_surface = spaceship.proc_gen(key_surfaces[r])
                previous = r
                display_surface = spaceship.clean_pixels(display_surface)
                if args.skin:
                    display_surface = spaceship.skin_image(display_surface)
        
                if args.post_colouring:
                    display_surface = spaceship.colour_pixels(display_surface)
                display_surface = spaceship.mirror_image_left_to_right(display_surface)
                final_surface = spaceship.paste_onto_final(display_surface, final_surface, x*32, y*32)
            if args.format_use_fill_number and count > args.format_fill_number:
                break
        
        pygame.image.save(final_surface, "output.png")
    elif args.format == "hbar":
        pass
    elif args.format == "vbar":
        pass
    elif args.format == "single":
        pass
    
    
    
if __name__ == '__main__':
    from timeit import Timer
    t = Timer("main()", "from __main__ import main")
    print (t.timeit(number=1))
