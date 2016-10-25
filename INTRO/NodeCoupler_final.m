function A_lowend = NodeCoupler_final(A,omega,accelerate)

    % ----- Low-energy network -----
    % ----- Create empty matrix -----
    A_low=zeros(length(A));
        
    % ----- Some needed vectors -----
    
    dif_m=sum(A)-sum(A_low+transpose(A_low));
    
    % ----- Create network -----
    % ----- Accelerated part -----    
    
    if accelerate==1,
        degrees=sum(A);
        degrees_degen=degrees;
        omega_degen=omega;
        Max=1;
        Min=0;
        r=0;
        dif=500;
        dif_m=degrees_degen;
        b=3;
        while sum(dif_m)>2*length(A),
            C=A_low+transpose(A_low);
            C(find(C==2))=1;
            dif_m=sum(A)-sum(C);
            sum(dif_m);
            deg_left=sum(degrees_degen);
            a=find(degrees_degen>0);
            if ~isempty(a),
                Max=a(end);
                if length(a)+1>degrees_degen(Max),
                    max_i=find(a==Max);
                    k=a(1:min(end,max_i));
                    Min=k(1:degrees_degen(Max));
                else
                    max_i=find(a==Max);
                    k=a(1:min(end,max_i));
                    Min=k;
                end
                b=find(A_low(Max,Min)==0);
                k=A_low(Max,Min);
                k(b)=1;
                A_low(Max,Min)=k;
                Min_b=Min(b);
                degrees_degen(Min_b)=degrees_degen(Min_b)-1;
                degrees_degen(Max)=degrees_degen(Max)-length(b);
            end
        end
    end
    
    % ----- Slower, but more accurate part -----
    
    p=200:500;
    p=p(end:-1:1);
    for i=1:300,
        for j=p,
            if dif_m(i)>0 && dif_m(j)>0,
                A_low(i,j)=1;
                dif_m(i)=dif_m(i)-1;
                dif_m(j)=dif_m(j)-1;
                dif_m=sum(A)-sum(A_low+transpose(A_low));
            end
        end
        a=round(i/300*100) % percentage finished to print
    end
    A_lowend=A_low+transpose(A_low);
end