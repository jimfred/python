import svgwrite
import math

units = svgwrite.inch
dwg = svgwrite.Drawing(filename="0.svg", profile='tiny', height=12*units, width=12*units)

dwg.viewbox(minx=-1200, miny=-1200, width=2*1200, height=2*1200)

blue = svgwrite.rgb(0, 0, 255)

circle_radial_qty = 80
circle_layer_qty = 4
circle_path_radius = 6

angle_inc = 360 / circle_radial_qty
r2 = math.sin(math.radians(angle_inc / 2)) * circle_path_radius

for i in range(circle_radial_qty):
    angle = angle_inc * i + 0

    for j in range(circle_layer_qty):
        x = math.cos(math.radians(angle)) * (circle_path_radius + j * 2 * r2)
        y = math.sin(math.radians(angle)) * (circle_path_radius + j * 2 * r2)
        circle = dwg.circle(center=(x * units, y * units), r=r2 * units, fill=blue, stroke=blue, stroke_width=0)
        dwg.add(circle)

dwg.save()

