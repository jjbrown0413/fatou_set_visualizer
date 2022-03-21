import os
import math
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Sets my favorite graph style.
plt.style.use("seaborn-notebook")

os.system("cls")

# Defines and implements functionality for complex numbers without using the complex library.
class Complex_Number():
    def __init__(self, real, im):
        # Sets the real and imaginary components of the complex number to numbers defined in the constructor.
        self.real = real
        self.im = im
        
        # Handles infinite values. TODO: Negative infinity might be necessary to parse.
        if abs(self.real) > 10000000:
            self.real = math.inf
        
        if abs(self.im) > 10000000:
            self.im = math.inf
        
    
    # Handles the addition operator with complex numbers.
    def __add__(self, a):
        if type(a) is Complex_Number:
            return Complex_Number(self.real + a.real, self.im + a.im)
    
    # Handles the multiplication operator with complex numbers. Uses FOIL.
    def __mul__(self, a):
        return Complex_Number(self.real * a.real - self.im * a.im, self.real * a.im + self.im * a.real)
    
    # Handles the subtraction operator with complex numbers.
    def __sub__(self, a):
        return Complex_Number(self.real - a.real, self.im - a.im)
        
    # Test if two complex numbers are equal.
    def __eq__(self, a):
        return self.real == a.real and self.im == a.im
        
    # Gets magnitude of the complex number using the pythagorean theorem.
    def mag(self):
        return math.sqrt(self.real ** 2 + self.im ** 2)
        
    # Gets the argument, or angle, of a complex number using inverse trig.
    def arg(self):
        return math.atan(self.im / self.real)
        
    # Gets the conjugate of the complex number.
    def conj(self):
        return Complex_Number(self.real, -self.im)

    # Scales the complex number by a certain factor.   
    def scale(self, num):
        return Complex_Number(self.real * num, self.im * num)
    
    # Inverts a complex number to be useful with division.
    def invert(self):
        try:
            top = self.conj()
            bottom = pow(self.real, 2) + pow(self.im, 2)
            return top.scale(1/bottom)
        except:
            return Complex_Number(math.inf, math.inf)
    
    # Divides complex numbers by multiplying by the reciprocal.
    def comp_div(self, a):
        return self * a.invert()
    
    # Raises a real number to a complex power. Uses the euler form of the complex number and converts it back.
    def exp(self, n):
        r = math.pow(math.e, self.real * math.log(n))
        theta = self.im * math.log(n)
        return euler_to_comp(r, theta)
    
    # Prints the string representation of a complex number: a + bi
    def str_out(self):
        return f"{self.real} + {self.im}i"

    # Tests if a complex number is sufficiently close to zero. 
    def is_zero(self):
        return abs(self.real) < 0.0001 and abs(self.im) < 0.0001

    # Tests if a complex number is sufficiently close to infinity or is infinity. 
    def is_pole(self):
        return self.real == math.inf or self.im == math.inf or abs(self.real) > 10000000 or abs(self.im) > 10000000 or math.isnan(self.real) or math.isnan(self.im)
        
    # Returns the sine of the complex number using: sin(a + bi) = sin(a) cosh(b) + (cos(a) sinh(b))i
    def sin(self):
        return Complex_Number(math.sin(self.real) * math.cosh(self.im), math.cos(self.real) * math.sinh(self.im))
    
    # Returns the cosine of a complex number using: cos(a + bi) = cos(a) cosh(b) - (sin(a) sinh(b))i
    def cos(self):
        return Complex_Number(math.cos(self.real) * math.cosh(self.im), - math.sin(self.real) * math.sinh(self.im))
    
    # Returns the tangent of a complex number.
    def tan(self):
        return self.sin() * self.cos().invert()
        
    # Raises a complex number to a real power. Uses the euler form of the complex number and converts back.
    def power(self, n):
        r = self.mag() ** n
        theta = self.arg() * n
        return euler_to_comp(r, theta)
            

