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

