clc;
clear all;
close all;
M = 11; %taps
tau = [3  7  11  18]; %delay
mu = [0.15  0.07  0.02  0.006]; %step size
wo = zeros(M,1);

run = 200; %running time 
N = 3000;  %
W = [2.9 3.1 3.3 3.5];

SNR = [5 10 15 20];
for index = 1:4
    for n = 1:3
        h(n) = (1+cos(2*pi*(n-2)/W(1)))/2; %raised cosine
    end
    for count=1:run
        d = 2*randi([0 1],1,N)-1;
        sigma = sqrt(1/(2*power(10,SNR(index)/10)));
        u = conv(d,h);
        U = [];
        for i=1:M
            U = [U;u(1:N)];
            u = [0 u];
        end
        dd = [zeros(1,tau(index)) d(1:N-tau(index))];  %tau in different value
        w = wo;
        for n = 1:N
            y(n) = w'*U(:,n);
            e(count,n) = dd(n)-y(n);
            w = w + mu(2)*U(:,n)*conj(e(count,n));
        end
    end
    figure(1);
    subplot(2,2,index);
    plot(mean(e.^2));; 
    title("tau is "+num2str(tau(index)));
    xlabel('n');
    ylabel('e[n]^2');
end