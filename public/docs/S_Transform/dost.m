function y = dost(in)
    if (sum(mod(log2(size(in)), 1)) == 0)
    else
        error('ERROR: Signal have to use 2^k size.')
    end
    if (isvector(in))
        y = fourier(in);
        D = length(in);
        bw = dostbw(D);
        k = 1;
        for ii = bw
            if ii == 1
                k = k + ii;
            else
                y(k : k + ii - 1) = ifourier(y(k : k + ii - 1));
                k = k + ii;
            end
        end
    end
end

function y = dostbw(in)
    y = 2.^([0, log2(in)-2:-1:0, 0, 0:log2(in)-2]);
end