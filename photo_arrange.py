#!/usr/bin/env python3
import os
import sys
import math
from PIL import Image
import argparse
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm, cm
from reportlab.lib.pagesizes import A4

def resize_and_arrange_photos(input_folder, photo_width_cm=None, photo_height_cm=None):
    # Check if folder exists
    if not os.path.exists(input_folder) or not os.path.isdir(input_folder):
        print(f"Error: Folder '{input_folder}' does not exist or is not a directory")
        return
    
    # Get all image files from the folder
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']
    image_files = []
    
    for file in os.listdir(input_folder):
        file_path = os.path.join(input_folder, file)
        if os.path.isfile(file_path) and os.path.splitext(file)[1].lower() in image_extensions:
            image_files.append(file_path)
    
    if not image_files:
        print(f"No image files found in '{input_folder}'")
        return
    
    print(f"Found {len(image_files)} image files")
    
    # A4 dimensions
    a4_width, a4_height = A4  # (595.2755905511812, 841.8897637795277) points
    
    # Define margins and spacing
    page_margin = 1 * cm  # 1 cm margin on all sides
    photo_spacing = 0.5 * cm  # 0.5 cm spacing between photos
    
    # Available space for images
    available_width = a4_width - 2 * page_margin
    available_height = a4_height - 2 * page_margin
    
    # Set photo dimensions
    if photo_width_cm and photo_height_cm:
        # Use user-specified dimensions
        photo_width = photo_width_cm * cm
        photo_height = photo_height_cm * cm
        print(f"Using custom photo size: {photo_width_cm}x{photo_height_cm} cm")
    else:
        # Default to 4 photos per row
        photo_width = (available_width - 3 * photo_spacing) / 4
        photo_height = photo_width  # Square by default
        print("Using default photo size")

    # Calculate how many photos can fit on a page
    photos_per_row = max(1, int((available_width + photo_spacing) / (photo_width + photo_spacing)))
    photos_per_column = max(1, int((available_height + photo_spacing) / (photo_height + photo_spacing)))
    
    print(f"Photos per row: {photos_per_row}, Photos per column: {photos_per_column}")
    
    # Calculate total pages needed
    photos_per_page = photos_per_row * photos_per_column
    total_pages = math.ceil(len(image_files) / photos_per_page)
    
    # Create PDF pages
    for page_num in range(total_pages):
        output_file = os.path.join(input_folder, f"ready_{page_num+1:02d}.pdf")
        c = canvas.Canvas(output_file, pagesize=A4)
        
        # Process images for current page
        start_idx = page_num * photos_per_page
        end_idx = min(start_idx + photos_per_page, len(image_files))
        
        for i in range(start_idx, end_idx):
            # Calculate position for current image
            idx_on_page = i - start_idx
            row = idx_on_page // photos_per_row
            col = idx_on_page % photos_per_row
            
            x = page_margin + col * (photo_width + photo_spacing)
            y = a4_height - page_margin - (row + 1) * photo_height - row * photo_spacing
            
            try:
                # Open image
                img = Image.open(image_files[i])
                
                # Resize image to exact dimensions if specified, or preserve aspect ratio
                if photo_width_cm and photo_height_cm:
                    # Use exact dimensions
                    new_width = photo_width
                    new_height = photo_height
                else:
                    # Preserve aspect ratio by fitting within the calculated dimensions
                    img_width, img_height = img.size
                    aspect_ratio = img_width / img_height
                    
                    if aspect_ratio > 1:  # Landscape image
                        new_width = photo_width
                        new_height = photo_width / aspect_ratio
                        if new_height > photo_height:
                            new_height = photo_height
                            new_width = photo_height * aspect_ratio
                    else:  # Portrait image
                        new_height = photo_height
                        new_width = photo_height * aspect_ratio
                        if new_width > photo_width:
                            new_width = photo_width
                            new_height = photo_width / aspect_ratio
                
                # Save resized image temporarily
                temp_image_path = os.path.join(input_folder, f"temp_{i}.jpg")
                img = img.resize((int(new_width), int(new_height)), Image.Resampling.LANCZOS)
                img.save(temp_image_path, "JPEG")
                
                # Calculate centering within cell
                x_centered = x + (photo_width - new_width) / 2
                y_centered = y + (photo_height - new_height) / 2
                
                # Draw image on PDF
                c.drawImage(temp_image_path, x_centered, y_centered, width=new_width, height=new_height)
                
                # Delete temporary file
                os.remove(temp_image_path)
                
            except Exception as e:
                print(f"Error processing image {image_files[i]}: {str(e)}")
        
        c.save()
        print(f"Created page {page_num+1}/{total_pages}: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Arrange photos on A4 pages')
    parser.add_argument('folder', help='Folder containing photos')
    parser.add_argument('--width', type=float, help='Width of each photo in centimeters (e.g., 4)')
    parser.add_argument('--height', type=float, help='Height of each photo in centimeters (e.g., 5)')
    args = parser.parse_args()
    
    resize_and_arrange_photos(args.folder, args.width, args.height)

if __name__ == "__main__":
    main() 