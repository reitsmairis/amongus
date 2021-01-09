import cv2
import numpy as np
import matplotlib.pyplot as plt

# Get Image and create hsv (put in ur own filepath)
img = cv2.imread(r'C:\Users\Iris Reitsma\Documents\Master\semester 1\blok 3\amongus\bbl.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Determine color ranges for mask (mask is a list of 0 & 1 with 1 when the pixel color is in the range)
lower_range = np.array([0,0,0])
upper_range = np.array([15,15,15])
mask = cv2.inRange(hsv, lower_range, upper_range)

# Assign True/False for when pixel is Black/not Black
grid = []
x_list = []
y_list = []
resolution = 6 # The higher this number, the lower the resolution
for i in range(0, len(mask), resolution):
    row = []
    for j in range(0, len(mask[0]), resolution):
        if mask[i][j] != 0:
            row.append(True)
            x_list.append(j)
            y_list.append(i)
        else:
            row.append(False)
    grid.append(row)
            
# Create scatter plot for visual check
plt.scatter(x_list, y_list, s=0.9)
plt.gca().invert_yaxis()
plt.show()

# Write to text file for visual check/use in other code
with open("mapfile.txt", "w") as file:
    for x in grid:
        for y in x:
            if y == True:
                file.write("o")
            elif y == False:
                file.write(" ")
        file.write("\n")

 