% ----- Parameters -----
tic
Rlength=10;
dt=1;
N_vec=[100,250,500,750,1000];
L_vec=zeros([length(N_vec),1]);
r_mat=zeros([length(N_vec),Rlength]);

%Construct omega and theta for the unsorted case
omega=-1+2*rand([N,1]);
theta=zeros([N,(T+T0)/dt]);
theta(:,1)=normrnd(0,1,[N,1]);

% ----- Loop to calculate r with varying K -----
for n=1:(length(N_vec)),
    N0=N_vec(n);
    r_vec=zeros([Rlength,1]);
    k_vec=zeros([Rlength,1]);
    for k=1:Rlength,
        K0=k;
        r_mat(n,k)=opg3(K0,dt,N0,theta,omega);
        k_vec(k)=K0;
    end
    L_vec(n) = mean(mean(graphallshortestpaths(sparse(A))))*N0/(N0-1);
    n
end
toc
%%
% ----- Plot -----
colormap jet
contourf(k_vec,N_vec,r_mat,10)
xlabel('Coupling strength $K$','Interpreter','latex','FontSize', 15)
ylabel('Number of oscillators $N$','Interpreter', 'latex','FontSize', 15)
set(gca,'FontSize',13)
colorbar()
caxis([0,0.12])

%%
% For the sorted array

Rlength=10;
dt=1;
N_vec=[100,250,500,750,1000];
L_vec=zeros([length(N_vec),1]);
r_mat=zeros([length(N_vec),Rlength]);

% Sort the omega array:
omega=sort(omega);
% 

% ----- Loop to calculate r with varying K -----
for n=1:(length(N_vec)),
    N0=N_vec(n);
    r_vec=zeros([Rlength,1]);
    k_vec=zeros([Rlength,1]);
    for k=1:Rlength,
        K0=k;
        r_mat(n,k)=opg3(K0,dt,N0,theta,omega);
        k_vec(k)=K0;
    end
    L_vec(n) = mean(mean(graphallshortestpaths(sparse(A))))*N0/(N0-1);
    n
end
toc
%%
% And for the sorted array
% ----- Plot -----
colormap jet
contourf(k_vec,N_vec,r_mat,10)
xlabel('Coupling strength $K$','Interpreter','latex','FontSize', 15)
ylabel('Number of oscillators $N$','Interpreter', 'latex','FontSize', 15)
set(gca,'FontSize',13)
colorbar()
caxis([0,0.12])