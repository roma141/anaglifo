import numpy as np 
'''

array([[ 0,  1,  2,  3],
       [10, 11, 12, 13],
       [20, 21, 22, 23],
       [30, 31, 32, 33],
       [40, 41, 42, 43]])
'''


def f(x,y):
	return 10*x+y

b = np.fromfunction(f,(5,4),dtype=int)
print(b)
print()

print(b[:, 0:-1] )

