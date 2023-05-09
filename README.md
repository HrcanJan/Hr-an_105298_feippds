# CUDA - convert images to grayscale

### A fully functional project written in python to showcase a grayscale transformation of images using CUDA

The example is written in Python (version 3.10) using ```numba.cuda``` module(```pip install numba```). Run the ```main.py``` in terminal to automatically test the program.

In this code you will find a grayscale transformation of images using CPU and using GPU separately.
In the first part of the code is the CPU conversion, where we use a formula we found on [wikipedia](https://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale), that we used to manipulate image's RGB values to convert them to their gray counterparts by iterating over each pixel and changing its values.
In the second part of the code is the GPU conversion, where we have to use CUDA to solve our problem using GPU instead of CPU. We used the same [wikipedia](https://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale) formula to manipulate image's RGB values to convert them to its gray counterparts. Only this time, we used CUDA and GPU to gain parallel access to each pixel instead of using 2 for loops.
We then loaded images to test the functionality of our code. First we load a lone image, then we load many images.
After we are done converting them to grayscale, we save them somewhere on our computer.
Here are some of the results:

![Normal image](https://imgur.com/XSlCr77.png)
![Grayscale counterpart](https://imgur.com/unKPsXp.png)

![Normal image](https://imgur.com/yMRT5oq.png)
![Grayscale counterpart](https://imgur.com/deSQQ2K.png)

![Normal image](https://imgur.com/k5yQW9A.png)
![Grayscale counterpart](https://imgur.com/CPf8zFt.png)

Both algorithms complete their tasks successfully.
Finally, we measured the time of the conversion (both average and total time and for CPU and GPU and for the single image and many images):

```
CPU 1.2  s
Average time per photo:  1.2  s
GPU 78.24  s
Average time per photo:  78.24  s
CPU 6.56  s
Average time per photo:  2.18  s
GPU 288.65  s
Average time per photo:  96.22  s
```

In theory, the GPU conversion should be faster than CPU conversion, but because we are using an emulator for python to use CUDA, the GPU processes run very slow, especially because I have an older laptop.
In order for the processes to execute faster, you need to install CUDA toolkit https://developer.nvidia.com/cuda-toolkit-archive.
Installing that and running this code should prove, that GPU conversion is faster than CPU conversion.
That is all, thank you for reading!
