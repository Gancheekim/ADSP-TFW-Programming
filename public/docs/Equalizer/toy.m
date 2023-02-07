t = -10:0.1:10;

x = sinc(t);

k = ones(1, 10);
k = k ./ sum(k);

y = cconv(x, k, size(x, 2));
noise = 0.01 * randn(1, size(x, 2));
y = y + noise;

restored1 = equalizer(y, k, 0);
restored2 = equalizer(y, k, 0.1);

figure
subplot(4,1,1)
plot(t, x)
title("(a) Original Signal")

subplot(4,1,2)
hold on
plot(t, x)
plot(t, y)
title("(b) Distortion with Noise")
legend("Original", "Distorted")
hold off

subplot(4,1,3)
hold on
plot(t, x)
plot(t, restored1)
title("(c) Restoration (c = 0)")
legend("Original", "Restored")
hold off

subplot(4,1,4)
hold on
plot(t, x)
plot(t, restored2)
title("(d) Restoration (c = 0.1)")
legend("Original", "Restored")
hold off