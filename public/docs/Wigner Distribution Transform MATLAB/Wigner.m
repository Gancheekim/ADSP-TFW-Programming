function W=Wigner(dtau, dt, df, tau, t, f, x) %#ok<INUSL>
S=dt/dtau;
N=1/dtau/df/2;
T=length(t);
F=length(f);
W=zeros(T, F);
if N<T   
    fprintf("N must >= T\n")   
end
for i=1:T
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
    
    for j=1:F
        m=floor(f(j)/df);
        k=0;
        while m+k*N <0
            k=k+1;
        end
        W(i,j)=2*dtau*exp(1i*2*pi*Q*m/N)*C1(mod(m+k*N, N)+1);
    end
end
end