### CURRENT USAGE: python images_to_pdf.py output.pdf first_image second_image third_image ....
### e.g. python images_to_pdf.py sub-000000_MoCA.pdf 1.jpg second.png 3rd_page.jpg 
### This script will create a single pdf out of all images provided, in order of appearance in the user-provided list.

import sys
from PIL import Image

def images_to_pdf(image_list, output_pdf):
    # Open each image, convert it to RGB (if necessary), and add it to a list
    images = []
    for image_file in image_list:
        img = Image.open(image_file)
        if img.mode != 'RGB':
            img = img.convert('RGB')  # Convert non-RGB images to RGB
        images.append(img)

    # Save all images as a PDF
    if images:
        images[0].save(output_pdf, save_all=True, append_images=images[1:])
        print(f"PDF created successfully at {output_pdf}")
    else:
        print("No images to convert.")

if __name__ == "__main__":
    # Ensure there are enough arguments provided
    if len(sys.argv) < 3:
        print("Usage: python images_to_pdf.py output.pdf image1.png image2.jpg ...")
        sys.exit(1)

    # Parse command-line arguments
    output_pdf = sys.argv[1]
    image_list = sys.argv[2:]  # List of image files

    # Convert images to PDF
    images_to_pdf(image_list, output_pdf)
