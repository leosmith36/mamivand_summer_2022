# Calculates the value of each parameter and returns a list

import math

D10 = D30 = 1e-4
D20 = 2e-5
Q1 = Q3 = 294e3
Q2 = 308e3

R = 8.314
T = 873
c1 = 0.46
c2 = 0.31
c3 = 0.23

D1 = D3 = D10*math.exp(-Q1/(R*T))
D2 = D20*math.exp(-Q2/(R*T))

M22 = float('%.5e' %((c1*c2*D1 + (1-c2)**2*D2 + c2*c3*D3)*(c2/(R*T))))
M33 = float('%.5e' %((c1*c3*D1 + c2*c3*D2 + (1-c3)**2*D3)*(c3/(R*T))))
M23 = float('%.5e' %((c1*D1 - (1-c2)*D2 - (1-c3)*D3)*((c2*c3)/(R*T))))

def main():
    #print(M22,M33,M23,1e-14)
    return [M22,M33,M23,1e-14]
    

if __name__=="__main__":
    main()
