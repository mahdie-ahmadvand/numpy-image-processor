# numpy-image-processor
convert rgb picture to gray picture by numpy

## ⚡ Performance Benchmark

A performance comparison between the pure Python nested loop approach (`gray_loop`) and the vectorized NumPy implementation (`gray_numpy`) on the same image.

### Test Environment
- **Image Resolution:** 1920 × 1080 (Full HD)
- **Total Pixels:** 2,073,600 pixels

### Results

| Method | Implementation | Execution Time | Speedup Factor |
| :--- | :--- | :--- | :--- |
| `gray_loop` | Nested `for` loops (Pure Python) | ** 2.052552 s** | 1.0x (Baseline) |
| `gray_numpy` | Vectorized matrix operations (NumPy) | ** 0.006274 s** | **~360x faster** 🚀 |

### Why is NumPy significantly faster?
1. **Underlying C Code:** NumPy operations are executed at compiled C-speed without Python interpreter overhead.
2. **SIMD Vectorization:** Modern CPUs process multiple pixel arrays simultaneously via vector registers.
3. **Contiguous Memory:** NumPy utilizes continuous memory blocks, maximizing CPU cache hit rates.






### New items added to the project


1.    # def histogram:


+ import matplotlib.pyplot as plt


     parser.add_argument(
         "--op",
         required=True,
-        choices=["gray","gray_loop","invert","brightness","split"],
+        choices=["gray", "gray_loop", "invert", "brightness", "split", "histogram"],
         help="Image operation"
     )





 +++++++++++++++++++++++++ بخش کاملاً جدید +++++++++++++++++++++++++

def compute_histogram_1d(channel_2d):
    """محاسبه فراوانی هر مقدار روشنایی (0 تا 255) با NumPy خالص"""
    return np.bincount(channel_2d.ravel(), minlength=256)


def compute_histogram(img):
    """محاسبه هیستوگرام بر اساس تک‌کاناله (Grayscale) یا سه‌کاناله (BGR) بودن تصویر"""
    if len(img.shape) == 2 or img.shape[2] == 1:
        return {"Gray": compute_histogram_1d(img)}
    else:
        return {
            "Blue": compute_histogram_1d(img[:, :, 0]),
            "Green": compute_histogram_1d(img[:, :, 1]),
            "Red": compute_histogram_1d(img[:, :, 2]),
        }


def plot_and_save_histogram(hist_dict, save_path):
    """رسم هیستوگرام با Matplotlib و ذخیره به عنوان تصویر خروجی"""
    plt.figure(figsize=(8, 5))
    x = np.arange(256)

    colors = {
        "Blue": "blue",
        "Green": "green",
        "Red": "red",
        "Gray": "black",
    }

    for name, counts in hist_dict.items():
        plt.plot(
            x,
            counts,
            color=colors.get(name, "black"),
            label=f"{name} Channel",
            linewidth=1.5,
        )

    plt.title("Pixel Intensity Histogram")
    plt.xlabel("Pixel Intensity (0-255)")
    plt.ylabel("Frequency (Count)")
    plt.xlim([0, 255])
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(loc="upper right")
    plt.tight_layout()
    plt.savefig(str(save_path), dpi=300)
    plt.close()
 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++




     elif op == "split":
         result = split_channels(img)
+    elif op == "histogram":
+        result = compute_histogram(img)



         if args.op == "split":
             b, g, r = result
             cv2.imwrite(str(out_dir / f"{stem}_B.png"), b)
             cv2.imwrite(str(out_dir / f"{stem}_G.png"), g)
             cv2.imwrite(str(out_dir / f"{stem}_R.png"), r)
+        elif args.op == "histogram":
+            plot_path = out_dir / f"{stem}_hist.png"
+            plot_and_save_histogram(result, plot_path)
         else:
             out_file = out_dir / f"{stem}_{args.op}.png"
             cv2.imwrite(str(out_file), result)




         if args.benchmark:
            print(f"⏱️ Execution Time for 'split': {elapsed_time:.6f} seconds")
         print(f"Done: split channels saved to {out_dir}/")
         
