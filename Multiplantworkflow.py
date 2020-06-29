#!/usr/bin/python

import sys, traceback
import cv2
import os
import re
import numpy as np
import argparse
import string
from plantcv import plantcv as pcv

### Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=True)
    parser.add_argument("-n", "--names", help="path to txt file with names of genotypes to split images into", required =False)
    parser.add_argument("-D", "--debug", help="Turn on debug, prints intermediate images.", action=None)
    args = parser.parse_args()
    return args

### Main workflow
def main():
    # Get options
    args = options()

    # Read image
    img, path, filename = pcv.readimage(args.image)

    pcv.params.debug=args.debug #set debug mode

    # STEP 1: Check if this is a night image, for some of these dataset's images were captured
    # at night, even if nothing is visible. To make sure that images are not taken at
    # night we check that the image isn't mostly dark (0=black, 255=white).
    # if it is a night image it throws a fatal error and stops the workflow.

    if np.average(img) < 50:
        pcv.fatal_error("Night Image")
    else:
        pass

    # STEP 2: Normalize the white color so you can later
    # compare color between images.
    # Inputs:
    #   img = image object, RGB colorspace
    #   roi = region for white reference, if none uses the whole image,
    #         otherwise (x position, y position, box width, box height)

    # white balance image based on white toughspot

    #img1 = pcv.white_balance(img=img,roi=(400,800,200,200))
    img1 = pcv.white_balance(img=img, mode='hist', roi=None)

    # STEP 3: Rotate the image
    # Inputs:
    #   img = image object, RGB color space
    #   rotation_deg = Rotation angle in degrees, can be negative, positive values 
    #                  will move counter-clockwise 
    #   crop = If True then image will be cropped to original image dimensions, if False
    #          the image size will be adjusted to accommodate new image dimensions 


    rotate_img = pcv.rotate(img=img1,rotation_deg=-1, crop=False)

    # STEP 4: Shift image. This step is important for clustering later on.
    # For this image it also allows you to push the green raspberry pi camera
    # out of the image. This step might not be necessary for all images.
    # The resulting image is the same size as the original.
    # Inputs:
    #   img    = image object
    #   number = integer, number of pixels to move image
    #   side   = direction to move from "top", "bottom", "right","left"

    shift1 = pcv.shift_img(img=img1, number=300, side='top')
    img1 = shift1

    # STEP 5: Convert image from RGB colorspace to LAB colorspace
    # Keep only the green-magenta channel (grayscale)
    # Inputs:
    #    img     = image object, RGB colorspace
    #    channel = color subchannel ('l' = lightness, 'a' = green-magenta , 'b' = blue-yellow)

    #a = pcv.rgb2gray_lab(img=img1, channel='a')
    a = pcv.rgb2gray_lab(rgb_img=img1, channel='a')

    # STEP 6: Set a binary threshold on the saturation channel image
    # Inputs:
    #    img         = img object, grayscale
    #    threshold   = threshold value (0-255)
    #    max_value   = value to apply above threshold (usually 255 = white)
    #    object_type = light or dark
    #       - If object is light then standard thresholding is done
    #       - If object is dark then inverse thresholding is done

    img_binary = pcv.threshold.binary(gray_img=a, threshold=120, max_value=255, object_type='dark')
    #img_binary = pcv.threshold.binary(gray_img=a, threshold=120, max_value=255, object_type'dark')
    #                                                   ^
    #                                                   |
    #                                     adjust this value

    # STEP 7: Fill in small objects (speckles)
    # Inputs:
    #    bin_img  = image object, binary. img will be returned after filling
    #    size = minimum object area size in pixels (integer)

    fill_image = pcv.fill(bin_img=img_binary, size=10)
    #                                          ^
    #                                          |
    #                           adjust this value

    # STEP 8: Dilate so that you don't lose leaves (just in case)
    # Inputs:
    #    img    = input image
    #    ksize  = kernel size
    #    i      = iterations, i.e. number of consecutive filtering passes

    #dilated = pcv.dilate(img=fill_image, ksize=1, i=1)
    dilated = pcv.dilate(gray_img=fill_image, ksize=2, i=1)

    # STEP 9: Find objects (contours: black-white boundaries)
    # Inputs:
    #    img  = image that the objects will be overlayed
    #    mask = what is used for object detection

    id_objects, obj_hierarchy = pcv.find_objects(img=img1, mask=dilated)
    #id_objects, obj_hierarchy = pcv.find_objects(gray_img, mask)

    # STEP 10: Define region of interest (ROI)
    # Inputs:
    #    img       = img to overlay roi
    #    x_adj     = adjust center along x axis
    #    y_adj     = adjust center along y axis
    #    h_adj     = adjust height
    #    w_adj     = adjust width
    # roi_contour, roi_hierarchy = pcv.roi.rectangle(img1, 10, 500, -10, -100)
    #                                                      ^                ^
    #                                                      |________________|
    #                                            adjust these four values

    roi_contour, roi_hierarchy = pcv.roi.rectangle(img=img1, x=200, y=190, h=2000, w=3000)

    # STEP 11: Keep objects that overlap with the ROI
    # Inputs:
    #    img            = img to display kept objects
    #    roi_contour    = contour of roi, output from any ROI function
    #    roi_hierarchy  = contour of roi, output from any ROI function
    #    object_contour = contours of objects, output from "Identifying Objects" function
    #    obj_hierarchy  = hierarchy of objects, output from "Identifying Objects" function
    #    roi_type       = 'partial' (default, for partially inside), 'cutto', or 'largest' (keep only largest contour)

    roi_objects, roi_obj_hierarchy, kept_mask, obj_area = pcv.roi_objects(img=img1, roi_contour=roi_contour, 
                                                                          roi_hierarchy=roi_hierarchy,
                                                                          object_contour=id_objects,
                                                                          obj_hierarchy=obj_hierarchy, 
                                                                          roi_type='partial')

    # STEP 12: This function take a image with multiple contours and
    # clusters them based on user input of rows and columns

    # Inputs:
    #    img               = An RGB image
    #    roi_objects       = object contours in an image that are needed to be clustered.
    #    roi_obj_hierarchy = object hierarchy
    #    nrow              = number of rows to cluster (this should be the approximate  number of desired rows in the entire image even if there isn't a literal row of plants)
    #    ncol              = number of columns to cluster (this should be the approximate number of desired columns in the entire image even if there isn't a literal row of plants)
    #    show_grid         = if True then a grid gets displayed in debug mode (default show_grid=False)

    clusters_i, contours, hierarchies = pcv.cluster_contours(img=img1, roi_objects=roi_objects, 
                                                             roi_obj_hierarchy=roi_obj_hierarchy, 
                                                             nrow=2, ncol=3)

    # STEP 13: This function takes clustered contours and splits them into multiple images,
    # also does a check to make sure that the number of inputted filenames matches the number
    # of clustered contours. If no filenames are given then the objects are just numbered
    # Inputs:
    #    img                     = ideally a masked RGB image.
    #    grouped_contour_indexes = output of cluster_contours, indexes of clusters of contours
    #    contours                = contours to cluster, output of cluster_contours
    #    hierarchy               = object hierarchy
    #    outdir                  = directory for output images
    #    file                    = the name of the input image to use as a base name , output of filename from read_image function
    #    filenames               = input txt file with list of filenames in order from top to bottom left to right (likely list of genotypes)

    # Set global debug behavior to None (default), "print" (to file), or "plot" (Jupyter Notebooks or X11)
    pcv.params.debug = "print"

    out = args.outdir
    names = args.names

    output_path, imgs, masks = pcv.cluster_contour_splitimg(rgb_img=img1, grouped_contour_indexes=clusters_i, 
                                                            contours=contours, hierarchy=hierarchies, 
                                                            outdir=out, file=filename, filenames=names)
    #output_path, imgs, masks = pcv.cluster_contour_splitimg(rgb_img, grouped_contour_indexes, contours, hierarchy)

# Call program
if __name__ == '__main__':
    main()
