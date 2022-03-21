# Fatou Set Visualizer

**![Uploading -0.63 + 0.44i Set.png…]()

NOTE: Please look at the 'set_images' folder for images of the Fatou sets!**

Uses the Matplotlib python library and custom complex number functionality to graph the Fatou set of a general complex function.

The **Fatou set** of a complex function is the set of all complex numbers for which, when the function is applied to the value recursively, it remains bounded. Say the function being studied is f(z) = z^2. Say we start with the number 1.

f(0.5) = 0.5^2 = 0.25        
f(0.25) = 0.25^2 = 0.0625         
f(0.0625) = 0.0625^2 = 0.003906        
...      

It is clear that the function is bounded when applied recursively when the initial z = 0. Therefore, we can say that 0 is in the Fatou set of z^2. Say we choose z = 2

f(2) = 2^2 = 4        
f(4) = 4^2 = 16       
f(16) = 16^2 = 256        
...

This tends towards infinity when the initial z = 2. Therefore, we can say that 2 is not in the Fatou set. Say we choose a complex number, such as z = i

f(i) = i^2 = -1       
f(-1) = (-1)^2 = 1        
f(1) = 1^2 = 1        
...

This remains bounded, showing that i is in the Fatou Set. Repeating this process for all values in the complex plane of interest yields the Fatou set of the complex function.

Included with the program is example Fatou Sets for the following functions:

f(z) = z^2        
f(z) = z^2 + -0.12 + 0.77i        
f(z) = z^2 + -0.63 + 0.44i        


Along with this is the titular Mandelbrot set. To generate this set, the initial z value is fixed at zero. The complex function followed is f(z) = z^2 + c, where each coordinate point is plugged in as c and run recursively. If the sequence remains bounded, the point is displayed.

Included with the file is a class representing a complex number. This library allows you to easily take the sine, cosine, tangent, conjugate, and inverse of a given complex number, as well as general arithmetic and exponentiation. The library allows for the easy creation of complex functions. In the program, the comp_func() function is the Riemann Zeta function.

Below is the Mandelbrot Set and my favorite Fatou Set.

![Mandelbrot Set](https://user-images.githubusercontent.com/28418992/159028980-ad88e15d-1456-4b17-a304-dba110998db4.png)

![- 63 + 0 44i Set](https://user-images.githubusercontent.com/28418992/159029012-411b3f81-865d-475e-aede-8cb609053479.png)
