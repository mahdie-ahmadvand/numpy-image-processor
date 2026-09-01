import  argparse
import sys
from pathlib import Path
import time

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
        choices=["gray","gray_loop","invert","brightness","split"] ,
        help="Image operation"
    )

    parser.add_argument(
        "--value",
        type=int , 
        help= "Brightness value from -255 to 255"
    )

    parser.add_argument(
        "--benchmark",
        action="store_true",
        help="Mesure and desplay execution time"
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

def gray_numpy(img):

    gray = (
        img[:,:,0] * 0.114 +
        img[:,:,1] * 0.587 +
        img[:,:,2] * 0.299
    )
    return gray.astype(np.uint8)

def invert_image(img):

    return(255-img).astype(np.uint8)

def adjust_brightness(img,value):
    temp = img.astype(np.int16) + value

    clipped = np.clip(temp , 0 , 255)
    return clipped.astype(np.uint8)

def split_channels(img):
    b = img[:,:,0]
    g = img[:,:,1]
    r = img[:,:,2]
    return b, g, r

def main():
    args = parse_arguments()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error input_path dose not exist : {input_path}")
        sys.exit(1)
            
    if not input_path.is_file():
        print("Error:  folder processing has not been implemented yet.")
        sys.exit(1)

    img = cv2.imread(str(input_path))
    if img is None:
        print(f"Error cannot read image file(corropted or unsupported format): {input_path}")
        sys.exit(1)

    if args.op == "split":
      if args.outdir is None:
        print("Error: --outdir is required for 'split' operation")
        sys.exit(1)    
      out_dir = Path(args.outdir)
      out_dir.mkdir(parents=True, exist_ok=True)  

      start_time = time.perf_counter()
      b, g, r = split_channels(img)
      elapsed_time= time.perf_counter() - start_time  

    
      stem = input_path.stem

      cv2.imwrite(str(out_dir / f"{stem}_B.png"), b)
      cv2.imwrite(str(out_dir / f"{stem}_G.png"), g)
      cv2.imwrite(str(out_dir / f"{stem}_R.png"), r)

      if args.benchmark:
           print(f"⏱️ Execution Time for 'split': {elapsed_time:.6f} seconds")

      print(f"Done: split channels saved to {out_dir}/")
      return


    if args.output is None:
        print(f"Error:--output is required for '{args.op}' operation.")
        sys.exit(1)

    start_time = time.perf_counter()

    if args.op == "gray":
        result = gray_numpy(img)
    elif args.op == "gray_loop": 
        result = gray_loop(img)

    elif args.op == "invert":
        result = invert_image(img)

    elif args.op == "brightness":
        if args.value is None:
            print("Error:value is required for 'brightness' operatio    ")
            sys.exit(1)
        if not (-255<= args.value <= 255):
            print("Error:value must be between -255 and 255.")
            sys.exit(1)
        result = adjust_brightness(img, args.value)

    elapsed_time = time.perf_counter() - start_time    

    if args.benchmark:
        print(f"⏱️ Execution time for '{args.op}': {elapsed_time:.6f}seconds")
    success = cv2.imwrite(args.output, result)
    if not success:
        print(f"Error: codnot save output image to {args.output} ") 
        sys.exit(1)

    print(f"Done: saved {args.op} image to {args.output}")

if __name__ =="__main__":
        main()                  



