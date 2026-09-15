import  argparse
import sys
import csv
from pathlib import Path
import time

import cv2
import numpy as np
import matplotlib.pyplot as plt

VALID_EXTENSIONS = {".jpg",".jpeg",".png",".bmp",".webp"}

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
        choices=["gray","gray_loop","invert","brightness","split",
                 "hsv_split","histogram","threshold","color_filter"] ,
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

    parser.add_argument(

        "--hsv-bounds",
        nargs=6,
        type=int,
        metavar=('H_MIN' , 'S_MIN' , 'V_MIN' , 'H_MAX' , 'S_MAX' , 'V_MAX'),
        help=  "6 values: H_min S_min V_min H_max S_max V_max"  
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

def split_hsv(img):
    hsv_img = cv2.cvtColor(img , cv2.COLOR_BGR2HSV)
    h=hsv_img[:,:,0]
    s=hsv_img[:,:,1]
    v=hsv_img[:,:,2]
    return h, s, v

def apply_threshold(img, thresh_val):

    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    ret , thresh_img = cv2.threshold(gray, thresh_val , 255 , cv2.THRESH_BINARY)
    return thresh_img 

def apply_color_filter(img, lower_hsv, upper_hsv):
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    lower_bound = np.array(lower_hsv, dtype=np.uint8)
    upper_bound = np.array(upper_hsv,dtype=np.uint8)

    mask = cv2.inRange(hsv , lower_bound, upper_bound)
    filtered_img = cv2.bitwise_and(img, img, mask=mask)

    active_pixels = cv2.countNonZero(mask)
    total_pixels = mask.shape[0] * mask.shape[1]
    mask_pct = (active_pixels / total_pixels)*100
    return filtered_img, mask_pct      


def compute_histogram_1d(channel_2d):
     """محاسبه فراوانی هر مقدار روشنایی (0 تا 255) با NumPy خالص"""
     return np.bincount(channel_2d.ravel(),minlength=256)

def compute_histogram(img):
    """محاسبه هیستوگرام بر اساس تک‌کاناله (Grayscale) یا سه‌کاناله (BGR) بودن تصویر"""
    if len (img.shape) == 2 or img.shape[2]==1:
        return {"Gray":compute_histogram_1d(img)}
    else :
        return{
            "Blue":compute_histogram_1d(img[:,:,0]),
            "Green":compute_histogram_1d(img[:,:,1]),
            "Red" : compute_histogram_1d(img[:,:,2])
        }

def plot_and_savehistogram(hist_dict,save_path):
       """رسم هیستوگرام با Matplotlib و ذخیره به عنوان تصویر خروجی"""
       plt.figure(figsize=(8,5))
       x= np.arange(256)

       colors ={
        "Blue": "blue",
        "Green": "green",
        "Red": "red",
        "Gray": "black",
       }   

       for name , counts in hist_dict.items():
           plt.plot(x,counts,color=colors.get(name,"black"),label=f"{name} chanel",
                    linewidth=1.5,)

        
       plt.title("pixel intensity histogram")
       plt.xlabel("pixel intensity (0-255)")  
       plt.ylabel("frequency (count)")
       plt.xlim([0,255])
       plt.grid(True,linestyle="--",alpha=0.5)
       plt.legend(loc="upper right")
       plt.tight_layout()
       plt.savefig(str(save_path),dpi=300)
       plt.close()

       
       
def process_single_image(img, op, value=None,hsv_bounds=None):

    start_time = time.perf_counter()

    if op == "gray":
        result = gray_numpy(img)
    elif op == "gray_loop": 
        result = gray_loop(img)

    elif op == "invert":
        result = invert_image(img)

    elif op == "brightness":
        result = adjust_brightness(img, value)

    elif op == "split":
        result = split_channels(img)

    elif op == "hsv_split":
        result = split_hsv(img)    

    elif op == "histogram" :
        result = compute_histogram(img)

    elif op == "threshold":
        result = apply_threshold(img, value)

    elif op == "color_filter" :
        lower_hsv = hsv_bounds[:3]
        upper_hsv = hsv_bounds[3:]
        result = apply_color_filter(img, lower_hsv, upper_hsv)    

    
    elapsed_time = time.perf_counter() - start_time
    return result, elapsed_time

    


def process_folder(folder_path, out_dir,args):
    image_files = [
        f for f in folder_path.iterdir()
        if f.is_file() and f.suffix.lower() in VALID_EXTENSIONS
    ]

    if not image_files:
        print(f"Warning: No valid image files found in {folder_path}")
        return

    out_dir.mkdir(parents=True , exist_ok=True)
    csv_path = out_dir / "log.csv"
    log_data = []
    print(f"Found {len(image_files)} images. Starting batch processing...")

    for img_path in image_files :
        img = cv2.imread(str(img_path))
        if img is None:
            print(f"Skipping corrupted file: {img_path.name}")
            continue

        h, w = img.shape[:2]
        c = img.shape[2] if len(img.shape) == 3 else 1
        dims = f"{w}*{h}*{c}"

        result, elapsed_time = process_single_image(img, args.op, args.value, args.hsv_bounds)

        stem = img_path.stem
        if args.op =="split":
            b, g, r = result

            cv2.imwrite(str(out_dir / f"{stem}_B.png"), b)
            cv2.imwrite(str(out_dir / f"{stem}_G.png"), g)
            cv2.imwrite(str(out_dir / f"{stem}_R.png"), r)

        elif args.op == "hsv_split":
            h_ch ,s_ch , v_ch = result
            cv2.imwrite(str(out_dir/f"{stem}_H.png"),h_ch) 
            cv2.imwrite(str(out_dir/f"{stem}_S.png"),s_ch)    
            cv2.imwrite(str(out_dir/f"{stem}_V.png"),v_ch)    
               

        elif args.op == "histogram":
            plot_path = out_dir / f"{stem}_hist.png"
            plot_and_savehistogram(result, plot_path)   


        elif args.op == "color_filter":
            filtered_img, pct = result
            out_file = out_dir / f"{stem}_filtered.png"
            cv2.imwrite(str(out_file), filtered_img)
            print(f"  [INFO] Color mask covers: {pct:.2f}% of the image.")

        else:
            out_file = out_dir / f"{stem}_{args.op}.png"
            cv2.imwrite(str(out_file), result)

        log_data.append([img_path.name, dims, args.op, f"{elapsed_time:.6f}"])
        print(f"  Processed: {img_path.name} ({dims}) in {elapsed_time:.4f}s")
        
    with open(csv_path, mode="w", newline="",encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename","dimensions","operation","execution_time_sec"])
        writer.writerows(log_data)

    print("\n✅ All images processed successfully!")
    print(f"📁 Output files and log saved to: {out_dir}/log.csv")
    
    
def main():
    args = parse_arguments()
    input_path = Path(args.input)

    if not input_path.exists():
        print(f"Error input_path dose not exist : {input_path}")
        sys.exit(1)
            
    if input_path.is_dir():
       if args.outdir is None:
            print("Error:  --outdir is required when processing a folder.")
            sys.exit(1)
       process_folder(input_path, Path(args.outdir), args)
       return


    if args.op == "brightness":
            if args.value is None:
                print("Error: --value is required for 'brightness' operation.")
                sys.exit(1)
            if not (-255 <= args.value <= 255):
                print("Error: --value must be between -255 and 255.")
                sys.exit(1)   

    
    if args.op == "threshold" :
    
        if args.value is None:
            print("Error: --value is required for 'threshold' operation (e.g. --value 128).")
            sys.exit(1)
    
        if not(0 <= args.value <= 255) :
                print("Error: --value for threshold must be between 0 and 255.")
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
        result, elapsed_time = process_single_image(img, "split")
        b, g, r = result
        stem = input_path.stem

        cv2.imwrite(str(out_dir / f"{stem}_B.png"), b)
        cv2.imwrite(str(out_dir / f"{stem}_G.png"), g)
        cv2.imwrite(str(out_dir / f"{stem}_R.png"), r)


    

    elif args.op == "hsv_split":
        if args.outdir is None :
            print("Error: --outdir is required for 'hsv_split' operation.")
            sys.exit(1)
        out_dir = Path(args.outdir) 
        out_dir.mkdir(parents=True, exist_ok=True)
        result, elapsed_time= process_single_image(img, "hsv_split")
        h_ch, s_ch, v_ch = result
        stem = input_path.stem

        cv2.imwrite(str(out_dir /f"{stem}_H.png"),h_ch)
        cv2.imwrite(str(out_dir /f"{stem}_S.png"),s_ch)
        cv2.imwrite(str(out_dir /f"{stem}_V.png"),v_ch)

        if args.benchmark:
            print(f"⏱️ Execution Time for 'hsv_split': {elapsed_time:.6f} seconds")
        print(f"Done: HSV channels (H, S, V) saved to {out_dir}/")

        
    elif args.op == "histogram" :  
        if args.output is None :
            print(f"Error: --output is required for 'histogram' operation.")
            sys.exit(1)
    
        result,elapsed_time =process_single_image(img,"histogram")
        plot_and_savehistogram(result,args.output)
    
        if args.benchmark:
           print(f"⏱️ Execution Time for 'histogram': {elapsed_time:.6f} seconds")
           print(f"Done: split channels saved to {args.output}/")


    elif args.op == "color_filter":
        if args.output is None:
            print("Error: --output is required for 'color_filter' operation.")
            sys.exit(1)  
        (filtered_img,pct), elapsed_time = process_single_image(
            img, "color_filter" , hsv_bounds=args.hsv_bounds
            )
        print(f"[INFO] Color mask covers: {pct:.2f}% of the image.")

        if args.benchmark:
            print(f"⏱️ Execution Time for 'color_filter': {elapsed_time:.6f} seconds")

        cv2.imwrite(args.output, filtered_img)   
        print(f"[SUCCESS] Saved output to {args.output}") 

    else:

        if args.output is None:
            print(f"Error:--output is required for '{args.op}' operation.")
            sys.exit(1)
        result, elapsed_time = process_single_image(img, args.op, args.value)        
   

        if args.benchmark:
           print(f"⏱️ Execution time for '{args.op}': {elapsed_time:.6f}seconds")
        success = cv2.imwrite(args.output, result)
        if not success:
            print(f"Error: codnot save output image to {args.output} ") 
            sys.exit(1)

        print(f"Done: saved {args.op} image to {args.output}")

if __name__ =="__main__":
        main()                  



