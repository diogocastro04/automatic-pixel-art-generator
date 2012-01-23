"""
Automatic Pixel Art Generator or apag. 

A set of functions to autmatically create pixel art for games.
"""

__author__ = "Richard James"
__copyright__ = "Copyright 2012, Richard James"
__license__ = "FreeBSD"
__version__ = "0.0.6"
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
        
        WHITE = key_surface.map_rgb((255, 255, 255))
        RED = key_surface.map_rgb((255, 0, 0))
        GREEN = key_surface.map_rgb((0, 255, 0))
        BLUE = key_surface.map_rgb((0, 0, 255))
        BLACK = key_surface.map_rgb((0, 0, 0))
        
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
    
    def colour_pixels(self, input_surface, colours):
        """
        change the colours of the created image from the ones used in the key image
        """
    
        # create pixel arrays from surface for work
        width = input_surface.get_width()
        height = input_surface.get_height()
        input_array = pygame.PixelArray(input_surface)
        output_surface = pygame.Surface((width, height))
        output_array = pygame.PixelArray(output_surface)
    
        BLACK = input_surface.map_rgb((0, 0, 0))
        GREEN = input_surface.map_rgb((0, 255, 0))
        RED = input_surface.map_rgb((255, 0, 0))
        BLUE = input_surface.map_rgb((0, 0, 255))
        WHITE = input_surface.map_rgb((255, 255, 255))
        PINK = input_surface.map_rgb((255, 0, 255))
        
        for row in range(0, height):
            for col in range(0, width):
                if input_array[col][row] == GREEN:
                    output_array[col][row] = colours.green_colour
                elif input_array[col][row] == RED:
                    output_array[col][row] = colours.red_colour
                elif input_array[col][row] == BLUE:
                    output_array[col][row] = colours.blue_colour
                elif input_array[col][row] == WHITE:
                    output_array[col][row] = colours.white_colour	
                elif input_array[col][row] == BLACK:
                    output_array[col][row] = colours.background_colour	
                elif input_array[col][row] == PINK:
                    output_array[col][row] = colours.skin_colour
                
                else:
                    output_array[col][row] = input_array[col][row]
        
        
        
        # copy pixel array to surface and delete pixel arrays
        output_surface = output_array.make_surface()	
        del input_array
        del output_array
        
        return output_surface
    

class ColouringValues():
    
    def __init__(self, args):
        # convert
        # ['255', '255', '0']
        # to 
        # ( 255, 255, 0)
        variables = { 'background_colour' : args.background_colour, 'skin_colour' : args.skin_colour, 'green_colour' : args.green_colour, \
        'red_colour' : args.red_colour, 'blue_colour' : args.blue_colour, 'white_colour' : args.white_colour }
        
        default_colours = { 'background_colour' : 'black', 'skin_colour' : 'orange', 'green_colour' : 'green', \
        'red_colour' : 'red', 'blue_colour' : 'blue', 'white_colour' : 'white' }
        
        for name, value in variables.iteritems():
            if value != None:
                setattr(self, name, pygame.color.Color(int(value[0]), int(value[1]), int(value[2]) ) )
            else:
                setattr(self, name, pygame.color.Color(default_colours[name]) )
        
        


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

def paste_onto_final(display_surface, final_surface, x, y):
    """
    paste the created image on the final image so that multiple images can be in the final
    """
    final_surface.blit(display_surface, (x, y))
    return final_surface


def generate_single_image(args, key_surface_to_use, colours):

    spaceship = SpaceShipGenerator()

    display_surface = spaceship.proc_gen(key_surface_to_use)
    display_surface = spaceship.clean_pixels(display_surface)
    if args.skin:
        display_surface = spaceship.skin_image(display_surface)

    if args.post_colouring:
        display_surface = spaceship.colour_pixels(display_surface, colours)
    display_surface = spaceship.mirror_image_left_to_right(display_surface)
    
    return display_surface

