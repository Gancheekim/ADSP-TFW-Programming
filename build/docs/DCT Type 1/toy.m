example = 1;

if example == 1
    n = 4;

    y = [4, 3, 5, 10, 5, 3];

    F = real(fft(y));
    M = dct_1(n);
    D = M * y(1:n)';

    disp("* Example 1")
    disp("The DCT-I is equivalent to the FFT for real, even-symmetrical inputs."); disp(" ")
    disp("Input:"); disp(y)
    disp("FFT:"); disp(F)
    disp("DCT:"); disp(D')
end


if example == 2
    M = dct_1(8, 1);

    disp("* Example 2")
    disp("DCT-I with orthonormal coefficients."); disp(" ")
    disp("8-point DCT matrix M = "); disp(M)
    disp("M * M' = "); disp(M * M')
end
