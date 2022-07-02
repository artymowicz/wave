import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import math
import scipy
from scipy import ndimage

N = 200 #linear size of grid
dt = 0.01 #timestep
alpha = 0.1 #spring constant
FRAMES = 23  
FRAME_INTERVAL = 500 #how many timesteps per frame of animation
TIMESTEPS = FRAMES*FRAME_INTERVAL

#initializing
positions = np.zeros((N,N))
velocities = np.zeros((N,N))
accelerations = np.zeros((N,N))

#defining initial state
positions[75, 75] = 50000
positions = ndimage.gaussian_filter(positions, 3)

#this list of ndarrays will store the animation
data = [np.ndarray.copy(positions)]

#computing the evolution
for i in range(1,TIMESTEPS):

    #updating positions, velocities, accelerations
    positions += velocities*dt
    velocities += accelerations*dt
    velocities = velocities*0.99992
    accelerations = alpha*ndimage.laplace(positions, mode='nearest')

    #object in the middle
    for j in range(20):
        for k in range(20):
            positions[100+k][100+j] = 0

    #saving current frame of animation (once every FRAME_INTERVAL iterations)
    if i%FRAME_INTERVAL == 0:
        print("writing frame "+str(i/FRAME_INTERVAL)+" of "+str(FRAMES))
        data.append(np.ndarray.copy(positions))

        #displaying object in the middle
        for j in range(20):
            for k in range(20):
                data[-1][100+k][100+j] = 7

#initializing graphics
fig = plt.figure()
ax = plt.axes(xlim=(0, N), ylim=(0, N))
imgplot = plt.imshow(data[0], vmin = -10, vmax = 10)

#defining animation function called by matplotlib.animation
def animate(k):
    imgplot.set_data(data[k])
    return [imgplot]

#displaying and saving the animation
anim = animation.FuncAnimation(fig, animate, frames=FRAMES-1, interval=1, blit=True)
anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])
plt.show()
