% ----- Parameters -----
clear all
tic
dt=1;
N=500;
K=10;
p=1/20;
T0=50;
T=100;
R1=[];
R2=[];
E1=[];
E2=[];


for zx=1:1,
    %Construct omega and theta for the unsorted case
    omega=-1+2*rand([N,1]);
    omega=sort(omega);
    theta=zeros([N,(T+T0)/dt]);
    theta(:,1)=normrnd(0,1,[N,1]);
    A = triu(rand(N,N) < p,1); A = A + transpose(A);

    % ----- Calculate Results -----
    Results=opg4(K,dt,omega,theta,A,T0,T,1);
    R1(end+1)=Results(1);
    R2(end+1)=Results(2);
    E1(end+1)=Results(3);
    E2(end+1)=Results(4);
end

%%
B=NodeCoupler_final(A,omega,1);

% ----- Calculate Results -----

figure
subplot(1,3,1);
spy(A)
subplot(1,3,2);
spy(B)
subplot(1,3,3);
plot(sum(A)-sum(B))

toc