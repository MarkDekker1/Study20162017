function A_lowend = NodeCoupler2(A,omega)

    % ----- Low-energy network -----
    % ----- Create empty matrix -----
    A_low=zeros(length(A));
        
    % ----- Create network -----
    
    degrees=sum(A);
    degrees_degen=degrees;
    omega_degen=omega;
    Max=1;
    Min=0;
    r=0;
    dif=500;
    dif_m=degrees_degen;
    b=3;
    while sum(dif_m)>15000000,%length(b)>0,%sum(degrees_degen)>396,
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
%             else
%                 b=find(A_low(a,a)==0);
%                 k=A_low(a,a);
%                 k(b)=1;
%                 A_low(a,a)=k;
%                 %A_low(a,a)(b)=A_low(a,a)(b)+1;
%                 degrees_degen(a)=degrees_degen(a)-1;
%                 
%                 m=0;
%                 i=0;
%                 
%                 while m==0,
%                     %b=degrees_degen(a);
%                     maxdeg=a(end-i);%find(b==max(b));
%                     mindeg=a(1);%find(b==min(b));
%                     i
%                     if A_low(maxdeg,mindeg)==0,
%                         A_low(maxdeg,mindeg)=1;
%                         degrees_degen(maxdeg)=degrees_degen(maxdeg)-1;
%                         degrees_degen(mindeg)=degrees_degen(mindeg)-1;
%                         m=1;
%                     else
%                         i=i+1;
%                     end
%                 end
                %sum(dif_m)-sum(deg_left)
        end
        r=r+1;
%         if sum(degrees_degen)==0 && sum(dif)>0,
%             a=find(dif>0);
%             for i=1:length(a)-1,
%                 Max=a(end-i);
%                 Min=a(i);
%                 A_low(Max,Min)=1;
%             end
%         end
        %dif=sum(sum(A)-sum(A_low+transpose(A_low)))
%         sum(dif)
    end
    i=0;
    dif_m=sum(A)-sum(A_low+transpose(A_low));
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
        i
    end
            
    
%     for i=1:28,
%         k=find(degrees_degen>0);
%         K=find(A_low(k(end-i),k)==0);
%         k(K)
%         k(end)
%         A_low(k(end),k(K))=1;
%         C=A_low+transpose(A_low);
%         C(find(C==2))=1;
%         dif_m=sum(A)-sum(C);
%     end
%     sum(dif_m)
    
    C=A_low+transpose(A_low);
    C(find(C==2))=1;
    A_lowend=C;
end