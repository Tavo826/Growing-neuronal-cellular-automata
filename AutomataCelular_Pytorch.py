import math
import numpy as np
import torch
import matplotlib.pyplot as plt
from PIL import Image
from torch import nn
from torch.nn import functional as F

POOL_SIZE = 1024
N_CHANNEL = 16
width = height = int(math.sqrt(POOL_SIZE))

sobelX = torch.from_numpy(np.array([[-1,0,1], \
                                    [-2,0,2], \
                                    [-1,0,1]]).astype(float)).repeat((16,16,1,1))
sobelY = torch.from_numpy(np.array([[-1,-2,-1], \
                                    [0,0,0], \
                                    [1,2,1]]).astype(float)).repeat((16,16,1,1))
cellId = torch.from_numpy(np.array([[0,0,0], \
                                    [0,0,0], \
                                    [0,0,0]]).astype(float)).repeat((16,16,1,1))

filters = [sobelX, sobelY, cellId]

grid = np.zeros((width, height, N_CHANNEL))

class UpdateGrid(nn.Module):

    def __init__(self):
        super(UpdateGrid, self).__init__()

        self.fc1 = nn.Conv2d(N_CHANNEL * len(filters), 128, (1,1))
        self.fc2 = nn.Conv2d(128, N_CHANNEL, (1,1))

    def forward(self, x):
        
        perception = torch.empty(1, (len(filters) * N_CHANNEL, width, height))
        
        for f,filt in enumerate(filters):
            perception[:, (f*N_CHANNEL):((f+1)*N_CHANNEL),:,:] = F.conv2d(x, filt, padding=[1,1])

        dx = self.fc1(perception)
        dx = F.relu(dx)
        dx = self.fc2(dx)

        #Skip connection + sctochastic update
        x = x + dx * torch.from_numpy(np.random.randint(0, 1, (width,height)))

        alive = F.conv2d((x > 0.1).type(torch.int), torch.from_numpy(np.ones((16,16,3,3))))[:,:,3] > 0.1
        return x * alive

image = '' #Imagen de 32x32
im = Image.open(image)

grid[:,:,0:4] = np.array(im) / 255

updateGrid = UpdateGrid()
result = updateGrid.forward(torch.from_numpy(grid).view(1,N_CHANNEL, width, height))

plt.imshow(result[:,:,0:4])
plt.show()
