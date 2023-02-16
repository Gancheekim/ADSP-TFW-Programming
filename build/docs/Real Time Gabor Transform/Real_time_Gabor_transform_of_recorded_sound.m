clear all; close all; clc; 

Fs = 1000; % Sample rate
durationSecs = 20; % Recording time (sec)
rate = 0.5; % Refresh rate (sec)

RecordAnalyze(Fs, durationSecs, rate);

function recorder = RecordAnalyze(Fs,durationSecs, rate)
    durationSecs = durationSecs+0.1;
    x_last_index = 0;
    X_t_f = [];
    recorder = audiorecorder(Fs,8,1);
    set(recorder,'TimerPeriod',rate,'TimerFcn',@Gabor); % Do Gabor transform at specific rate.
    
    Fig   = figure;
    Axes1 = subplot(1,1,1);
    Plot1 = plot(Axes1,NaN,NaN);
    axis([0 1 -inf inf]);
    drawnow;

    record(recorder,durationSecs);
    
    function Gabor(hObject,~) % Do Gabor transform and update the plot
        x  = getaudiodata(hObject)';
        x_data = x(x_last_index+1:length(x));
        tau = 0:1/Fs:(length(x)-1)/Fs;
        dt = 0.01;
        df = 1;
        sgm = 200;
        t = 0:dt:max(tau);
        tt = x_last_index/Fs:dt:max(tau);
        f = 20:df:1000;
        dtau = tau(2)-tau(1);
        Q = floor(1.9143/dtau/sqrt(sgm));
        N = 1/(dtau*df);
        S = dt/dtau;
        window_function = exp(-sgm.*pi.*((Q-[0:2*Q])*dtau).^2);
        x_expand = [zeros(1,Q),x_data,zeros(1,Q)];
        m = [f(1)/df:f(end)/df];
        X1_index = int32(mod(m,N)+1);
        for n = 1:length(tt)-1
            x1 = [sgm^(1/4).*window_function.*x_expand(n*S:n*S+2*Q), zeros(1,int32(N)-2*Q-1)];
            X1 = fft(x1);
            Xm = X1(X1_index).*dt;
            X_t_f = [X_t_f, abs(Xm)'];
        end
        
        Plot1 = image(t, f, abs(X_t_f)/max(max(abs(X_t_f)))*400);
        colormap(gray(256));
        set(gca, 'Ydir', 'normal');
        set(gca, 'Fontsize', 12);
        xlabel('Time (Sec)', 'FontSize', 12);
        ylabel('Frequency (Hz)','FontSize', 12);
        title('Gabor transform of the signal','FontSize', 12);
        
        if(length(x)/Fs>1)
            axis([length(x)/Fs-1 length(x)/Fs -inf inf]);
        else
            axis([0 1 -inf inf]);
        end
        x_last_index = length(x);
    end
end