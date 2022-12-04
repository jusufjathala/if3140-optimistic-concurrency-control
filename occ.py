# Tugas Besar IF3140 2022

import time

class Transaction:
    def __init__(self, txNum): #constructor
        self.txNum = txNum
        self.readWriteList = []
        self.startTS = time.time()
        self.validateTS = 0
        self.finishTS = 0
        
def isTxInMemory(txList, txNum):
    for tx in txList:
        if tx.txNum==txNum :
            return tx

 
def validate(txList,validateList,txVal,txAmounts,txCache):
    #txVal = tj to be validated, tx = ti (other transactions)
    valid = True
    txVal.validateTS = time.time()
    if (validateList): #if validateList not empty
        validOne = True
        validTwo = True
        for tx in txList :
            if (tx.txNum!=txVal.txNum) and (tx.validateTS < txVal.validateTS):
                #check condition 1
                if tx.finishTS > txVal.startTS : 
                    validOne = False 
                    print('c1false')
                #check condition 2
                if (txVal.startTS < tx.finishTS) and (tx.finishTS < txVal.validateTS) : 
                    for write in tx.readWriteList :
                        for read in txVal.readWriteList :
                            #check if intersect exists
                            if (write[0]=="w" and read[0]=="r" and write[1]==read[1]) : 
                                validTwo = False
                                print('c2false')
                
        if (validOne) or (validTwo):
            valid = True
        else :
            valid = False

    if (valid):
        validateList.append(txVal)
        txVal.finishTS = time.time()
        print (str("        "*(txVal.txNum-1))+"validate"+str("        "*(txAmounts-txVal.txNum+2))+"T"+str(txVal.txNum)+" validation success")
    else :
        print (str("        "*(txVal.txNum-1))+"validate"+str("        "*(txAmounts-txVal.txNum+2))+"T"+str(txVal.txNum)+" validation fail, transaction must rollback")
        txVal.startTS = time.time()
        rollbackProcedure(txList,validateList,txAmounts, txCache, txVal.txNum)
        
def rollbackProcedure(txList,validateList,txAmounts, txCache, txNum):
    tx = isTxInMemory(txList,txNum)
    print(str("        "*(tx.txNum-1)+"rollback"))
    txWords = txCache[txNum]
    words = txWords.split(',')
    for idx,word in enumerate(words):
        if ("r" in word ) or ("w" in word ):
            if ("r" in word ):
                print(str("        "*(tx.txNum-1)+"read "+word[1]))
            if ("w" in word ):
                print(str("        "*(tx.txNum-1)+"write "+word[1]))
    validate(txList,validateList,tx,txAmounts,txCache)
    
def updateCache(cache ,txNum, word):
    temp = cache[txNum]
    newCache = word
    if (temp!=None):
        newCache = temp+","+word
    cache.update({txNum:newCache})                  
                    
def main():
    #initialize
    txList = []
    validateList = []
    filename = input("Input filename: ")
    file = open(filename, 'r')
    lines = file.read().splitlines()
    words = lines[1].split(',')
    txAmounts = len(words[1])+1   
    txCache = dict.fromkeys((range(1,txAmounts+1)))
    
    for idx,word in enumerate(words):
        print ("T"+str(idx+1)+" "*(6-len(str(txAmounts))), end =" ")
    print()    
    
    for line in lines:
        words = line.split(',')   
        for idx,word in enumerate(words):
            txNum=idx+1
            if ("r" in word ) or ("w" in word ):
                #check if new transaction
                if not (isTxInMemory(txList, txNum)) :
                    txList.append(Transaction(txNum))
                tx = isTxInMemory(txList,txNum)
                tx.readWriteList.append(word)
                if ("r" in word ):
                    print(str("        "*(tx.txNum-1)+"read "+word[1]))
                if ("w" in word ):
                    print(str("        "*(tx.txNum-1)+"write "+word[1]))
                updateCache(txCache,txNum,word)
            if ("v" in word ):
                tx = isTxInMemory(txList,txNum)
                validate(txList,validateList,tx,txAmounts,txCache)
            time.sleep(0.001)
    
if __name__ == '__main__':
    main()