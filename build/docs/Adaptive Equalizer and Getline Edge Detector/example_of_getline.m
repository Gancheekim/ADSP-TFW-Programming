X=imread('cat.jpg');

dif=100;


[k,l]=size(X);


figure(1)
imshow(X)
figure(2)
parameter=25;

NEW=X;
imshow(getline(X,parameter))