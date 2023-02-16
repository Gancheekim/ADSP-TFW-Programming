function out = ifourier(in)
    out = sqrt(length(in)) .* fftshift(ifft(ifftshift(in)));
end