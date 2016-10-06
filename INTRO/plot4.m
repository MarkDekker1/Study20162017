% ----- Parameters -----
clear all
tic
dt=1;
N=500;
K=10;
p=1/20;
T0=50;
T=100;

%Construct omega and theta for the unsorted case
omega=-1+2*rand([N,1]);
omega=sort(omega);
theta=zeros([N,(T+T0)/dt]);
theta(:,1)=normrnd(0,1,[N,1]);
A = triu(rand(N,N) < p,1); A = A + transpose(A);

% ----- Calculate Results -----
Results=opg4(K,dt,omega,theta,A,T0,T);
rbar=Results(1);
rbar_low=Results(2);
E=Results(3);
E_low=Results(4);
Results
%%
B=NodeCoupler(A,omega);

% ----- Calculate Results -----

figure
subplot(1,2,1);
spy(A)
subplot(1,2,2);
spy(B)

toc