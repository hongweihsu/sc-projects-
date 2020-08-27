"""
File: stanCodoshop
Name: Dennis Hsu

SC101 - Assignment3
Adapted from Nick Parlante's Ghost assignment by
Jerry Liao.

-----------------------------------------------

The function of the program is to reproduce an image by removing unexpected part such as uncertain people or object,
it needs some images as row materials, which took at the same frame and the same perspective, moreover, it should be
better if all materials took in closing period so that the light from sky will not change dramatically between different
materials.

listing the process of the program:

01-1. Get pixels at every position (x, y) from every material picture.
01-2. Store those pixels as values and position as key in an dictionary.

02-1. Input one key value pair to function: get_best_pixel.
02-2. The k, v pair of position and pixels will be used to get mean RGB and calculate color distance for each pixel.
02-3. Only a pixel will be replaced at a time.

03-1. After running through every key (position), all pixels should be best one (min color distance).

"""

import os
import sys
import math
import time
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns color distance between pixel and mean RGB value

    Input:
        pixel (Pixel): pixel with RGB values to be compared
        red (int): average red value across all images
        green (int): average green value across all images
        blue (int): average blue value across all images

    Returns:
        dist (int): color distance between red, green, and blue pixel values

    """

    color_distance = math.sqrt(
        (pixel.red - red) ** 2 + (pixel.green - green) ** 2 + (pixel.blue - blue) ** 2)

    return color_distance


def get_average(pixels):
    """
    Given a list of pixels, finds the average red, blue, and green values

    Input:
        pixels (List[Pixel]): list of pixels to be averaged
    Returns:
        rgb (List[int]): list of average red, green, blue values across pixels respectively

    Assumes you are returning in the order: [red, green, blue]

    """
    rgb_avg = []  # a list used to store average RGB value.
    red_sum = 0
    green_sum = 0
    blue_sum = 0
    for i in range(len(pixels)):
        red_sum += pixels[i].red
        green_sum += pixels[i].green
        blue_sum += pixels[i].blue

    red_avg = red_sum / len(pixels)
    green_avg = green_sum / len(pixels)
    blue_avg = blue_sum / len(pixels)

    rgb_avg.append(red_avg)
    rgb_avg.append(green_avg)
    rgb_avg.append(blue_avg)

    return rgb_avg  # a list consist of [mean_r, mean_g, mean_b] of a specific position (x, y).


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest
    distance from the average red, green, and blue values across all pixels.

    Input:
        pixels (List[Pixel]): list of pixels to be averaged and compared
    Returns:
        best (Pixel): pixel closest to RGB averages

    """

    mean_rgb = get_average(pixels)  # get_average will return a list contains [mean_r, mean_g, mean_b].
    dist_of_pixels = []  # each pixel that has same position (x, y) can determine a distance value from their
    # mean_rgb, using this list to store those values.

    for i in pixels:
        distance = get_pixel_dist(i, mean_rgb[0], mean_rgb[1], mean_rgb[2])
        dist_of_pixels.append(distance)

    min_dist = min(dist_of_pixels)  # get the minimal value from [dist of pixels].
    best_pixel_index = dist_of_pixels.index(min_dist)  # check which pixel has min distance at the specific position.
    best_pixel = pixels[best_pixel_index]  # get best pixel from pixels.
    return best_pixel


def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    t0 = time.time()
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)  # set a blank board with same width and height as original photo.

    ######## YOUR CODE STARTS HERE #########
    pixel_same_position = {}  # a dict stores positions tuple (x, y) as key and list [pixel] as value.

    """
    Get pixels which have same position but from different images.
    """
    for i in images:
        for x in range(i.width):
            for y in range(i.height):
                pixel = i.get_pixel(x, y)
                if not (x, y) in pixel_same_position:  # if key (x, y) have not be created
                    pixel_same_position[(x, y)] = [pixel]
                else:
                    pixel_same_position[(x, y)].append(pixel)

    """
    Replace pixel through every position from blank one to correct one.
    
    Since the method 1 is a triple for loop, which cause more time consuming, I develop the method 2 to reduce total
    needed in running this program. On my local site for running photos in 'clock-tower', method 1 takes almost 23s to 
    finish this program while method 2 only takes 7s to finish the same code block. However, although method 2 is more 
    efficiency and scalable, method 1 still has advantages of readability and more intuition in my view.
    """

    # This is method 1 : O(n^3)
    # for i in images:
    #     for x in range(i.width):
    #         for y in range(i.height):
    #             best_pixel = get_best_pixel(pixel_same_position[x, y])
    #             new_pixel = result.get_pixel(x, y)
    #             new_pixel.red = best_pixel.red
    #             new_pixel.green = best_pixel.green
    #             new_pixel.blue = best_pixel.blue

    # # This is method 2 : O(n^2)
    best_pixels = list(map(get_best_pixel, list(pixel_same_position.values())))
    for x in range(images[0].width):
        for y in range(images[0].height):
            new_pixel = result.get_pixel(x, y)
            new_pixel.red = best_pixels[x * images[0].height + y].red
            new_pixel.green = best_pixels[x * images[0].height + y].green
            new_pixel.blue = best_pixels[x * images[0].height + y].blue

    ######## YOUR CODE ENDS HERE ###########
    print("Displaying image!")
    t1 = time.time()
    time_consume = t1 - t0
    print('time_consuming :', time_consume, 's')
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]  # input file directory
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])  # get a list consist of images.
    solve(images)


if __name__ == '__main__':
    main()
