function Energy = CouplingEnergy(A,omega)
%     omega_mat=zeros(length(omega));
%     for i=1:length(omega),
%         omega_mat(i,:)=omega;
%     end
%     Energy=0.5*sum(sum(A*omega_mat*omega_mat));
    
    N=length(A);
    summation=zeros([N,N]);
    for i=1:N,
        for k=1:N,
            summation(k,i)=A(k,i)*omega(k)*omega(i);
        end
    end
    Energy=sum(sum(summation));
        
end