+    elif args.op == "histogram":
+        if args.output is None:
+            print(f"Error: --output is required for 'histogram' operation.")
+            sys.exit(1)
+        result, elapsed_time = process_single_image(img, "histogram")
+        plot_and_save_histogram(result, args.output)
+
+        if args.benchmark:
+            print(f"⏱️ Execution time for 'histogram': {elapsed_time:.6f} seconds")
+        print(f"Done: saved histogram plot to {args.output}")
+
     else:
         if args.output is None:





**mistakes:** 

1. I didn’t run the file from the virtual environment.
2. I made some typos in the histogram . I was wroten histogeram



**Types of Color Spaces**

RGB Color Space:
In this color space, the color of each pixel is determined using three primary colors: Red, Green, and Blue. The intensity of each color is defined by an integer value ranging from 0 to 255, and mixing these three values produces the final pixel color.

BGR Color Space:
The mechanism is virtually identical to RGB. The only difference lies in the memory layout and storage order of the color bytes (Blue first, then Green, then Red).

HSV Color Space:
The HSV color space is designed to model human visual perception. It consists of three components:

H (Hue): Represents the color itself. It can be visualized as a 360-degree color wheel displaying the entire color spectrum (e.g., around 
0
∘
0 
∘
 
 corresponds to Red). A specific angle represents a specific color.
Advantage over RGB: In RGB, varying lighting conditions change all three R, G, and B channel values for a given pixel. In HSV, however, the Hue angle assigned to an object remains largely invariant under varying lighting conditions.
S (Saturation): Represents color purity, vividness, or concentration, represented on a numeric scale (typically mapped between 0 and 255 or 0% to 100%).
V (Value): Represents brightness or luminous intensity, mapped using a value from 0 to 255.
Use Case in Image Processing: HSV is widely used for color-based object tracking and color filtering/masking. You can define a target color range purely based on Hue (and Saturation/Value bounds); fluctuations in lighting will not easily confuse the detector, ensuring robust detection across different brightness levels.
Grayscale Color Space:
Grayscale (often referred to as black and white) allocates a single byte (8-bit depth, with values from 0 to 255) to each pixel, indicating brightness intensity.

Use Case: It significantly reduces computational overhead. It is ideal for preprocessing tasks—such as edge detection, thresholding, or contour detection—allowing costly full-color analysis to run only after regions of interest are located, thus speeding up the overall pipeline.



**OpenCV vs. Matplotlib Channel Ordering Note**


By default, OpenCV reads and stores images in BGR format.
Matplotlib, on the other hand, expects images in RGB format.
Consequently, if you load an image using cv2.imread() and directly display it using plt.imshow(), the Red and Blue channels are swapped, resulting in an unnatural, bluish tint. To fix this, you must convert the image first using cv2.cvtColor(img, cv2.COLOR_BGR2RGB).


   


2.    # def_HSV:


       parser.add_argument(
        "--op" ,
        required=True ,
         ⬅️ اضافه شدن hsv_split به لیست
    +    choices=["gray","gray_loop","invert","brightness","split","hsv_split","histogram"] ,
        help="Image operation"
    )


+ def split_hsv(img):
    
+ hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
+ h = hsv_img[:, :, 0]
+ s = hsv_img[:, :, 1]
+ v = hsv_img[:, :, 2]
+ return h, s, v


    **(process_single_image)**

+ elif op == "hsv_split":
+        result = split_hsv(img)


    **(process_folder)**

        if args.op =="split":            b, g, r = result
            cv2.imwrite(str(out_dir / f"{stem}_B.png"), b)
           cv2.imwrite(str(out_dir / f"{stem}_G.png"), g)
           cv2.imwrite(str(out_dir / f"{stem}_R.png"), r)

         ⬅️ بلاک شرطی جدید برای ذخیره کانال‌های H و S و V به صورت مجزا
