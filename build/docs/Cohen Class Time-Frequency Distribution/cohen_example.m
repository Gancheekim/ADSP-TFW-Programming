clear
dt=0.1;
t1=0:dt:10-dt; t2=10:dt:20-dt; t3=20:dt:30;
x1=[cos(2*pi*t1),cos(6*pi*t2),cos(4*pi*t3)];
fs = 1 / dt;
x = x1';

[WVD, ~, ~] = wigner_ville(x, fs);

%% LPF
alpha = 0.01;

[Wr, A, H, t, f] = cohen_class(x, fs, "Cone", alpha);

subplot(221);
image(t,f/1e6,real(WVD));
colormap(gray(256));
set(gca,'YDir','normal')
xlabel('Time (s)');
ylabel('Freqeuncy (MHz)');
title("Wigner");
subplot(222);
image(t,f/1e6,real(A));
colormap(gray(256));
set(gca,'YDir','normal')
xlabel('Time (s)');
ylabel('Freqeuncy (MHz)');
title("Ambiguity")
subplot(223);
image(t,f/1e6,real(H) * 400);
colormap(gray(256));
set(gca,'YDir','normal')
xlabel('Time (s)');
ylabel('Freqeuncy (MHz)');
title("Cone");
subplot(224);
image(t,f/1e6,real(Wr));
colormap(gray(256));
set(gca,'YDir','normal')
xlabel('Time (s)');
ylabel('Freqeuncy (MHz)');
title("Cohen");
