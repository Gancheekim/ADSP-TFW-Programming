import numpy as np
from math import *
import matplotlib.pyplot as plt


def plot_transform_result(y,t,f):

    # Plot the transform result
    C = 400
    y = np.abs(y)/np.max(np.abs(y))*C
    plt.imshow(y,cmap='gray',origin='lower')
    plt.xlabel('Time(Sec)')
    plt.ylabel('Frequency(Hz)')

    

    
    x_label = [str(int(t[0])),str(int(t[0]+t[-1])//2),str(int(t[-1]))]
    y_label = [str(int(f[0])),str(int(f[0]+f[-1])//2),str(int(f[-1]))]

    x_max = len(t)
    y_max = len(f)

    plt.xticks(np.arange(0,x_max,step=int(x_max/(len(x_label)-1))),x_label)
    plt.yticks(np.arange(0,y_max,step=int(y_max/(len(y_label)-1))),y_label)


    # Save and Show the transform result
    plt.savefig('Time-Frequency Analysis Result.png')
    plt.show()