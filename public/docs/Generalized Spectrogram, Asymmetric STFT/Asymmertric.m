clear
dt = 0.05;
df = 0.05;
t1 = 0:dt:10-dt;
t2 = 10:dt:20-dt;
t3 = 20:dt:30-dt;
t = 0:dt:30-dt;
f = -5:df:5;
%% For onset detection
xo = [cos(2*pi*t1),0*cos(t2),cos(4*pi*t3)] + normrnd(0,1,size(t));
yo_asym = AsymSTFT(xo, t, 1/40, 1/200,false,0);
yo_sym = AsymSTFT(xo, t, 1/120, 1/120,false,0);
yo_asym = to255(yo_asym);
yo_sym = to255(yo_sym);

figure
subplot(2,1,1);
imshow(yo_asym');
title('asymmetric (more on future, for onset detection)');
hold on
xline(400,'-r');
hold off
subplot(2,1,2);
imshow(yo_sym');
title('symmetric');
hold on
xline(400,'-r');
hold off
%% Real-Time Simulation
xr = [cos(0.4*pi*(t1.^2)),cos(8*pi*t2),cos(0.4*pi*(30-t3).^2)];

yr_sym = AsymSTFT(xr, t, 1/120, 1/120,true, -5);
yr_asym = AsymSTFT(xr, t, 1/200, 1/40, true, -5);
yr_asym = to255(yr_asym);
yr_sym = to255(yr_sym);

figure
subplot(2,1,1);
imshow(yr_asym');
title('asymmetric (more on past, for real-time simulation)');
hold on
xline(200,'-r');
xline(400,'-r');
hold off
subplot(2,1,2);
imshow(yr_sym');
title('symmetric');
hold on
xline(200,'-r');
xline(400,'-r');
hold off
%% Function
function X = AsymSTFT(x, t, spast,sfuture,realtime,delay)
    wpast = 0:spast:(1-spast);
    wfuture = (1-sfuture):-sfuture:0;
    w = [wpast,1,wfuture];

    dt = max(t)/(length(t)-1);
    if realtime
        extra = cast(delay/dt,'int32')+2;
        w(length(wpast)+extra:end)=0;
    end
    len = length(w);
    X = zeros(length(t), len);
    for n=1:size(X,1)
        x1 = zeros(1,len);
        left = n-length(wpast);
        right = n+length(wfuture);
        if left<=0
            x1(len-right+1:end) = x(1:right);
        elseif right > length(x)
            x1(1:(length(x)-left+1)) = x(left:end);
        else
            x1(1:right-left+1) = x(left:right);
        end
        x1 = x1.*w;
        post_term = fftshift(fft(x1));
        prior_term = dt * exp(2*pi*1i*(length(wpast)-n)/len * (0:len-1));
        buff = prior_term.*post_term;
        X(n,:) = buff;
    end
end
function out=to255(in)
    out = abs(in);
    out = out/max(max(out))*255;
    out = cast(out,'uint8');
end