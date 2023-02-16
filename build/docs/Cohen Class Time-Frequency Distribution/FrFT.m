function F = FrFT(f, L, a)
    f = f(:);
    N = length(f);
    shft = rem((0: N - 1) + fix(N / 2), N) + 1;
    sN = sqrt(N);
    a = mod(a, 4);
    switch (a)
        case 0
            F = f;
        case 2
            F = flip(f);
        otherwise
            % reduce to interval 0.5 < a < 1.5
            if (a > 2.0)
                a = a - 2;
                f = flip(f);
            end
            if (a > 1.5)
                a = a - 1;
                f(shft, 1) = fft(f(shft), L) / sN;
            end
            if (a < 0.5)
                a = a + 1;
                f(shft, 1) = ifft(f(shft), L) * sN;
            end
            % the general case for 0.5 < a < 1.5
            alpha = a * pi / 2;
            tana2 = tan(alpha / 2);
            sina = sin(alpha);
            f = [zeros(N - 1, 1); transpose(interp1(1: N, f, 1: 0.5: N)); zeros(N - 1, 1)];
            % chirp premultiplication
            chrp = exp(-1i * pi / N * tana2 / 4 * (-2 * N + 2: 2 * N - 2)'.^ 2);
            f = chrp .* f;
            % chirp convolution
            c = pi / N / sina / 4;
            F = conv(exp(1i * c * (-(4 * N - 4): 4 * N - 4)'.^ 2), f);
            F = F(4 * N - 3: 8 * N - 7) * sqrt(c / pi);
            % chirp post multiplication
            F = chrp .* F;
            % normalizing constant
            F = exp(-1i * (1 - a) * pi / 4) * F(N: 2: end - N + 1);
    end
end