import numpy as np
import cv2 
import matplotlib.pyplot as plt
import scipy.ndimage
from gradient import Gradient
import argparse
def downsample(sig):
    sigDown = []
    for i in range(len(sig)):
        if i%2==0:
            sigDown.append(sig[i])
    return sigDown
def wavedbc6(img):
    gn = np.array([0.0352, 0.0854, 0.1350, 0.4599, 0.8069, 0.3327])
    hn = np.array([0.3327, -0.8069, 0.4599, -0.1350, 0.0854, -0.0352])
    # Along n
    v_1L = []
    for m in range(len(img)):
        v_1L.append(downsample(np.convolve(img[m],gn)))
    v_1H = []
    for m in range(len(img)):
        v_1H.append(downsample(np.convolve(img[m],hn)))
    v_1L = np.array(v_1L)
    v_1H = np.array(v_1H)
    # Along m
    # print((img.shape[0]+len(gn)-1)/2)
    # print(np.ceil((img.shape[0]+len(gn)-1)/2))
    len_thumb = int(np.ceil((img.shape[0]+len(gn)-1)/2))
    # print(len_thumb)
    
    x_1L=np.zeros((len_thumb, len_thumb))
    x_1H1 = np.zeros((len_thumb, len_thumb))
    x_1H2 = np.zeros((len_thumb, len_thumb))
    x_1H3 = np.zeros((len_thumb, len_thumb))
    for n in range(len_thumb):
        x_1L[:,n] = downsample(np.convolve(v_1L[:,n].T, gn.T))
        x_1H1[:,n] = downsample(np.convolve(v_1L[:,n].T, hn.T))
        x_1H2[:,n] = downsample(np.convolve(v_1H[:,n].T, gn.T))
        x_1H3[:,n] = downsample(np.convolve(v_1H[:,n].T, hn.T))

    return {'LL':x_1L, 'LH':x_1H1, 'HL':x_1H2, 'HH':x_1H3}

def compute_modulus(x_1L, x_1H1, x_1H2, x_1H3):
    return np.sqrt(x_1H1**2+x_1H2**2), np.arctan(x_1H2/x_1H1)

def quantize(mod, threshold=58):
    q = np.zeros(mod.shape)
    for m in range(mod.shape[0]):
        for n in range(mod.shape[1]):
            q[m,n]= 255 if mod[m,n] >threshold else 0
    return q
def upsample(sig):
    sigUp = np.zeros(2*sig.shape[0])
    for i in range(len(sigUp)):
        if i%2==0:
            sigUp[i]=sig[int(i/2)]
        else:
            sigUp[i]=0
    return sigUp
def upsampleImg(stage):
    ret = {}
    for name, img in stage.items():
        if stage['LL'].shape[0]%2==0:
            ret[name]=scipy.ndimage.zoom(img,2,order=0)[:-5, :-5]
        else:
            ret[name]=scipy.ndimage.zoom(img,2,order=0)[:-6, :-6]
    return ret

def construct_edge(stage1, stage2):
    stage2Up=upsampleImg(stage2)
    ret = (np.abs(stage1['LH']*stage2Up['LH']+2.5*stage1['HL']*stage2Up['HL']+0.8*stage1['HH']*stage2Up['HH']))**0.55
    return ret

if __name__=='__main__':
    #image = cv2.imread('Lena_gray_512.bmp')
    #image = cv2.imread('Lena256c.jpg')
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_name", '-n', type=str, default='', help="Name of file")
    args = parser.parse_args()
    image = cv2.imread(args.file_name, 0)
    # image = image[:,:,0]
    #image = cv2.imread('Pepper512c.bmp',0)

    stage1= wavedbc6(image)
    stage2= wavedbc6(stage1['LL'])
    stage3= wavedbc6(stage2['LL'])
    stage4= wavedbc6(stage3['LL'])

    
    
    mod, ang = compute_modulus(stage1['LL'],stage1['LH'],stage1['HL'],stage1['HH'])
    modG = Gradient(mod)


    mod2, ang2 = compute_modulus(stage2['LL'],stage2['LH'],stage2['HL'],stage2['HH'])
    mod2G = Gradient(mod2)
    mod3, ang3 = compute_modulus(stage3['LL'],stage3['LH'],stage3['HL'],stage3['HH'])
    
    invTransform = plt.figure('Edge')
    plotMod = invTransform.add_subplot(2,2,1)
    plotMod.set_title('Mod')
    plotMod.imshow(mod, cmap='gray')


    #q = quantize(mod)
    q = quantize(modG.grad,25)
    quant = invTransform.add_subplot(2,2,2)
    quant.set_title('edge')
    quant.imshow(q, cmap='gray')

    #invTransform = plt.figure('Edge')
    plotMod2 = invTransform.add_subplot(2,2,3)
    plotMod2.set_title('Mod 2')
    plotMod2.imshow(mod2, cmap='gray')


    q2 = quantize(mod2G.grad,55)
    quant2 = invTransform.add_subplot(2,2,4)
    quant2.set_title('edge')
    quant2.imshow(q2, cmap='gray')

    #-----FIG 2-----#

    invTransform2 = plt.figure('Edge Using 1st+2nd wavelet transform')

    ret_12 = construct_edge(stage1, stage2)
    retG2 = Gradient(ret_12)
    ret2 = quantize(retG2.grad,45)
    edge = invTransform2.add_subplot(2,2,1)
    edge.set_title('edge 2')
    edge.imshow(ret2, cmap='gray')

    invTransform.tight_layout()
    invTransform2.tight_layout()
    plt.show()