def generate_image_sheet(args, key_surfaces, colours):

    # create the output sheet
    if not args.format_use_fill_number:
        sheet_width = args.output_width
        sheet_height = args.output_height
    else:
        square = int(math.ceil(math.sqrt(args.format_fill_number)))
        sheet_width =  square * args.art_width
        sheet_height = square * args.art_height

    final_surface = pygame.Surface((sheet_width, sheet_height))
    final_surface.fill(colours.background_colour)

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
            print ("generating image %s of %s | %.2f%%" % (count, total, (count / total) * 100) )

            count += 1

            while (r == previous and len(key_surfaces) > 1):
                r = randint(0, len(key_surfaces)-1)
            previous = r
            display_surface = generate_single_image(args, key_surfaces[r], colours)
            final_surface = paste_onto_final(display_surface, final_surface, x*32, y*32)
        if args.format_use_fill_number and count > args.format_fill_number:
            break
    
    return final_surface
        
def generate_image_single(args, key_surfaces, colours):
    # create the output sheet
    final_surface = pygame.Surface((args.art_width, args.art_height))
    final_surface.fill(colours.background_colour)

    # create image
    r = randint(0, len(key_surfaces)-1)
    display_surface = generate_single_image(args, key_surfaces[r], colours)
    final_surface = paste_onto_final(display_surface, final_surface, 0, 0)
    
    return final_surface    
    
def generate_image_hbar(args, key_surfaces, colours):
    # create the output sheet
    if not args.format_use_fill_number:
        sheet_width = args.output_width
        sheet_height = args.art_height
    else:
        sheet_width =  args.format_fill_number * args.art_width
        sheet_height = args.art_height

    final_surface = pygame.Surface((sheet_width, sheet_height))
    final_surface.fill(colours.background_colour)

    # calculate number of images to generate
    columns = sheet_width / args.art_width
    count = 1
    if not args.format_use_fill_number:
        total = columns 
    else:
        total = args.format_fill_number
    total = total * 1.0
    
    # values for random number generation
    previous = 0
    r = 0
    
    # create multiple images
    for x in range(0, columns):
        if args.format_use_fill_number and count > args.format_fill_number:
            break
        print ("generating image %s of %s | %.2f%%" % (count, total, (count / total) * 100) )
        count += 1
        while (r == previous and len(key_surfaces) > 1):
            r = randint(0, len(key_surfaces)-1)
        previous = r
        display_surface = generate_single_image(args, key_surfaces[r], colours)
        final_surface = paste_onto_final(display_surface, final_surface, x*32, 0)
    
    return final_surface

def generate_image_vbar(args, key_surfaces, colours):
    # create the output sheet
    if not args.format_use_fill_number:
        sheet_width = args.art_width
        sheet_height = args.output_height
    else:
        sheet_width =  args.art_width
        sheet_height = args.format_fill_number * args.art_height

    final_surface = pygame.Surface((sheet_width, sheet_height))
    final_surface.fill(colours.background_colour)

    # calculate number of images to generate
    rows = sheet_height / args.art_height
    count = 1
    if not args.format_use_fill_number:
        total = rows
    else:
        total = args.format_fill_number
    total = total * 1.0
    
    # values for random number generation
    previous = 0
    r = 0
    
    # create multiple images
    for y in range(0, rows):
        if args.format_use_fill_number and count > args.format_fill_number:
            break
        print ("generating image %s of %s | %.2f%%" % (count, total, (count / total) * 100) )
        count += 1
        while (r == previous and len(key_surfaces) > 1):
            r = randint(0, len(key_surfaces)-1)
        previous = r

        display_surface = generate_single_image(args, key_surfaces[r], colours)
        final_surface = paste_onto_final(display_surface, final_surface, 0, y*32)
    
    return final_surface

def output_file_name_generator(copies):
    if copies > 1:
        list_of_filenames = []
        for num in range(copies):
            file_name = 'output' + str(num) + '.png'
            list_of_filenames.append(file_name)
    else:
        list_of_filenames = ['output.png']
    return list_of_filenames

