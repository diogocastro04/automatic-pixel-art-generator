# Basic instructions #

Once downloaded you can run
```
python apag.py
```
From within the
```
automatic-pixel-art-generator
```
directory
It uses the key .png files to create the images. And outputs the result in a output.png file.

Default arguments in the command line options cause it to create a 100x300 pixel png file containing a sheet of 27 spaceships with no colouring options.

## key Image files ##

The key image files are in separate subdirectories. Directory structure is
```
/automatic-pixel-art-generator
apag.py
todo.txt
license.txt
    /spaceships
    key1.png
    key2.png
    ...
```

# Command Line Options #

## Basic options ##

### command line help ###

```
python apag.py -h
```

Will display a list of the options available

### version information ###

```
python apag.py -v
```

Will display the current version of the program

### mode ###

```
  --mode {spaceships,planets}
                        one of (spaceships, planets). Default is spaceships
```

```
python apag.py --mode spaceships
```

Note: currently spaceships are the only implemented mode

### keys ###

```
  --keys KEYS [KEYS ...]
                        Names of the files to use as image keys. Default is
                        'key*.png'
```

Can accept 1 or more arguments

```
python apag.py --keys key1.png key2.png
```

The search for these files starts in the key directories of each mode

### art width and height ###

```
  --art-width ART_WIDTH
                        in pixels the input width of the art. Default is 32
                        pixels
  --art-height ART_HEIGHT
                        in pixels the input height of the art. Default is 32
                        pixels
```

These actually don't do anything yet. May be removed in the future.

### skinning ###
```
  --skin                Add a 1 pixel skin to the output. Default is don't add
                        a skin
```

After generating the image it tries to add a 1 pixel thick skin around the edge of the picture.

## Output format options ##

### format type ###
```
  --format {sheet,hbar,vbar,single}
                        sheet gives you an ouput filled with x*y images, hbar
                        gives you a row of images and vbar a column, single
                        gives only a single image. Default is sheet
```

|![http://www.users.on.net/~richardjam13/apag-sheet-default.png](http://www.users.on.net/~richardjam13/apag-sheet-default.png)|
|:----------------------------------------------------------------------------------------------------------------------------|
|sheet format                                                                                                                 |
|![http://www.users.on.net/~richardjam13/apag-hbar-default.png](http://www.users.on.net/~richardjam13/apag-hbar-default.png)  |
|hbar format                                                                                                                  |
|![http://www.users.on.net/~richardjam13/apag-vbar-default.png](http://www.users.on.net/~richardjam13/apag-vbar-default.png)  |
|vbar format                                                                                                                  |
|![http://www.users.on.net/~richardjam13/apag-single-default.png](http://www.users.on.net/~richardjam13/apag-single-default.png)|
|single format                                                                                                                |


### format fill number ###
```
  --format-use-fill-number
                        use a specific number of images instead of filling the
                        whole output. Default is don't do that
```

Normally the program tries to fill in the format with as many images that will fit in the height and/or width supplied. If however you want to generate a specific number of images without specifying the height and/or width. You can use this option to generate as many or as little images as you want and the program will calculate the size of the output need for you.

```
  --format-fill-number FORMAT_FILL_NUMBER
                        how many copies of the image you want on the format.
                        Default is 10
```

```
python apag.py --format-use-fill-number --format-fill-number 100
```

Generates 100 images in default sheet format.

### copies ###
```
  --copies COPIES       Output n sets of the output, i.e. n sheets or n single
                        images. Default is 1 set
```

### output size ###
```
  --output-width OUTPUT_WIDTH
                        width of a hbar or sheet format. Default is 100 pixels
```
```
  --output-height OUTPUT_HEIGHT
                        height of a vbar or sheet format. Default is 300
                        pixels
```
## Colouring options ##

### post colouring ###
```
  --post-colouring      Turn on colouring after an image is created, Default
                        is colouring turned on
  --no-post-colouring   Turn off colouring after an image is created
```

Turns on or off post colouring routine. Which colours the image after generation.
Defaults to on.

```
python apag.py --no-post-colouring
```
To turn post colouring off.

### colour values ###

```
  --background-colour BACKGROUND_COLOUR BACKGROUND_COLOUR BACKGROUND_COLOUR
                        The background colour for colouring in the format RED
                        GREEN BLUE
  --skin-colour SKIN_COLOUR SKIN_COLOUR SKIN_COLOUR
                        The skin colour for colouring in the format RED GREEN
                        BLUE
  --green-colour GREEN_COLOUR GREEN_COLOUR GREEN_COLOUR
                        The colour for colouring in the parts of the key image
                        that are green. The format is RED GREEN BLUE
  --red-colour RED_COLOUR RED_COLOUR RED_COLOUR
                        The colour for colouring in the parts of the key image
                        that are red. The format is RED GREEN BLUE
  --blue-colour BLUE_COLOUR BLUE_COLOUR BLUE_COLOUR
                        The colour for colouring in the parts of the key image
                        that are blue. The format is RED GREEN BLUE
  --white-colour WHITE_COLOUR WHITE_COLOUR WHITE_COLOUR
                        The colour for colouring in the parts of the key image
                        that are white. The format is RED GREEN BLUE
```
These set the colour values for the colouring mode to use. If they are not set it will default values which map the colours 1-1 except for the skin.

The values are in the range 0-255 and a set of triplet values is required for the red green blue. Later alpha values will also be included requiring a quadruplet of values.

|![http://www.users.on.net/~richardjam13/apag-sheet-default.png](http://www.users.on.net/~richardjam13/apag-sheet-default.png)|
|:----------------------------------------------------------------------------------------------------------------------------|
|Example With Default Colouring                                                                                               |

```
python apag.py --background-colour 255 255 255 --skin-colour 0 0 0 --green-colour 255 165 0 --skin --blue-colour 139 90 43
```

|![http://www.users.on.net/~richardjam13/apag-sheet1.png](http://www.users.on.net/~richardjam13/apag-sheet1.png)|
|:--------------------------------------------------------------------------------------------------------------|
|Example of output with colours as used above                                                                   |