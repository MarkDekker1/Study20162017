% ----- Parameters -----
tic
Rlength=50;
dt=0.1;

r_vec=zeros([Rlength,1]);
k_vec=zeros([Rlength,1]);
for k=1:Rlength,
    K0=k;
    r_vec(k)=opg2(K0,dt);
    k_vec(k)=K0;
    K0
end
L = mean(mean(graphallshortestpaths(sparse(A))))*N/(N-1)

plot(k_vec,r_vec,'LineWidth',2.5,'Color','red')
xlabel('K','FontSize', 15)
ylabel('rbar','FontSize', 15)
set(gca,'FontSize',13)
toc