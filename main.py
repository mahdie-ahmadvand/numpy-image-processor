import  argparse
import sys
from pathlib import Path

import cv2
import numpy as np


def parse_arguments():
    parser = argparse.ArgumentParser(

        description = "Simple image processing using Numpy"
    )
    parser.add_argument(
        "--input",
        required=True ,
        help="path to an input image or folder"
    )

    parser.add_argument(
        "--output",
        help="path for output image"
    )

    parser.add_argument(
        "--outdir" ,
        help="diretory for output files"
    )

    parser.add_argument(
        "--op" ,
        required=True ,
        choices=["gray","invert","brightness","split"] ,
        help="Image operation"
    )

    parser.add_argument(
        "--value",
        type=int , 
        help= "Brightness value from -255 to 255"
    )

    return parser.parse_args()

def gray_loop(img):
    height,width ,channels = img.shape
    gray = np.zeros((height,width),dtype=np.uint8)

    for y in range (height):
        for x in range (width):
            blue = img[y , x , 0]
            green = img[y,x,1]
            red = img[y,x,2]

            gray_value =(
                0.114 * blue +
                0.587 * green +
                0.299 * red
            )

            gray[y,x] = int(gray_value)

    return gray

def main():

    args = parse_arguments()

    input_Path = Path(args.input)

    if not input_Path.exists():
        print(f"Error: input path does not exist: {input_Path}")
        sys.exit(1)

    if not input_Path.is_file():
        print("Error: folder processing has not been implemented yet.")
        sys.exit(1)

    if args.op != "gray" :
        print("Error: currently only gray operation is implemented.")
        sys.exit(1)

    if args.output is None :
        print("Error: --output is required for gray operation.")
        sys.exit(1)

    img=cv2.imread(str(input_Path))
    if img is None:
        print(f"Error: cannot read image file: {input_Path}")
        sys.exit(1)

    gray_img = gray_loop(img)

    success = cv2.imwrite (args.output , gray_img)

    if not success :
        print(f"Error: could not save output image: {args.output}")
        sys.exit(1)

    print(f"Done: saved grayscale image to {args.output}")

if __name__ == "__main__":
    main()



 
    
