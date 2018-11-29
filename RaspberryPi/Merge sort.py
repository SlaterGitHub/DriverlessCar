import random as rdm
import time

#fil = open("SortTimes.txt", "w")

#print(numbers)
               
def getDigits(array, indx):
    Digits = [None]*indx
    for l in range(indx):
        if (len(array) - 1) < l:
            break
        Digits[l] = array[l]
        if l > 0:
            if Digits[l] < Digits[l-1]:
                Digits.insert(l-1, Digits.pop(l))
    return Digits

def mergeSort(array, indx, finalArray):
    loop = len(array)/indx
    #print(loop)
    excess = len(array) - loop*indx
    for loop in range((len(array))/indx):
        tempArray = []
        tempArray = getDigits(array[(indx*loop):((indx*loop)+(indx))], indx)
        for j in range(len(tempArray)):
            finalArray.append(tempArray[j])
            
    if excess != 0:
        mergeSort(array[((len(array))-excess):(len(array))], excess, finalArray)

    
    return finalArray 

def listSorted(array):
    for m in range(len(array)):
        if m > 0:
            if array[m] < array[m-1]:
                return False
    return True

#print(numbers)
start = time.time()

size = 50000
Range = 1000
numbers = [None]*size
times = []
y = 2
runs = 0

for i in range(size):
    numbers[i] = rdm.randint(0, Range)

secNumbers = numbers
"""    
start = time.time()
while listSorted(numbers) == False:
    numbers = mergeSort(numbers, y, [])
    y += y
    runs += 1
end = time.time()"""

secStart = time.time()
secNumbers = sorted(secNumbers, key=int)
secEnd = time.time()
        
    

#print(numbers)
print(secNumbers)
#print(runs)
#print(end-start)
print(secEnd - secStart)

    
    
        



    
        

