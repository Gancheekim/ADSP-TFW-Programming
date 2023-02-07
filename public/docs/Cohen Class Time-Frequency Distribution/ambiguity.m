function [A, t, f] = ambiguity(x, fs)
% Obtain Ambiguity function by Wigner distribution functions
% 1. Fourier transform along time axis
% 2. Inverse Fourier transform along frequency axis
    [DVW, t, f] = wigner_ville(x, fs);
    A = fft(DVW, [], 2);
    A = ifft(A, [], 1);
end