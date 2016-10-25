function Results = opg4(K,dt,omega,theta,A,T0,T,accelerate)
    % ----- Function to calculate order parameter with input K -----
    % ----- Parameters, vectors and matrices -----
    N=length(omega);
        
    % ----- Timeloop regular A -----
    for t = 1:(T0+T)/dt,
        for i = 1:N,
            summation=A(i)*sin(theta(:,t)-theta(i,t));
            theta(i,t+1)=theta(i,t)+dt*(omega(i)+K/N*sum(summation));
        end
    end
    
    % ----- Calculate order parameter regular A -----
    r=abs(sum(exp(1i*theta)))/N;
    rbar=sum(r(T0/dt:(T0+T)/dt))*dt/T;
    E=CouplingEnergy(A,omega);
        
    % ----- Low-energy network -----
    % ----- Create network -----
    A_low=NodeCoupler_final(A,omega,accelerate);
    theta_low=zeros([N,(T+T0)/dt]);
    theta_low(:,1)=theta(:,1);            
    
    % ----- Timeloop low-energy A -----
    for t = 1:(T0+T)/dt,
        for i = 1:N,
            summation=A_low(i)*sin(theta_low(:,t)-theta_low(i,t));
            theta_low(i,t+1)=theta_low(i,t)+dt*(omega(i)+K/N*sum(summation));
        end
    end
    
    % ----- Calculate order parameter low-energy A -----
    r_low=abs(sum(exp(1i*theta_low)))/N;
    rbar_low=sum(r_low(T0/dt:(T0+T)/dt))*dt/T;
    E_low=CouplingEnergy(A_low,omega);
    
    % ----- Save results -----
    Results=[rbar,rbar_low,E,E_low];
    
end