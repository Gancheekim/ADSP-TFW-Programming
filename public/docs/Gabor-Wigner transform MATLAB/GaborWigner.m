function D=GaborWigner(dtau, dt, df, tau, t, f, a, b, thr, sigma, x) %#ok<INUSL>
S=dt/dtau;
N=1/dtau/df;
T=length(t);
F=length(f);
%% Gabor
Q=ceil(1.9143/dtau/sqrt(sigma));
G=zeros(T, F);

for i=1:T
    n=floor(t(i)/dt);
    x1=zeros(1, N);
    for q=0:N-1
        if q<=2*Q && n*S-Q+q+1>=1 && n*S-Q+q+1<=length(x)
            x1(q+1)=sigma^(1/4)*x(n*S-Q+q+1)*exp(-sigma*pi*((Q-q)*dtau)^2);
        end
    end
    X1=fft(x1);
    
    for j=1:F
        m=floor(f(j)/df);
        k=0;
        while m+k*N <=0
            k=k+1;
        end
        G(i,j)=dtau*exp(1i*2*pi*(Q-n*S)*m/N)*X1(mod(m+k*N, N)+1);
    end
end

%% Wigner
W=zeros(T, F);
N=1/dtau/df/2;
if N<T
    fprintf("N must >= T\n")
end
for i=1:T
    for j=1:F
        if abs(G(i, j))>thr
            n=floor(t(i)/dt);
            Q=min(T-1-n, n);
            if 2*Q+1>N
                fprintf("N must >= 2*Q-1\n");
            end
            c1=zeros(1, N);
            for q=0:2*Q
                c1(q+1)=x(n*S-Q+q+1)*conj(x(n*S-q+Q+1));
            end
            C1=fft(c1);
            m=floor(f(j)/df);
            k=0;
            while m+k*N <0
                k=k+1;
            end
            W(i,j)=2*dtau*exp(1i*2*pi*Q*m/N)*C1(mod(m+k*N, N)+1);
        end
    end
end
%G=transpose(G);
%W=transpose(W);
D=(G.^a).*(W.^b);

end