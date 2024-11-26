import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def hex_to_rgba(hex_color):
    """Convert hex color to RGBA."""
    hex_color = hex_color.lstrip('#')
    return [int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4)] + [1.0]

def hex_colormap_to_array(hex_colors):
    """Convert a list of hex colors to a NumPy array of RGBA values."""
    rgba_colors = [hex_to_rgba(color) for color in hex_colors]
    return np.array(rgba_colors)

# 使用示例
hex_colors = ['#ffffd9','#edf8b1','#c7e9b4','#7fcdbb','#41b6c4','#1d91c0','#225ea8','#253494','#081d58']
rgba_array = hex_colormap_to_array(hex_colors)
print(rgba_array)
