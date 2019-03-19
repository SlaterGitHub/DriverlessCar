import random as rdm
import time
"""import libraries"""

def getDigits(data, lower, upper, indx, l):
    Digits = [i[l] for i in data][lower:upper]
    for l in range(indx):
        if (len(Digits) - 1) < l:
            break
        #if the length of the array is less than 1 then end process

        if l > 0:
            if Digits[l] < Digits[l-1]:
                tempHold = data[l]
                data[l] = data[l-1]
                data[l-1] = tempHold

        """when the loop has passed more than once if the value in index of
        digits is less than the value in the cell before, swap the values"""
    return data

def mergeSort(data, indx, l):
    loop = len([i[l] for i in data])/indx
    #Find how many times the array can be run before running out of cells
    excess = len([i[l] for i in data]) % indx
    #Find how many cells will be left in an excess
    for loop in range(loop):
        #runs loop times for every loop
        data = getDigits(data, (indx*loop), ((indx*loop)+(indx)), indx, l)
    if excess != 0:
        mergeSort(data, excess, l)
    #run the excess values through mergeSort as their own array

    return data

def listSorted(array):
    for m in range(len(array)-1):
        if array[m+1] < array[m]:
            return False
    return True
    #Check the array to make sure each value is in order from smallest to biggest

def sort(data, l):
    y = 2
    while listSorted([i[l] for i in data]) == False:
        data = mergeSort(data, y, l)
        y += y
    return data
