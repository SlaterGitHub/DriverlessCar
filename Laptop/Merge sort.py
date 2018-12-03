import random as rdm
import time
#import libraris

def getDigits(Digits, indx):
    for l in range(indx):
        if (len(Digits) - 1) < l:
            break
        #if the length of the array is less than 1 then end process

        if l > 0:
            if Digits[l] < Digits[l-1]:
                Digits.insert(l-1, Digits.pop(l))
        """when the loop has passed more than once if the value in index of
        digits is less than the value in the cell before, swap the values"""
    return Digits

def mergeSort(array, indx, finalArray):
    loop = len(array)/indx
    #Find how many times the array can be run before running out of cells
    excess = len(array) % indx
    #Find how many cells will be left in an excess
    for loop in range(loop):
        #runs loop times for every loop
        tempArray = getDigits(array[(indx*loop):((indx*loop)+(indx))], indx)
        for j in range(len(tempArray)):
            finalArray.append(tempArray[j])

    if excess != 0:
        mergeSort(array[((len(array))-excess):(len(array))], excess, finalArray)
    #run the excess values through mergeSort as their own array

    return finalArray

def listSorted(array):
    for m in range(len(array)-1):
        if array[m+1] < array[m]:
            return False
    return True
    #Check the array to make sure each value is in order from smallest to biggest

size = 50
Range = 1000
numbers = [None]*size
y = 2
runs = 0

for x in range(size):
    numbers[x] = rdm.randint(1, Range)

while listSorted(numbers) == False:
    numbers = mergeSort(numbers, y, [])
    y += y
    runs += 1

print(numbers)
