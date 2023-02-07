[x,fs] = audioread('Chord.wav');
x = x(:,1).';
tau = 0:1/fs:(length(x)-1)/fs;
dt = 0.005; df= 1; 
sgm1 = 25; sgm2 = 400;
t= 0:dt:max(tau); f= 20:df:1000;

y1 = Gabor(x,tau,t,f,sgm1);
y2 = Gabor(x,tau,t,f,sgm2);
y = y1.*conj(y2);

y1 = abs(y1);
y1 = y1/max(max(y1))*255;
y1 = cast(y1,'uint8');
y2 = abs(y2);
y2 = y2/max(max(y2))*255;
y2 = cast(y2,'uint8');
y = abs(y);
y = y/max(max(y))*255;
y = cast(y,'uint8');

figure;
subplot(1,2,1);
imshow(y1');
title('small sigma (narrower window)');
subplot(1,2,2);
imshow(y2');
title('large sigma (wider window)');

figure;
imshow(y');
title('Genrealized Spectrogram');


function X = Gabor(x, tau, t, f, sgm)
    %w = ones(1,(2*B)/dt+1);
    dt = max(t)/(length(t)-1);
    dtau = max(tau)/(length(tau)-1);
    Q = (1.9143/dt)/sqrt(100);
    len = ceil((2*Q*dt)/dtau);
    bottom = floor(f(1)*len*dtau);
    top = ceil(f(end)*len*dtau);
    X = zeros(length(t), top-bottom+1);
    for n=1:size(X,1)
        x1 = zeros(1,len);
        left = ceil(((n-Q)*dt)/dtau);
        if left<=0
            left = 1;
        end
        right = ceil(((n+Q)*dt)/dtau);
        if right > length(tau)
            right = length(tau);
        end
        if right-left>=len
            right = left+len-1;
        end
        x1(1:right-left+1) = x(left:right);
        w = exp((-pi*sgm).*((dtau*((1:len)-(1+len)/2)).^2));
        x1 = x1.*w;
        post_term = fft(x1);
        prior_term = dt * exp(2*pi*1i*(Q-n)/len * (0:len-1));
        buff = prior_term.*post_term;
        X(n,:) = buff(bottom:top);
    end
    X(:,end:-1:1) = X;
end