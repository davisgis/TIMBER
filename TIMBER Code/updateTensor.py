def update(a, x, y, z, maxLH):
    a[int(x), int(y), int(z)] = a[int(x), int(y), int(z)] + maxLH
    a[int(y), int(x), int(z)] = a[int(y), int(x), int(z)] + maxLH

    print("The value of ", x, "-", y, "-", z, " is: ", a[int(x), int(y), int(z)])
    print("The value of ", y, "-", x, "-", z, " is: ", a[int(x), int(y), int(z)])

def view(a, x, y, z):
    print("The value of ", x, "-", y, "-", z, " is: ", a[int(x), int(y), int(z)])
    print("The value of ", y, "-", x, "-", z, " is: ", a[int(x), int(y), int(z)])




