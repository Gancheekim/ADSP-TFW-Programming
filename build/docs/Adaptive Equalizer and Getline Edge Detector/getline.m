function NEW=getline(X,dif)
    NEW=X;

    [k,l]=size(X);
    for i=1:k
        for j=1:l
            if inrange(i-1,k)%up
                if abs(X(i,j)-X(i-1,j))>dif
                    NEW(i,j)=255;
                end
            end

            if inrange(i+1,k)%down
                if abs(X(i,j)-X(i+1,j))>dif
                    NEW(i,j)=255;
                end
            end
        
            if inrange(j-1,l)%left
                if abs(X(i,j)-X(i,j-1))>dif
                    NEW(i,j)=255;
                end
            end
        
            if inrange(j+1,l)%right
                if abs(X(i,j)-X(i,j+1))>dif
                    NEW(i,j)=255;
                end
            end
        end
    end
    NEW(NEW~=255)=0;
    NEW=255-NEW;
end

function a=inrange(k,max)
    if k<=max && k>=1
        a =boolean(1);
    else
        a=boolean(0);
    end
end