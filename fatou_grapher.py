from distutils.errors import CompileError
import math
import matplotlib.pyplot as plt
import pandas as pd

plt.style.use("seaborn-notebook")

class Complex_Number():

    def __init__(self, real, im):
        try:
            self.real = real
            self.im = im
            pass
        except:
            self.real = real
            self.im = im
            
        if abs(self.real) > 10000000:
            self.real = math.inf
        
        if abs(self.im) > 10000000:
            self.im = math.inf
        
        
    def __add__(self, a):
        if type(a) is Complex_Number:
            return Complex_Number(self.real + a.real, self.im + a.im)
        
    def __mul__(self, a):
        return Complex_Number(self.real * a.real - self.im * a.im, self.real * a.im + self.im * a.real)
    
    def __sub__(self, a):
        return Complex_Number(self.real - a.real, self.im - a.im)
        
    def __eq__(self, a):
        return self.real == a.real and self.im == a.im
        
    def mag(self):
        return math.sqrt(self.real ** 2 + self.im ** 2)
        
    def arg(self):
        return math.atan(self.im / self.real)
        
    def conj(self):
        return Complex_Number(self.real, -self.im)
        
    def scale(self, num):
        return Complex_Number(self.real * num, self.im * num)
        
    def e(self):
        pass
        
    def invert(self):
        try:
            top = self.conj()
            bottom = pow(self.real, 2) + pow(self.im, 2)
            return top.scale(1/bottom)
        except:
            return Complex_Number(math.inf, math.inf)
        
    def comp_div(self, a):
        return self * a.invert()
    
    def exp(self, n):
        r = math.pow(math.e, self.real * math.log(n))
        theta = self.im * math.log(n)
        return euler_to_comp(r, theta)
    
    def str_out(self):
        return f"{self.real} + {self.im}i"
        
    def is_zero(self):
        return abs(self.real) < 0.0001 and abs(self.im) < 0.0001
        
    def is_pole(self):
        return self.real == math.inf or self.im == math.inf or abs(self.real) > 10000000 or abs(self.im) > 10000000 or math.isnan(self.real) or math.isnan(self.im)
        
    def sin(self):
        return Complex_Number(math.sin(self.real) * math.cosh(self.im), math.cos(self.real) * math.sinh(self.im))
    
    def cos(self):
        return Complex_Number(math.cos(self.real) * math.cosh(self.im), - math.sin(self.real) * math.sinh(self.im))
    
    def tan(self):
        return self.sin() * self.cos().invert()
        
    def power(self, n):
        r = self.mag() ** n
        theta = self.arg() * n
        return euler_to_comp(r, theta)
            
    
def comp_func(a):
    l = [a.exp(n).invert() for n in range(1, 10000)]
    val = Complex_Number(0, 0)
    for e in l:
        print(val.str_out())
        val += e
    return val
    
def euler_to_comp(r, theta):
    real = r * math.cos(theta)
    im = r * math.sin(theta)
    return Complex_Number(real, im)


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

def test_fatou(c, z_to_test = Complex_Number(0, 0)):
    original_z = c
    reps = 0
    func = lambda z, c: z * z + c
    z = func(z_to_test, c)
    while reps < 50:
        z = func(z, c)
        if z.is_pole():
            return False
        reps += 1
    
    return True

def test_mandelbrot(c):
    original_z = c
    reps = 0
    func = lambda z, c: z * z + c
    z = func(Complex_Number(0, 0), c)
    while reps < 50:
        z = func(z, c)
        if z.is_pole():
            return False
        reps += 1
    
    return True


def save_fatou_to_file(name):
    save_file = open(f"{name}.csv", "w") 
    save_file.write("X,Y\n")
    xs = []
    ys = []
    r = 0
    theta = 0
    while r < 2:
        while theta < (2 * math.pi):
            num = euler_to_comp(r, theta)
            if test_fatou(z_val, num):
                save_file.write(f"{num.real},{num.im}\n")
                xs.append(num.real)
                ys.append(num.im)
                if r == 0:
                    theta = 2 * math.pi
            theta += 0.005
        theta = 0
        r += 0.005
        
    save_file.close()
    print("Finished!")

def save_mandelbrot_to_file(name):
    save_file = open(f"{name}.csv", "w") 
    save_file.write("X,Y\n")
    xs = []
    ys = []
    r = 0
    theta = 0
    while r < 2:
        while theta < (2 * math.pi):
            num = euler_to_comp(r, theta)
            if test_mandelbrot(num):
                save_file.write(f"{num.real},{num.im}\n")
                xs.append(num.real)
                ys.append(num.im)
                if r == 0:
                    theta = 2 * math.pi
            theta += 0.005
        theta = 0
        r += 0.005
        
    save_file.close()
    print("Finished!")

def graph_fatou(name, xs = [], ys = []):
    if len(xs) == 0:
        df = pd.read_csv(f'{name}.csv')
        xs = df["X"].to_list()
        ys = df["Y"].to_list()
    plt.scatter(xs, ys, label=f"Points in the {name} Set", s=10)
    plt.title("The Mandelbrot Set")
    plt.tight_layout()
    plt.legend()
    plt.show()

z_val = Complex_Number(-.12, .77)

'''
save_fatou_to_file(z_val.str_out())

z_val = Complex_Number(-.63, .44)
save_fatou_to_file(z_val.str_out())

z_val = Complex_Number(0, 0)
save_fatou_to_file(z_val.str_out())

'''

save_mandelbrot_to_file("Mandelbrot Set")