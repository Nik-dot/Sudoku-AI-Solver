#const n = 9.
%* borders of subgrids *%
border(0;3;6).

%* each cells must be filled with a number from 1 to 9 *%
1 {cell(1..n,I,J)} 1 :- J = 0..n-1, I= 0..n-1.
%* In each subgrids each number from 1 to 9 must be present *%
1 {cell(N,I,J): I = 0..n-1, J = 0..n-1, B<=I, I<=B+2, B<=J, J<=B+2} 1 :- border(B), N = 1..n.

%* There cannot be the same number on the same column *%
:- cell(N,I,J), cell(N,I,J2), J!=J2.
%* There cannot be the same number on the same row *%
:- cell(N,I,J), cell(N,I2,J), I!=I2.

#show tile/3.