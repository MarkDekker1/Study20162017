k = 1:250;
X=1:500;
Y=1:500;
XY=[X;Y];
XY=transpose(XY);
%[A,XY] = bucky;
[X2,Y2]=find(B==1);
XY2=[X2,Y2];
%XY2=transpose(XY2);
a=length(find(B==1));
b=ones(a);

gplot(b,XY2,'-*')
axis square