function [WVD, t, f] = wigner_ville(x, fs)
%     Wigner-Ville distribuion methond by FFT
    N = length(x) - 1;
    X = fft(x);
    X = [X(1: N / 2 + 1); zeros(N, 1); X(N / 2 + 2: N + 1)];
    x = 2 * ifft(X);
    x = [zeros(N, 1); x; zeros(N, 1)];
    z = hilbert(x);
    k = 1: 2 * N + 1;
    k = k + (0: 2 * N)';
    X = z(k);
    
    t = (0: 2 * N) / fs;
    f = (0: N)' / (N + 1) * fs;
    f = linspace(0, f(end), 2 * N + 1);
    
    
    K = X .* conj(flipud(X));
    WVD = real(fft(K([N + 1: 2 * N + 1, 1: N], :)));
end