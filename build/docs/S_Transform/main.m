clc;
clear all;
close all;

ns = 2^10;
dt=0.05;
df=0.05;
t=linspace(0,60,ns);
f=[-5:df:5];
% in=1/2*((exp(-1i*2*pi*t)+exp(1i*2*pi*t))+...
%     0);
in=cos(1*pi*t);
% in2=cos(4*pi*t2);

dostIn = dost(in);
% dostIn2 = dost(in2);
figure
% dostIn=[dostIn,zeros(1,ns)];
% dostIn2=[zeros(1,ns),dostIn2];
% dostIn0=(dostIn+dostIn2)';
dostIn=dostIn';
image(t, f, abs(dostIn)/max(max(abs(dostIn)))*400);
colormap(gray(256));
set(gca, 'Ydir', 'normal');

xlabel("Tims(sec)","FontSize",12);
ylabel("Frequency(Hz)","FontSize",12);
title("Discrete Orthonormal Stockwell Transforms","FontSize",12);
axis tight
