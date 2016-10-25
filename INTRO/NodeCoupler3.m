function A_lowend = NodeCoupler3(A,omega)

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
    while sum(dif)>300,
        dif=sum(A)-sum(A_low+transpose(A_low));
        a=find(dif>0);
        Max=a(end);
        Min_raw=a(1:min(length(a),dif(Max)));
        Min=Min_raw(find(Min_raw<Max));
        A_low(Max,Min)=1;
        sum(dif)
        degrees_degen(Max)=degrees_degen(Max)-length(Min);
        degrees_degen(Min)=degrees_degen(Min)-1;
        if ~isempty(Min_raw),
            if Min_raw(1)>=Max,
                A_low(Max,Min_raw(1))=1;
                degrees_degen(Max)=degrees_degen(Max)-length(Min_raw);
                degrees_degen(Min_raw)=degrees_degen(Min_raw)-1;
            end
        end
            
%         a=find(degrees_degen>0);
%         Max=a(end);
%         if length(a)+1>degrees_degen(Max),
%             Min=a(1:degrees_degen(Max));
%         else
%             Min=a;
%         end
%         if length(a)>25,
%             A_low(Max,Min)=1;
%             degrees_degen(Min)=degrees_degen(Min)-1;
%             degrees_degen(Max)=degrees_degen(Max)-length(Min);
%             omega_degen(Max)=0;
%         else
%             b=degrees_degen(a);
%             maxdeg=find(b==max(b));
%             mindeg=find(b==min(b));
%             maxdeg=maxdeg(end);
%             mindeg=mindeg(1);
%             A_low(a(maxdeg),a(mindeg))=1;
%             degrees_degen(a(maxdeg))=degrees_degen(a(maxdeg))-1;
%             degrees_degen(a(mindeg))=degrees_degen(a(mindeg))-1;
%         end       
        r=r+1;
        sum(dif);
    end
    %A_lowend=A_low+transpose(A_low);
    %sum(sum(A))-sum(sum(A_lowend))
end