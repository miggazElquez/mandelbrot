mandelbrot
=====

![mandelbrot set](/image/3000x3000-400.png)

Overview
-----

This program allow you to visualize the mandelbrot set, to save picture of it, and to explore the set in an interactive way.


Usage
----
You can use this program in two way : generating picture, or exploring the set.

###mode

If you want to use the interactive mode, just use `-i`, or `--interactive`.

If you prefer to generate one picture, you can specify the files to save it using `--files`, or `-f`.
You can specify multiple files : `-f file.png -f file2.png`. We use Pillow, so you can save to all the format supported by Pillow.
You can also show the picture, with `-s`.

###generic options

To specify the size of the picture, you can use `-x` and `-y`. The default is 500, 500 in interactive mode and 1000,1000 when you generate a picture.
For example, if you want an interactive mode with a bigger window, you can use `mandelbrot.py -i -x 800 -y 800`.

You can also decide the number of iteration used to determine if a point is part of the set, with `-n`.
If the value is higher, the set will be more precise, but it will take more time to compute.

If you specify `no-color`, you will have a picture only black and white.
