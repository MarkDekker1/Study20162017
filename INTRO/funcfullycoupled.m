function boo=funcfullycoupled(A)
   % Function to determine whether adjacency matrix A is fully coupled.
   k = length(A);
   B = A^k;
   if(min(B)~=0),
       boo = 1;
   else
       boo = 0;
   end