+        elif args.op == "hsv_split":
+            h_ch, s_ch, v_ch = result
+            cv2.imwrite(str(out_dir / f"{stem}_H.png"), h_ch)
+            cv2.imwrite(str(out_dir / f"{stem}_S.png"), s_ch)
+            cv2.imwrite(str(out_dir / f"{stem}_V.png"), v_ch)

        elif args.op == "histogram":



      **(main)**


     ⬅️ بلاک شرطی جدید برای حالت تک‌تصویر
+    elif args.op == "hsv_split":
+       if args.outdir is None:
+            print("Error: --outdir is required for 'hsv_split' operation.")
+            sys.exit(1)
+        out_dir = Path(args.outdir)
+        out_dir.mkdir(parents=True, exist_ok=True)
+        result, elapsed_time = process_single_image(img, "hsv_split")
+        h_ch, s_ch, v_ch = result
+        cv2.imwrite(str(out_dir / f"{stem}_H.png"), h_ch)
+        cv2.imwrite(str(out_dir / f"{stem}_S.png"), s_ch)
+       cv2.imwrite(str(out_dir / f"{stem}_V.png"), v_ch)

+        if args.benchmark:
+            print(f"⏱️ Execution Time for 'hsv_split': {elapsed_time:.6f} seconds")
+        print(f"Done: HSV channels (H, S, V) saved to {out_dir}/")


**mistakes:** 


1.cv2.imwrite(str(out_dir /f"{stem}_H.png",h_ch))    #غلط 
   cv2.imwrite(str(out_dir /f"{stem}_H.png"),h_ch)    # درست


**Analysis and Interpretation of HSV Color Space Channels**

When converting the BGR color space to HSV (e.g., using --op hsv_split), three distinct grayscale images are generated, representing each channel:

H Channel (Hue): Represents the nature and “type” of the color (range 0–179 in OpenCV). In this channel, pixels with the same color—regardless of their lightness or darkness—will have the same brightness intensity.
S Channel (Saturation): Indicates the purity and vividness of the color. Brighter pixels in this channel represent pure, intense, and sharp colors, while dark or blackish areas represent dull, matte, white, gray, or neutral colors.
V Channel (Value): Simulates the intensity of light or brightness, which is very similar to a standard grayscale version of the image.



3. # def threshold :


    parser.add_argument(
        "--op",
        required=True,
+        choices=["gray", "gray_loop", "invert", "brightness""split""hsv_split",    "histogram", "threshold"],
        help="Image operation"
    )

+ def apply_threshold(img, thresh_val):
    """
    تبدیل تصویر به باینری (سیاه و سفید) با استفاده از cv2.threshold
    """
     اطمینان از تک‌کاناله بودن تصویر
+    if len(img.shape) == 3:
+        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
+    else:
+        gray = img

     اعمال آستانه‌گذاری باینری
+    ret, thresh_img = cv2.threshold(gray, thresh_val, 255, cv2.THRESH_BINARY)
+    return thresh_img



  **process_single_image**

+    elif op == "threshold":
+        result = apply_threshold(img, value)


   **main**

+       if args.op == "threshold":
+        if args.value is None:
+            print("Error: --value is required for 'threshold' operation (e.g. --value 128).")
+            sys.exit(1)
+       if not (0 <= args.value <= 255):
+            print("Error: --value for threshold must be between 0 and 255.")
+            sys.exit(1)






       **mistakes:**

1. cv2.cvtcolor   #غلط          cv2.cvtColor   #صحیح  
2. in the part of main I should write terms of threshold before part of 
cv2.imread     


 **describtion of def threshold**

 Thresholding is one of the most fundamental and widely used concepts in image processing and machine vision. Its main goal is to convert a continuous grayscale image into a pure binary image (black and white) in order to separate the subject or objects (Foreground) from the background (Background).

In the following, we will examine exactly what the cv2.threshold function does in OpenCV and how its mathematical mechanism and parameters work.

   