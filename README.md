# CUDA - convert images to grayscale

### A fully functional project written in python to showcase a grayscale transformation of images using CUDA

The example is written in Python (version 3.10) using ```numba.cuda``` module(```pip install numba```). Run the ```main.py``` in terminal to automatically test the program.

In this code you will find a grayscale transformation of images using CPU and using GPU separately.
In the first part of the code is the CPU conversion, where we use ```opencv```'s ```.cvtColor``` to transform a BGR image to a gray image. This function uses CPU for the conversion.
In the second part of the code is the GPU conversion, where we have to use CUDA to solve our problem using GPU instead of CPU. After a quick search, we found a formula on [wikipedia](https://en.wikipedia.org/wiki/Grayscale#Converting_color_to_grayscale), that we used to manipulate image's RGB values to convert them to their gray counterparts.
We then loaded images to test the functionality of our code. First we load a lone image, then we load many images.
After we are done converting them to grayscale, we save them somewhere on our computer.
Here are some of the results:

![Normal image](./single_img/we_miss_him.png)
![Grayscale counterpart](./gray/we_miss_him.png)

![Normal image](./img/santaSogger.png)
![Grayscale counterpart](./gray/santaSogger.png)

![Normal image](./img/good3.PNG)
![Grayscale counterpart](./gray/good3.PNG)

Both algorithms complete their tasks successfully.
Finally, we measured the time of the conversion (both average and total time and for CPU and GPU and for the single image and many images):

```
CPU 0.02 s
Average time per photo:  0.02 s
GPU 66.1 s 
Average time per photo:  66.1 s
CPU 0.23 s
Average time per photo:  0.04 s
GPU 3030.78 s
Average time per photo:  505.13 s
```

In theory, the GPU conversion should be faster, but because we are using an emulator for python to use CUDA, the GPU processes run very slow, especially because I have an older laptop.
In order for the processes to execute faster, you need to install CUDA toolkit https://developer.nvidia.com/cuda-toolkit-archive.
Installing that and running this code should prove, that GPU conversion is faster than CPU conversion.
That is all, thank you for reading!
