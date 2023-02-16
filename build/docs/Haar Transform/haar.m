function y=haar(M, H)

if M==1
    y=H;
else
    for iter=2:M
        if iter==2
            I11=[1, 1];
            b1=kron(H, I11);
            I12=[1, -1];
            b2=kron(eye(iter),I12);
            temp=[b1;b2];
        else
            I11=[1, 1];
            b1=kron(temp, I11);
            I12=[1, -1];
            b2=kron(eye(2^(iter-1)),I12);
            temp=[b1;b2];
        end
    end
y=temp;

end