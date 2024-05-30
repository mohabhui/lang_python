'''
---------------------
python 3
Author: mohabhui
Date: 26-Sep-2021
---------------------
'''
import math

# rost -> round and string; input data are floating point
# used for printing
def rost(mydata):
    return str(round(mydata,3))


# roli -> round list items where items are floating point
# used for printing
def roli(mylist):
    alist = []
    for i in range(len(mylist)):
        alist.append(round(mylist[i], 3))
    return alist

def prettyPrintList(mylist):
    mystr = ""
    for itm in mylist:
        myitm = str(round(itm, 3))
        if mystr == "":
            mystr = myitm
            m = 10-len(myitm)
        else:
            n = 10-len(myitm)
            mystr = mystr + ' '*m + myitm
            m = n

    print(mystr)

# pData -> probability Data
def calcEntropy(pData, entropy = 'jointXY'):
    '''
    (list or list-of-list, str) --> float

    Calculate and return shannon, joint or conditional entropy.

    The entropy parameter independentX is for shannon,
    jointXY for Joint, conditionalYX for conditional entropy of Y over X and
    conditionalXY for conditional entropy of X given Y.

    pData should be one-dimensional array for independentX and two-dimensional array for the rest.

    Data is not rounded at any stage of calculation but rounded for printing purposes only.

    All steps are printed on-screen.

    Probability data can be given as floating point e.g. 0.1 or fraction e.g. 1/10 in the array

    Result of this function can be validated in https://planetcalc.com/8414/

    '''
    if entropy not in ['independentX', 'jointXY', 'conditionalYX', 'conditionalXY']:
        print("Invalid operation request: %s" % (entropy))
        return

    arrDimension = 1
    mdx = [] # marginal distribution of X
    mdy = [] # marginal distribution of Y
    if pData != []:
        if type(pData[0]) == list:
            arrDimension = 2
            for i in range(len(pData)):
                mdy.append(sum(pData[i]))
                for j in range(len(pData[i])):
                    if i == 0:
                        mdx.append(pData[i][j])
                    else:
                        mdx[j] = mdx[j] + pData[i][j]

    if entropy in ['independentX'] and arrDimension != 1:
        print("Invalid data format for operation: %s" % (entropy))
        return

    if entropy in ['jointXY', 'conditionalYX', 'conditionalXY'] and arrDimension != 2:
        print("Invalid data format for operation: %s" % (entropy))
        return

    s = 0.00 # calculation accumulator
    astr = ""
    bstr = ""

    #for presentation
    print('Input Data:')
    if arrDimension == 1: prettyPrintList(pData)
    if arrDimension == 2:
        for row in pData:
            prettyPrintList(row)
        print(f'Marginal distribution of X: {roli(mdx)}')
        print(f'Marginal distribution of Y: {roli(mdy)}')

    print('Entropy: ' + entropy)


    if entropy == 'independentX':
        for p in pData:
            astr = astr + ' + ' + rost(p) + ' × ' + 'log ' + rost(p)
            if p>0: s=s+(p*math.log(p,2))
        print(astr.lstrip(' + ') + ' = ' + rost(s))

    elif entropy == 'jointXY':
        for row in pData:
            t = 0.00 # calculation accumulator
            for p in row:
                if p>0: t=t+(p*math.log(p,2))
                astr = astr + ' + ' + rost(p) + ' × ' + 'log ' + rost(p)
            s=s+t
            print(astr.lstrip(' + ') + ' = ' + rost(t))
            astr = ""
            bstr = bstr + ' + ' + rost(t)
        print(bstr.lstrip(' + ') + ' = ' + rost(s))

    elif entropy == 'conditionalXY':
        for col_index, row in enumerate(pData):
            t = 0.00  # calculation accumulator
            for p, mdy_val in zip(row, mdy):
                if p > 0:
                    t = t + p * math.log(p / mdy_val, 2)
                astr = astr + ' + ' + rost(p) + ' × ' + 'log(' + rost(p) + '/' + rost(mdy_val) + ')'
            s = s + t
            print(astr.lstrip(' + ') + ' = ' + rost(t))
            astr = ""
            bstr = bstr + ' + ' + rost(t)
        print(bstr.lstrip(' + ') + ' = ' + rost(s))



    elif entropy == 'conditionalYX':
        k = []
        for i in range(len(pData)):
            for j in range(len(pData[i])):
                p = pData[i][j]
                if i == 0:
                    if p>0:
                        k.append(p*math.log(p/mdx[j],2))
                    else:
                        k.append(p)
                else:
                    if p>0: k[j] = k[j] + p*math.log(p/mdx[j],2)
                astr = astr + ' + ' + rost(p) + ' × ' + 'log(' + rost(p) + '/' + rost(mdx[j]) + ')'
            print(astr.lstrip(' + ') + ' = ' + rost(k[i]))
            astr = ""
            bstr = bstr + ' + ' + rost(k[i])
        s = sum(k)
        print(bstr.lstrip(' + ') + ' = ' + rost(s))

    s = (-1)*s

    if entropy == 'independentX': print('H(X) = ' + rost(s))
    if entropy == 'jointXY': print('H(X,Y) = ' + rost(s))
    if entropy == 'conditionalYX': print('H(Y|X) = ' + rost(s))
    if entropy == 'conditionalXY': print('H(X|Y) = ' + rost(s))
    print('-'*30)

    return s

if __name__ == "__main__":
    data1 = [1/2, 1/4, 1/8, 1/8]
    data2 = [[0.1, 0, 0], [0.2, 0.3, 0.2],[0, 0, 0.2]]
    data3 = [[1/10,	1/20, 1/40, 1/80, 1/80], [1/20,	1/40, 1/80,	1/80, 1/10],[1/40, 1/80, 1/80, 1/10, 1/20], [1/80,1/80,1/10,1/20,1/40], [1/80,1/10,1/20,1/40,1/80]]
    data4v1 = [[1/8, 1/16, 1/32, 1/32],[1/16, 1/8, 1/32, 1/32],[1/16, 1/16, 1/16, 1/16],[1/4, 0, 0, 0]]
    data4v2 = [[0.125, 0.0625, 0.03125, 0.03125], [0.0625, 0.125, 0.03125, 0.03125], [0.0625, 0.0625, 0.0625, 0.0625], [0.25, 0, 0, 0]]
    data5=[[24/100,25/100], [1/100, 50/100]]


##    calcEntropy(data1, 'independentX')
##    calcEntropy(data2, 'jointXY')
##    calcEntropy(data2, 'conditionalYX')
##    calcEntropy(data2, 'conditionalXY')
    calcEntropy(data5, 'conditionalXY')