# Sample implementation of a complex function. Completes the Riemann Zeta function for a given a.
def comp_func(a):
    l = [a.exp(n).invert() for n in range(1, 10000)]
    val = Complex_Number(0, 0)
    for e in l:
        print(val.str_out())
        val += e
    return val

# Converts the euler representation of a complex number (re^(ix)) to it's a + bi form.
def euler_to_comp(r, theta):
    real = r * math.cos(theta)
    im = r * math.sin(theta)
    return Complex_Number(real, im)

# Finds the critical points of a complex function. Includes it's zeros and poles.
def find_zero_poles():
    poi = []
    r = 1
    theta = 0
    while theta < math.pi * 2:
        num = euler_to_comp(r, theta)
        res = comp_func(num)
        if res.is_zero() or res.is_pole():
            is_dup = False
            for p in poi:
                if p == num:
                    is_dup = True
            if not is_dup:
                poi.append(num)
        theta += math.pi / (math.factorial(7))

    return poi

# Tests if a certain z value is within the fatou set of a complex function.
def test_fatou(c, z_to_test = Complex_Number(0, 0)):
    original_z = c
    reps = 0
    func = lambda z, c: z * z + c
    z = func(z_to_test, c)
    while reps < 99:
        z = func(z, c)
        if z.is_pole():
            return (False, reps)
        reps += 1
    
    return (True, 0)

# Tests if a certain z value is within the mandelbrot set.
def test_mandelbrot(c):
    original_z = c
    reps = 0
    func = lambda z, c: z * z + c
    z = func(Complex_Number(0, 0), c)
    while reps < 75:
        z = func(z, c)
        if z.is_pole():
            return (False, reps)
        reps += 1
    
    return (True, 0)

# Saves a collection of all points within the fatou set of a certain function to a file.
def save_fatou_to_file(name):
    save_file = open(f"{name}.csv", "w") 
    save_file.write("X,Y,C\n")
    r = 0
    theta = 0
    while r < 2:
        while theta < (2 * math.pi):
            num = euler_to_comp(r, theta)
            res = test_fatou(z_val, num)
            if res[0]:
                save_file.write(f"{num.real},{num.im},{res[1]}\n")
                if r == 0:
                    theta = 2 * math.pi
            else:
                save_file.write(f"{num.real},{num.im},{res[1]}\n")
                if r == 0:
                    theta = 2 * math.pi
            theta += 0.005
        theta = 0
        r += 0.005
        
    save_file.close()
    print("Finished!")

# Save a collection of all points within the mandelbrot set.
def save_mandelbrot_to_file(name):
    save_file = open(f"{name}.csv", "w") 
    save_file.write("X,Y,C\n")
    r = 0
    theta = 0
    while r < 2:
        while theta < (2 * math.pi):
            num = euler_to_comp(r, theta)
            res = test_mandelbrot(num)
            if res[0]:
                save_file.write(f"{num.real},{num.im},{res[1]}\n")
                if r == 0:
                    theta = 2 * math.pi
            theta += 0.005
        theta = 0
        r += 0.005
        
    save_file.close()
    print("Finished!")

# Graphs a fatou or mandelbrot set.
def graph_fatou(name='Mandelbrot Set', color='red', xs = [], ys = []):
    colors = []
    if len(xs) == 0:
        df = pd.read_csv(f'{name}.csv')
        xs = df["X"].to_list()
        ys = df["Y"].to_list()
        colors = np.array(df["C"].to_list())
    plt.scatter(xs, ys, label=f"Points in the {name} Set", c=colors, cmap='nipy_spectral', s=5)
    plt.title(f"Fatou Set: {name}")
    plt.tight_layout()
    plt.legend()
    plt.savefig(f'{name} Set.png')



'''
z_val = Complex_Number(-.12, .77)
save_fatou_to_file(z_val.str_out())

z_val = Complex_Number(-.63, .44)
save_fatou_to_file(z_val.str_out())

z_val = Complex_Number(0, 0)
save_fatou_to_file(z_val.str_out())

'''

z_val = Complex_Number(-.63, .44)
save_fatou_to_file(z_val.str_out())
graph_fatou(z_val.str_out(), 'black')