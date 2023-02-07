function [DCTmat] = dct_1(N, ortho)
%%%%%%%%%%
% Description:
%   Implementation of the 1-D DCT Type-I.
% Input:
%   N:      Length of the transform (N-point DCT)
%            ( Data type: an integer bigger than 1 )
%   ortho:  Output a matrix with orthonormal coefficients
%            ( Data type: numeric )
%            ( 0 -> False, otherwise -> True )
%            ( Optional, default = 0 (False) )
% Output:
%   DCTmat: Transformation matrix of DCT-I
%            ( Size = N x N )
%%%%%%%%%%

if nargin < 2
    ortho = 0;
end

if N < 2
    error("DCT-I is not defined when the sequence length is less than 2.")
end

N = floor(N);
ortho = logical(ortho);

sqrt2 = sqrt(2);

if ortho
    M_x0 = ones(N, 1) .* sqrt2;
    M_xn = ((-1) .^ (0:N-1))' .* sqrt2;
else
    M_x0 = ones(N, 1);
    M_xn = ((-1) .^ (0:N-1))';
end

M_x = (0:N-1)' * (1:N-2);
M_x = 2 .* cos((pi / (N-1)) .* M_x);

DCTmat = [M_x0 M_x M_xn];

if ortho
    DCTmat(1, :) = DCTmat(1, :) ./ sqrt2;
    DCTmat(N, :) = DCTmat(N, :) ./ sqrt2;
    DCTmat = DCTmat .* sqrt(1 / 2 / (N-1));
end

end

