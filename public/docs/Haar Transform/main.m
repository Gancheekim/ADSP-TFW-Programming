clc; clear; close all;

str = "Please input your Haar tansform matrix points! \n";
fprintf(str);
prompt = "Points: ";
n = input(prompt); % Points number
M=(n==2)*1+(n~=2)*log2(n); % Iterate times
H=[1, 1;
   1, -1;];
HaarM=haar(M,H);
Signal=randi(n+2,n,1);
HaarSig=HaarM*Signal;
figure
plot(1:n,Signal,'r:diamond',1:n,HaarSig,'b-o');
xlabel('Points','FontSize',12);
ylabel('Values','FontSize',12);
title("Haar",'FontSize',12);
legend('Signal','HaarSig');
grid on;



