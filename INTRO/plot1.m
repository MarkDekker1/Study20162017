%Create vector with different K
tic
Rlength=25;
dt=0.1;

r_vec=zeros([Rlength,1]);
k_vec=zeros([Rlength,1]);
for k=1:Rlength,
    K0=1+k/50;
    r_vec(k)=opg1(K0,dt);
    k_vec(k)=K0;
    K0
end

plot(k_vec,r_vec,'LineWidth',2.5,'Color','red')
xlabel('K','FontSize', 15)
ylabel('rbar','FontSize', 15)
set(gca,'FontSize',13)
toc