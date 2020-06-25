# python sampleworkflow.py -i C:\Users\adam\.spyder-py3\testpic.jpg -o C:\Users\adam\.spyder-py3\images -r results.txt -w -D 'print'




# !/usr/bin/python
import sys, traceback
import cv2
import numpy as np
import argparse
import string
from plantcv import plantcv as pcv


### Parse command-line arguments
def options():
    parser = argparse.ArgumentParser(description="Imaging processing with opencv")
    parser.add_argument("-i", "--image", help="Input image file.", required=True)
    parser.add_argument("-o", "--outdir", help="Output directory for image files.", required=False)
    parser.add_argument("-r", "--result", help="result file.", required=False)
    parser.add_argument("-w", "--writeimg", help="write out images.", default=False, action="store_true")
    parser.add_argument("-D", "--debug",
                        help="can be set to 'print' or None (or 'plot' if in jupyter) prints intermediate images.",
                        default=None)
    args = parser.parse_args()
    return args

#### Start of the Main/Customizable portion of the workflow.

### Main workflow
def main():
    # Get options
    args = options()

    pcv.params.debug = args.debug  # set debug mode
    pcv.params.debug_outdir = args.outdir  # set output directory

    # Read image
    img, path, filename = pcv.readimage(filename=args.image)

    # Convert RGB to HSV and extract the saturation channel
    s = pcv.rgb2gray_hsv(rgb_img=img, channel='s')

    # Threshold the saturation image
    s_thresh = pcv.threshold.binary(gray_img=s, threshold=85, max_value=255, object_type='light')

    # Median Blur
    s_mblur = pcv.median_blur(gray_img=s_thresh, ksize=5)
    s_cnt = pcv.median_blur(gray_img=s_thresh, ksize=5)

    # Convert RGB to LAB and extract the Blue channel
    #b = pcv.rgb2gray_lab(gray_img=img, channel='b')
    b = pcv.rgb2gray_lab(rgb_img=img, channel='b')

    # Threshold the blue image
    b_thresh = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')
    b_cnt = pcv.threshold.binary(gray_img=b, threshold=160, max_value=255, object_type='light')

    # Fill small objects
    # b_fill = pcv.fill(b_thresh, 10)

    # Join the thresholded saturation and blue-yellow images
    bs = pcv.logical_or(bin_img1=s_mblur, bin_img2=b_cnt)

    # Apply Mask (for VIS images, mask_color=white)
    #masked = pcv.apply_mask(rgb_img=img, mask=bs, mask_color='white')
    masked = pcv.apply_mask(img=img, mask=bs, mask_color='white')
    # Convert RGB to LAB and extract the Green-Magenta and Blue-Yellow channels
    masked_a = pcv.rgb2gray_lab(rgb_img=masked, channel='a')
    masked_b = pcv.rgb2gray_lab(rgb_img=masked, channel='b')

    # Threshold the green-magenta and blue images
    maskeda_thresh = pcv.threshold.binary(gray_img=masked_a, threshold=115, max_value=255, object_type='dark')
    maskeda_thresh1 = pcv.threshold.binary(gray_img=masked_a, threshold=135, max_value=255, object_type='light')
    maskedb_thresh = pcv.threshold.binary(gray_img=masked_b, threshold=128, max_value=255, object_type='light')

    # Join the thresholded saturation and blue-yellow images (OR)
    ab1 = pcv.logical_or(bin_img1=maskeda_thresh, bin_img2=maskedb_thresh)
    ab = pcv.logical_or(bin_img1=maskeda_thresh1, bin_img2=ab1)

    # Fill small objects
    ab_fill = pcv.fill(bin_img=ab, size=200)

    # Apply mask (for VIS images, mask_color=white)
    #masked2 = pcv.apply_mask(rgb_img=masked, mask=ab_fill, mask_color='white')
    masked2 = pcv.apply_mask(img=masked, mask=ab_fill, mask_color='white')
    # Identify objects
    id_objects, obj_hierarchy = pcv.find_objects(img=masked2, mask=ab_fill)

    # Define ROI
    roi1, roi_hierarchy= pcv.roi.rectangle(img=masked2, x=100, y=100, h=200, w=200)

    # Decide which objects to keep
    roi_objects, hierarchy3, kept_mask, obj_area = pcv.roi_objects(img=img, roi_contour=roi1, 
                                                               roi_hierarchy=roi_hierarchy, 
                                                               object_contour=id_objects, 
                                                               obj_hierarchy=obj_hierarchy,
                                                               roi_type='partial')

    # Object combine kept objects
    obj, mask = pcv.object_composition(img=img, contours=roi_objects, hierarchy=hierarchy3)

    ############### Analysis ################

    outfile=False
    if args.writeimg == True:
        outfile = args.outdir + "/" + filename

    # Find shape properties, output shape image (optional)
    shape_imgs = pcv.analyze_object(img=img, obj=obj, mask=mask)

    # Shape properties relative to user boundary line (optional)
    boundary_img1 = pcv.analyze_bound_horizontal(img=img, obj=obj, mask=mask, line_position=1680)

    # Determine color properties: Histograms, Color Slices, output color analyzed histogram (optional)
    color_histogram = pcv.analyze_color(rgb_img=img, mask=kept_mask, hist_plot_type='all')

    # Pseudocolor the grayscale image
    pseudocolored_img = pcv.visualize.pseudocolor(gray_img=s, mask=kept_mask, cmap='jet')

    # Write shape and color data to results file
    pcv.print_results(filename=args.result)

if __name__ == '__main__':
    main()
