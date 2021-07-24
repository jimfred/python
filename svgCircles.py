import os.path

import svgwrite
import math

circle_radial_qty = 80
circle_layer_qty = 4
circle_path_radius = 6

units = svgwrite.inch
svg_name = os.path.splitext(__file__)[0] + ".svg"  # output .svg file based on this file's name.

dwg = svgwrite.Drawing(filename=svg_name, profile='tiny', height=circle_path_radius*2*units, width=circle_path_radius*2*units)

dwg.viewbox(minx=-1200, miny=-1200, width=2*1200, height=2*1200)

blue = svgwrite.rgb(0, 0, 255)

angle_inc = 360 / circle_radial_qty
r2 = math.sin(math.radians(angle_inc / 2)) * circle_path_radius

for spoke in range(circle_radial_qty):
    angle = angle_inc * spoke + 0

    for layer in range(circle_layer_qty):
        x = math.cos(math.radians(angle)) * (circle_path_radius + layer * 2 * r2)
        y = math.sin(math.radians(angle)) * (circle_path_radius + layer * 2 * r2)
        circle = dwg.circle(center=(x * units, y * units), r=r2 * units, fill=blue, stroke_width=0)
        dwg.add(circle)

dwg.save()

