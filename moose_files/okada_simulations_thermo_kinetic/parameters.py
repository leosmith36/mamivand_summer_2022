# Calculates the value of each parameter and returns it for csvgen.py files

import math
from xml.etree.ElementTree import C14NWriterTarget

D10 = D30 = 1e-4
D20 = 2e-5
Q1 = Q3 = 294e3
Q2 = 308e3

R = 8.314
T = 873
c2 = 0.31
c3 = 0.23
c1 = 1 - c2 - c3

D1 = D3 = D10*math.exp(-Q1/(R*T))
D2 = D20*math.exp(-Q2/(R*T))

M22 = float('%.5e' %((c1*c2*D1 + (1-c2)**2*D2 + c2*c3*D3)*(c2/(R*T))))
M33 = float('%.5e' %((c1*c3*D1 + c2*c3*D2 + (1-c3)**2*D3)*(c3/(R*T))))
M23 = float('%.5e' %((c1*D1 - (1-c2)*D2 - (1-c3)*D3)*((c2*c3)/(R*T))))
LAB = float('%.5e' %(20500 - 9.68*T))
LAC = float('%.5e' %(-23669 + 103.9627*T - 12.7886*T*math.log(T)))
LBC = float('%.5e' %((24357 - 19.797*T) - 2010*(c3 - c2)))


def main():
    print(M22,M33,M23,1e-14,LAB,LAC,LBC)
    return [M22,M33,M23,1e-14,LAB,LAC,LBC]
    

if __name__=="__main__":
    main()
