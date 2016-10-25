function rbar = opg2(K,dt,theta,omega,A)
    % ----- Function to calculate r with input K in ER network-----
    % ----- Parameters, vectors and matrices -----
    p=1/20;
    N=500;
    T0=50;
    T=100;

    % ----- Timeloop -----
    for t = 1:(T0+T)/dt,
        for i = 1:N,
            summation=A(i)*sin(theta(:,t)-theta(i,t));
            theta(i,t+1)=theta(i,t)+dt*(omega(i)+K/N*sum(summation));
        end
    end
    
    % ----- Calculate order parameter -----  
    r=abs(sum(exp(1i*theta)))/N;
    rbar=sum(r(T0/dt:(T0+T)/dt))*dt/T;
end