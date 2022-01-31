
import PIL.Image  # pip install --upgrade pillow-simd --global-option="build_ext" --global-option="--disable-jpeg" --global-option="--disable-zlib"
img = PIL.Image.open("PillowBmp_00.png")
# img.rotate(45).show()

# load PNG into arrays.

(size_x, size_y) = img.size
img.load()
if img.im.bands != 2 or img.mode != 'LA':
    raise Exception('Expected a gray-alpha bmp')

import numpy
gray_2D = numpy.zeros((size_x, size_y))
fixed_2D = numpy.zeros((size_x, size_y))

# for each pixel in PNG, load data.
# Assume any pixel with a=255 is not to be blurred.
for x in range(size_x):
    for y in range(size_y):
        (g, a) = img.getpixel((x, y))  # get this pixel, the grayscale and alpha.
        fixed_2D[x, y] = (a == 255)  # pixel is 'fixed' (not blurred) if a=255.
        gray_2D[x, y] = g if (a == 255) else 127  # pixel retains value if fixed.

img.show()

# repeat several times, a blurring operation
for i in range(120):
    print(i)
    for x in range(1, size_x - 1):
        for y in range(1, size_y - 1):
            c = gray_2D[x, y]
            n = gray_2D[x, y - 1]
            s = gray_2D[x, y + 1]
            e = gray_2D[x + 1, y]
            w = gray_2D[x - 1, y]
            if not fixed_2D[x, y]:  # if not static, do a simplistic blur.
                gray_2D[x, y] = (n + s + e + w) / 4

img_blurred = img.copy()
for x in range(1, size_x - 1):
    for y in range(1, size_y - 1):
        img_blurred.putpixel((x, y), (int(gray_2D[x, y]), 255))
for x in range(0, size_x):
    img_blurred.putpixel((x, 0), (int(gray_2D[x, y]), 0))
    img_blurred.putpixel((x, size_y - 1), (int(gray_2D[x, y]), 0))
for y in range(0, size_y):
    img_blurred.putpixel((0, y), (int(gray_2D[x, y]), 0))
    img_blurred.putpixel((size_x - 1, y), (int(gray_2D[x, y]), 0))
img_blurred.show()
img_blurred.save("PillowBmpBlurred.png")

import matplotlib.pyplot
fig = matplotlib.pyplot.figure()
ax = fig.add_subplot(111, projection='3d')
X = numpy.zeros((size_x, size_y))
Y = numpy.zeros((size_x, size_y))
Z = numpy.zeros((size_x, size_y))
for x in range(size_x):
    for y in range(size_y):
        X[x, y] = x
        Y[x, y] = y
        Z[x, y] = gray_2D[x, y]
red_blue_colormap = matplotlib.colors.LinearSegmentedColormap.from_list("", ["blue", "gray", "red"])  # https://stackoverflow.com/a/46778420/101252
ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=red_blue_colormap)
matplotlib.pyplot.show()

