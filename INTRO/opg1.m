function rbar = opg1(K,dt)
    % ----- Function to calculate order parameter with input K -----
    % ----- Parameters, vectors and matrices -----
    p=1/20;
    N=500;
    T0=50;
    T=100;

    A=ones(N)-eye(N);
    omega=-1+2*rand([N,1]);

    theta=zeros([N,(T+T0)/dt]);
    theta(:,1)=normrnd(0,1,[N,1]);

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