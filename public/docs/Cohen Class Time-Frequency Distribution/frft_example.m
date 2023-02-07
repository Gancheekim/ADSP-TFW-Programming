x = zeros(1, 300);
x(1, 100: 200) = 1;
y = x;
c = conv(x, y);

N = length(x);
y = zeros(2*N-1,1);
y(1:2:2*N-1) = x;
xint = conv(y(1:2*N-1), sinc((-(2*N-3):(2*N-3))'/2));
xint = xint(2*N-2:end-2*N+3);

xq = 1: 0.5: 300;

x_int = interp1(1:300, x, xq);
x_int2 = round(xint);

a = 1;

Faf = FrFT(x, [], a);
xf = FrFT(Faf, [], -a);

subplot(121);
plot(real(Faf));
hold on
plot(imag(Faf));
hold off
subplot(122);
plot(real(xf));
hold on
plot(imag(xf));
hold off