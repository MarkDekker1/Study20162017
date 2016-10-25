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

%And after the shuffling procedure of exercise 4:
B = NodeCoupler(A,omega); B = B + transpose(B);

q = 100;
C = shuffle5(B,omega,q,N);

figure
%plot(1,2,1);
spy(C)
title('The matrix A','FontSize', 20)
%ylabel('rbar','FontSize', 15)
set(gca,'FontSize',13)

toc
%%
tic
%Calculating rbar(K)
%dt can be reduced for a higher resolution
dt = 0.5;
Rlength=50;
r_vec=zeros([Rlength,1]);
k_vec=zeros([Rlength,1]);

for k=1:Rlength,
    K0=k;
    r_vec(k)=opg2(K0,dt,theta,omega,B);
    k_vec(k)=K0;
    K0
end

plot(k_vec,r_vec,'LineWidth',2.5,'Color','red')
xlabel('K','FontSize', 15)
ylabel('rbar','FontSize', 15)
set(gca,'FontSize',13)

toc
%%
tic
%The average path length:
L = mean(mean(graphallshortestpaths(sparse(B))))*N/(N-1);

toc




