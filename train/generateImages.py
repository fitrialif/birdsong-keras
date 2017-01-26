#################################################################################################
#
# (c) Balint Czeba, Balint Pal Toth
# 
# If you use this code thank you referring to the corresponding paper:
# 
# Tóth Bálint Pál, Czeba Bálint,
# "Convolutional Neural Networks for Large-Scale Bird Song Classification in Noisy Environment", 
# In: Working Notes of Conference and Labs of the Evaluation Forum, Évora, Portugália, 2016, p. 8
# 
#################################################################################################

# this script generates images from the preprocessed spectograms

from scipy import io
import pandas as pd
import numpy as np
import time
import pickle
import os
import h5py

hdf5path = '../birdclef_data/data_top999_nozero.hdf5' # it takes long if we save all the spectorgram, maybe it is better to call processNMostCommon from loadData.py with a small N (eg. =3)
todirrootpath = '../images_bw_3/'

f = h5py.File(hdf5path, 'r')
X = f.get('X')
y = f.get('y')
mediaId = f.get('MediaId')
classId = f.get('ClassId')
print(mediaId[0])

y_class = np.empty((0,1))
for row in y:
    for i in range(len(row)):
        if row[i]==1:
            y_class=np.vstack((y_class,i))

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

fig = plt.figure(frameon=False)
ax = fig.add_axes([0, 0, 1, 1])
ax.axis('off')

i=0
lenX=X.shape[0]
img_artist = ax.imshow(np.flipud(X[0][0]), cmap=plt.cm.binary)

if not os.path.exists(todirrootpath):
    os.makedirs(todirrootpath)

for i in range(X.shape[0]):
    directory=os.path.join(todirrootpath,'{}'.format(classId[i][0]))
    if not os.path.exists(directory):
            os.makedirs(directory)
    print('{}/{}'.format(i, lenX))
    img_artist.set_data(np.flipud(X[i][0]))
    fileNumber=0
    while(os.path.isfile(os.path.join(directory, '{}_{}.png'.format(int(mediaId[i][0]), fileNumber)))):
        fileNumber=fileNumber+1;
        print(fileNumber)
    
    with open(os.path.join(directory, '{}_{}.png'.format(int(mediaId[i][0]), fileNumber)), 'w') as outfile:
        fig.canvas.print_png(outfile)
    
f.close()
