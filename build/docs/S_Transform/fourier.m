function y = fourier(in)
    if(isvector(in))
        y = (1 ./sqrt(length(in))) .* fftshift(fft(ifftshift(in)));
    end
end

