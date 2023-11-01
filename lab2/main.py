import numpy as np
import matplotlib.pyplot as plt


width, height, distance_between_points = open('big.dem', 'r').readline().split()
width, height, distance_between_points = int(width), int(height), int(distance_between_points)
raw_data = np.loadtxt('big.dem', skiprows=1).reshape(int(width), int(height))

min_h = raw_data.min()
max_h = raw_data.max()
# gradient
def color(h):
    # normalize
    h = (h - min_h) / (max_h - min_h)
    if h < 0.5:
        return [h * 2, 1, 0]
    else:
        return [1, (1 - h) * 2, 0]
    
scale = 30

x = [[color(j) for j in i] for i in raw_data]
for i in range(height):
    for j in range(width):
        if j == 0:
            diff = 0
        else:
            diff = raw_data[i, j] - raw_data[i, j - 1]

        x[i][j] = [max(0, min(1, x[i][j][0] - diff / scale)), max(0, min(1, x[i][j][1] - diff / scale)), max(0, min(1, x[i][j][2] - diff / scale))]

light = np.array([0, 0, -1])
light = light / np.linalg.norm(light)

for i in range(height):
    for j in range(width):
        if i == 0 or i == height-1 or j == 0 or j == width-1:
            normal = np.array([0, 0, 1])
        else:
            dzdx = (raw_data[i, j+1] - raw_data[i, j-1]) / (2 * distance_between_points)
            dzdy = (raw_data[i+1, j] - raw_data[i-1, j]) / (2 * distance_between_points)
            normal = np.cross(np.array([2*distance_between_points, 0, dzdx]), np.array([0, 2*distance_between_points, dzdy]))
        normal = normal / np.linalg.norm(normal)
        angle = np.arccos(np.dot(normal, light)) - (np.pi/2)
        x[i][j] = [max(0, min(1, x[i][j][0] + angle / scale)), max(0, min(1, x[i][j][1] + angle / scale)), max(0, min(1, x[i][j][2] + angle / scale))]
            

plt.imshow(x)

plt.show()