def add_output_format_options(parser):
    parser.add_argument('--format', default="sheet", choices=('sheet','hbar','vbar','single'), \
        help='sheet gives you an ouput filled with x*y images, hbar gives you a row of images and vbar a column, \
        single gives only a single image. Default is sheet')
    parser.add_argument('--format-use-fill-number', action='store_true', default=False, \
        help="use a specific number of images instead of filling the whole output. Default is don't do that")
    parser.add_argument('--format-fill-number', default=10, \
        help='how many copies of the image you want on the format. Default is 10')
    parser.add_argument('--copies', default=1, \
        help='Output n sets of the output, i.e. n sheets or n single images. Default is 1 set')
    parser.add_argument('--output-width',default=100, \
        help='width of a hbar or sheet format. Default is 100 pixels')
    parser.add_argument('--output-height',default=300, \
        help='height of a vbar or sheet format. Default is 300 pixels')
    
    return parser

def add_colouring_options(parser):
    parser.add_argument('--post-colouring', action='store_true', default=True, \
        help='Turn on colouring after an image is created, Default is colouring turned on')
    parser.add_argument('--no-post-colouring', action='store_false', default=True, dest='post_colouring', \
        help='Turn off colouring after an image is created')
    parser.add_argument('--background-colour', nargs=3, \
        help='The background colour for colouring in the format RED GREEN BLUE')
    parser.add_argument('--skin-colour', nargs=3, \
        help='The skin colour for colouring in the format RED GREEN BLUE')
    parser.add_argument('--green-colour', nargs=3, \
        help='The colour for colouring in the parts of the key image that are green. The format is RED GREEN BLUE')
    parser.add_argument('--red-colour', nargs=3, \
        help='The colour for colouring in the parts of the key image that are red. The format is RED GREEN BLUE')
    parser.add_argument('--blue-colour', nargs=3, \
        help='The colour for colouring in the parts of the key image that are blue. The format is RED GREEN BLUE')
    parser.add_argument('--white-colour', nargs=3, \
        help='The colour for colouring in the parts of the key image that are white. The format is RED GREEN BLUE')
    
    return parser


def main():
    
    parser = argparse.ArgumentParser(description='Automatic Pixel Art Generator '+__version__, version=__version__)
    parser.add_argument('--mode', default="spaceships", choices=('spaceships','planets'), help='one of (spaceships, planets). Default is spaceships')
    parser.add_argument('--keys', default=['key*.png'], nargs='+', \
        help="Names of the files to use as image keys. Default is 'key*.png'")
    parser.add_argument('--art-width', default=32, \
        help='in pixels the input width of the art. Default is 32 pixels')
    parser.add_argument('--art-height', default=32, \
        help='in pixels the input height of the art. Default is 32 pixels')
    parser.add_argument('--skin', action='store_true', default=False, \
        help="Add a 1 pixel skin to the output. Default is don't add a skin")

    parser = add_output_format_options(parser)
    parser = add_colouring_options(parser)

    args = parser.parse_args()
    
    ######################################
    # Override args for testing purposes
    #args.format = 'sheet'
    #args.format_use_fill_number = True
    #args.format_fill_number = 128
    #args.copies = 1
    
    # Finish args override
    
    #print (args)
    ######################################

    pygame.init()
    key_surfaces = load_key_image_files(args.mode, args.keys)
    colours = ColouringValues(args)
    
    current_copy = 1
    for output_file_name in output_file_name_generator(args.copies):
        
        final_surface = None
        
        if args.format == "sheet":
            final_surface = generate_image_sheet(args, key_surfaces, colours)
        elif args.format == "hbar":
            final_surface = generate_image_hbar(args, key_surfaces, colours)
        elif args.format == "vbar":
            final_surface = generate_image_vbar(args, key_surfaces, colours)
        elif args.format == "single":
            final_surface = generate_image_single(args, key_surfaces, colours)
        
        
        if final_surface != None:
            print ('writing copy %s/%s as %s' % (current_copy, args.copies, output_file_name))
            current_copy += 1
            pygame.image.save(final_surface, output_file_name)
        

    
    
    
if __name__ == '__main__':
    from timeit import Timer
    t = Timer("main()", "from __main__ import main")
    print ('Took %.6f seconds to complete.' % (t.timeit(number=1)))
