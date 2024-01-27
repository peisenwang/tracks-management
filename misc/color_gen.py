#!/usr/bin/env python3
"""Generate a group of similar but distinct colors"""
import cv2
import numpy as np


num = 7
step = 5


if __name__ == '__main__':
    rng = np.random.default_rng(0)

    hues = np.arange(0, num * step, step, dtype=np.uint8)
    sv = rng.integers(150, 255, (hues.size, 1, 2), dtype=np.uint8)
    sv = np.full((hues.size, 1, 2), 255, dtype=np.uint8)
    colors = np.concatenate((hues[:, None, None], sv), -1)
    colors = cv2.cvtColor(colors, cv2.COLOR_HSV2BGR)
    colors = colors.squeeze()
    colors = [
        '#' + ''.join(f'{c:02x}' for c in color[::-1]) for color in colors]
    for c in colors:
        print(c)
