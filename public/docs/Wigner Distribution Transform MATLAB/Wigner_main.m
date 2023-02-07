% Wigner Distribution
clc;clear;close all;

%% inputs
dtau=0.01;
dt=dtau*2;
df=0.01;

tau=0:dtau:10;
t=0:dt:max(tau);
f=-10:df:10;

x=cos(2*pi*3*tau);
%x=exp(1i*(2*pi/3*(tau-5).^3-6*pi*tau));
%x=exp(1i*pi*tau.^2);

%%
tic;
W=Wigner(dtau, dt, df, tau, t, f, x);
toc;
%% plot
W=transpose(W);
C=400;
image(t, f, abs(W)/max(max(abs(W)))*C);
colormap(gray(256));
set(gca,'Ydir','normal') ;
xlabel('time(sec)');
ylabel('frequency(Hz)');