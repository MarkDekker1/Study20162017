clear all
dt=0.1;
N=500;
p=1/20;
T0=50;
T=100;
A = triu(rand(N,N) < p,1); A = A + transpose(A);
omega=-1+2*rand([N,1]);
omega=sort(omega);
theta=zeros([N,(T+T0)/dt]);
theta(:,1)=normrnd(0,1,[N,1]);
% ----- Low-energy network -----
% ----- Create network -----

A_low=zeros(N);
theta_low=zeros([N,(T+T0)/dt]);
theta_low(:,1)=theta(:,1);
degrees=sum(A);
degrees_degen=degrees;
omega_degen=omega;
Max=1;
Min=0;
r=0;
while sum(degrees_degen)>0 && Max~=Min(end),
    a=omega_degen(find(omega_degen~=0));
    Max=find(omega==max(a));
    Min=1:degrees_degen(Max);
    vec=degrees_degen(Min);
    a=degrees_degen(Max);
    while sum(vec==0)>0 && a ~=500,
        for i =1:length(vec),
            if vec(i)==0 && a ~=500,
                Min(end+1)=a+1;
                vec(end+1)=degrees_degen(a+1);
                Min(i)=[];
                vec(i)=[];                
                a=a+1;
            end
        end
    end
    
    
    A_low(Max,Min)=1;
    degrees_degen(Min)=degrees_degen(Min)-1;
    degrees_degen(Max)=0;
    omega_degen(Max)=0;
    r=r+1;
end

A_low=A_low+transpose(A_low);
        