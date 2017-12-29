import numpy as np



def pos_n(data, n):

    var = np.where(data == n)
    i=var[0][0]
    j=var[1][0]
    #print var
    #print i,j
    return [i,j]

filename = "input.txt"
data = np.loadtxt(filename)
data = data.astype(int)
print pos_n(data,10)