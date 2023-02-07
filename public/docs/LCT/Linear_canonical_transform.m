clear all; close all; clc;

dt = 0.01;
df = 0.05;
sgm = 2; % sigma of scaled Gabor transform
t1 = [-5:dt:-2.5-dt];
t2 = [-2.5:dt:2.5-dt];
t3 = [2.5:dt:5];
t = [-5:dt:5];
f = [-10:df:10];
x = [0*t1,ones(1,length(t2)),0*t3]; % Rectangular function

a = cosd(45); % Define coefficient a
b = sind(45); % Define coefficient b
c = sind(45); % Define coefficient c
d = cosd(45); % Define coefficient d

Xu = LCT(x, t, a, b, c, d);
y = Gabor(Xu, t, f, sgm);

function Xu_func = LCT(x_func, t_func, a_func, b_func, c_func, d_func)
    delta_t = t_func(2)-t_func(1);
    Xu_temp = [];
    for n=1:length(t_func)
        u = t_func(n);
        if b_func==0 % when b is equal to 0.
            x_index = floor(u*d_func/delta_t-t_func(1)/delta_t+1);
            if x_index>=1 & x_index<=length(x_func)
                xdu = x_func(x_index);
            else
                xdu = 0;
            end
            Xu_temp = [Xu_temp, sqrt(d_func)*exp(1j*pi*c_func*d_func*u*u)*xdu];
        else % when b is not equal to 0.
            Q = exp(-1j*2*pi/b_func*u*t_func).*exp(1j*pi*a_func/b_func.*t_func.*t_func).*x_func;
            Xu_temp = [Xu_temp, sqrt(1/(1j*b_func))*exp(1j*pi*d_func/b_func*u*u)*trapz(t_func,Q)];
        end
    end
    Xu_func = Xu_temp;
end


function y_func = Gabor(x_func, t_func, f_func, sgm_func)
    delta_t = t_func(2)-t_func(1);
    delta_f = f_func(2)-f_func(1);
    Q = floor(1.9143/delta_t/sqrt(sgm_func));
    N = 1/(delta_t*delta_f);
    window_function = exp(-sgm_func.*pi.*((Q-[0:2*Q])*delta_t).^2);
    x_func = [zeros(1,Q),x_func,zeros(1,Q)];
    m = [f_func(1)/delta_f:f_func(end)/delta_f];
    X1_index = int32(mod(m,N)+1);
    X_t_f = [];
    for n = 1:length(t_func)-1
        x1 = [sgm_func^(1/4).*window_function.*x_func(n:n+2*Q), zeros(1,int32(N)-2*Q-1)];
        X1 = fft(x1);
        Xm = X1(X1_index).*delta_t;
        X_t_f = [X_t_f, abs(Xm)'];
    end
    
    y_func = image(t_func, f_func, abs(X_t_f)/max(max(abs(X_t_f)))*400);
    colormap(gray(256));
    set(gca, 'Ydir', 'normal');
    set(gca, 'Fontsize', 12);
    xlabel('Time (Sec)', 'FontSize', 12);
    ylabel('Frequency (Hz)','FontSize', 12);
    title('Gabor transform of the signal','FontSize', 12);
end