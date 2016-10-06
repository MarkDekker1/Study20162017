function A_lowend = NodeCoupler(A,omega)

    % ----- Low-energy network -----
    % ----- Create network -----
    A_low=zeros(length(A));
    
    
    % ----- Create network -----
    
    degrees=sum(A);
    degrees_degen=degrees;
    omega_degen=omega;
    Max=1;
    Min=0;
    r=0;
    while sum(degrees_degen)>0,
        a=omega_degen(find(omega_degen~=0));
        Max=find(omega==max(a));
        Min=1:degrees_degen(Max);
        vec=degrees_degen(Min);
        a=degrees_degen(Max);
        while sum(vec==0)>0 && a ~=length(A) && Max>Min(1),
            for i =1:length(vec),
                if vec(i)==0 && a ~=length(A),
                    Min(end+1)=a+1;
                    vec(end+1)=degrees_degen(a+1);
                    Min(i)=[];
                    vec(i)=[];                
                    a=a+1;
                end
            end
        end

        if length(Max)>0 && length(Min)>0,
            if sum(degrees_degen)>length(Min),
                A_low(Max,Min)=1;
                degrees_degen(Min)=degrees_degen(Min)-1;
                degrees_degen(Max)=0;
                omega_degen(Max)=0;
            else
                Min=Min(1:sum(degrees_degen));
                A_low(Max,Min)=1;
                degrees_degen(Min)=degrees_degen(Min)-1;
                degrees_degen(Max)=degrees_degen(Max)-length(Min);
            end
        end
        r=r+1;
    end
    A_lowend=A_low%%+transpose(A_low);
end