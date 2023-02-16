function [Wr, A1, H, t, f] = cohen_class(x, fs, D, alpha)
    [A, t, f] = ambiguity(x, fs);
    A1 = cat(1, A(floor(size(A, 1) / 2) + 1: size(A, 1), :), A(1: floor(size(A, 1) / 2), :));
    A1 = A1';
    A1 = cat(1, A1(floor(size(A, 1) / 2) + 1: size(A, 1), :), A1(1: floor(size(A, 1) / 2), :));

    [f1, f2] = freqspace(size(A, 1),'meshgrid');
%     f1 = f1 * 1.1;
%     f2 = f2 * 1.1;
    switch D
        case "wigner"
            Hd = ones(size(A));
        case "CW"
            CWH = exp(-1 * alpha * ((f1) .* (f2) .^ 2));
            CWH = fft(CWH, [], 1);
            CWH = ifft(CWH, [], 2);
            CWH = abs(CWH);
            Hd = CWH;
            Hd(Hd >= 10) = 1;
        case "Riha"
            CWH = exp(-1i * pi * ((f1) .* (f2)));
            CWH = fft(CWH, [], 1);
            CWH = ifft(CWH, [], 2);
            CWH = abs(CWH);
            Hd = CWH;
            Hd(Hd >= 10) = 1;
        case "Cone"
            CWH = sinc(f1 .* f2) .* exp(-2 * pi * alpha * (f2 .^ 2));
            CWH = fft(CWH, [], 1);
            CWH = ifft(CWH, [], 2);
            CWH = abs(CWH);
            Hd = CWH;
            Hd(Hd >= 1e-2) = 1;
        otherwise
            Hd = ones(size(A));
    end

    H = cat(1, Hd(floor(size(Hd, 1) / 2) + 1: size(Hd, 1), :), Hd(1: floor(size(Hd, 1) / 2), :));
    H = H';
    H = cat(1, H(floor(size(H, 1) / 2) + 1: size(H, 1), :), H(1: floor(size(H, 1) / 2), :));
    
    Ar = A .* Hd;
    Wr = fft(Ar, [], 1);
    Wr = ifft(Wr, [], 2);
end