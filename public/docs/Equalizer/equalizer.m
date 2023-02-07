function [x_out] = equalizer(y, k, c)
%%%%%%%%%%
% Description:
%   Implementation of the 1-D Equalizer (Wiener Filter).
% Input:
%   y:       Received signal
%             ( Data type: 1-D array )
%   k:       Effect of the system
%             ( Data type: 1-D array )
%   c:       A constant, usually the noise-to-signal power ratio of the additive noise
%             ( Data type: numeric )
% Output:
%   x_out:   Restored signal
%             ( Data type: 1-D array )
%%%%%%%%%%

sz_y = size(y);
sz_k = size(k);

if (sz_y(1) ~= 1) || (sz_k(1) ~= 1) || (size(sz_y, 2) ~= 2) || (size(sz_k, 2) ~= 2)
    error("The dimension of the input array must be 1.")
end

N = sz_y(2);
K = fft(k, N);
Y = fft(y, N);

mag_K = abs(K);
phase_K = angle(K);

K_inv = 1 ./ ((c ./ (mag_K+1e-5) + mag_K) .* exp(1i * phase_K));

x_out = real(ifft(Y .* K_inv));

end

