# Photo-arrange
This script arranges multiple photos on A4 pages. By default, it automatically calculates the optimal number of photos per page with 1 cm margins around the page and 0.5 cm spacing between photos. If all photos don't fit on a single page, the script will create additional pages.
## Requirements
To use this script, you need to install the following Python libraries:
```
pip install pillow reportlab
```

## Usage
1. Place all photos in a single folder
2. Run the script, specifying the path to the folder with photos:
```
python photo_arrange.py /path/to/photos/folder
```

To specify exact photo dimensions in centimeters, use the `--width` and `--height` parameters:
```
python photo_arrange.py /path/to/photos/folder --width 4 --height 5
```
This will create photos that are 4x5 cm in size.

3. The script will create PDF files named ready_01.pdf, ready_02.pdf, etc. in the specified folder 
