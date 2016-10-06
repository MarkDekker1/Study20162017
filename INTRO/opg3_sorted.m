function rbar = opg3_sorted(K,dt,N)
    % ----- Function to calculate order parameter with input K -----
    % ----- Parameters, vectors and matrices -----
    p=1/20;
    T0=50;
    T=100;
    omega=-1+2*rand([N,1]);
    omega=sort(omega);
    theta=zeros([N,(T+T0)/dt]);
    theta(:,1)=normrnd(0,1,[N,1]);

    % ----- Create nearest neighbour network -----
    A=zeros(N);
    for i = 1:N-1,
        A(i,i+1)=1;
    end
    A=A+transpose(A);
    
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