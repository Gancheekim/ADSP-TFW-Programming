% Gabor-Wigner transform
clc;clear;close all;

dtau=0.01;
dt=dtau*2;
df=0.05;

tau=0:dtau:10;
t=0:dt:max(tau);
f=-10:df:10;

a=2;
b=1;
thr=0.01;
sigma=1; % scaling factor of Gabor transform

%x=cos(2*pi*2*tau); % horizontal lines
x=exp(1i*(2*pi/3*(tau-5).^3-6*pi*tau)); % parabola
%x=exp(1i*pi*tau.^2); % oblique line
D=GaborWigner(dtau, dt, df, tau, t, f, a, b, thr, sigma, x);

%% plot
D=transpose(D);
C=400;
image(t, f, abs(D)/max(max(abs(D)))*C);
colormap(gray(256));
set(gca,'Ydir','normal') ;
xlabel('time(sec)');
ylabel('frequency(Hz)');