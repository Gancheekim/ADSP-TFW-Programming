import numpy as np
class Gradient():
    def __init__(self,img):
        self.height=img.shape[0]
        self.width=img.shape[1]
        self.grad_x = np.zeros((img.shape[0],img.shape[1],3))
        self.grad_y = np.zeros((img.shape[0],img.shape[1],3))
        self.grad = np.zeros(img.shape[:2])
        self.YCbCr = np.zeros((img.shape[0],img.shape[1],3))
        self.YCbCr[:,:,0]=img
        self.YCbCr[:,:,1]=img
        self.YCbCr[:,:,2]=img
        self.compute_gradient()

    def compute_x_gradient(self):
        # first column 
        self.grad_x[:,0]=self.YCbCr[:,1]/2+self.YCbCr[:,2]/3+self.YCbCr[:,3]/6
        # second column
        self.grad_x[:,1]=(self.YCbCr[:,2]-self.YCbCr[:,0])/2
        # third column
        self.grad_x[:,2]=(self.YCbCr[:,3]-self.YCbCr[:,1])/2+(self.YCbCr[:,4]-self.YCbCr[:,1])/3
        for i in range(3,self.width-3):
            self.grad_x[:,i]=(
                (self.YCbCr[:,i+1]-self.YCbCr[:,i-1])/2+
                (self.YCbCr[:,i+2]-self.YCbCr[:,i-2])/3+
                (self.YCbCr[:,i+3]-self.YCbCr[:,i-3])/6
            )
        self.grad_x[:,-3]=(self.YCbCr[:,-2]-self.YCbCr[:,-4])/2+(self.YCbCr[:,-1]-self.YCbCr[:,-5])/3
        self.grad_x[:,-2]=(self.YCbCr[:,-1]-self.YCbCr[:,-3])/2
        self.grad_x[:,-1]=self.YCbCr[:,-2]/2+self.YCbCr[:,-3]/3+self.YCbCr[:,-4]/6
    def compute_y_gradient(self):
        # first row 
        self.grad_y[0]=self.YCbCr[1]/2+self.YCbCr[2]/3+self.YCbCr[3]/6
        # second row
        self.grad_y[1]=(self.YCbCr[2]-self.YCbCr[0])/2
        # third row
        self.grad_y[2]=(self.YCbCr[3]-self.YCbCr[1])/2+(self.YCbCr[4]-self.YCbCr[1])/3
        for i in range(3,self.height-3):
            self.grad_y[i]=(
                (self.YCbCr[i+1]-self.YCbCr[i-1])/2+
                (self.YCbCr[i+2]-self.YCbCr[i-2])/3+
                (self.YCbCr[i+3]-self.YCbCr[i-3])/6
            )
        self.grad_y[-3]=(self.YCbCr[-2]-self.YCbCr[-4])/2+(self.YCbCr[-1]-self.YCbCr[-5])/3
        self.grad_y[-2]=(self.YCbCr[-1]-self.YCbCr[-3])/2
        self.grad_y[-1]=self.YCbCr[-2]/2+self.YCbCr[-3]/3+self.YCbCr[-4]/6
    def compute_gradient(self):
        self.compute_x_gradient()
        self.compute_y_gradient()
        self.grad=np.sqrt((np.sum(self.grad_x,axis=2)/3)**2
                        +(np.sum(self.grad_y,axis=2)/3)**2)