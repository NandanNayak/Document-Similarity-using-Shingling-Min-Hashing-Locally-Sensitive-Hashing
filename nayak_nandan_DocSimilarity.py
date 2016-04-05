#Import all the modules
import os
import math
import itertools
import sys

#Replace these values with arguments
#path="D:/Toshiba Desktop/Desktop/USC/Spatial_Informatics/Spring 2016/INF 553 - DM/Assignments/Assignment3/Assignment3/Assignment3/Docs/"
path=sys.argv[1]
k=sys.argv[2]
typeOfShingles=sys.argv[3]
hashes=sys.argv[4]
s=sys.argv[5]

#Convert string arguments to int/float
k=int(k)
hashes=int(hashes)
s=float(s)

#Global Variables
hashMatrix=[]
fileList=[]
shingle=[]
shingleList=[]
uniqueShingleList=[]
Matrix=[]
sigMatrix=[]
isPrint=False
weight=0.2
simDocs=[]

#Define all functions
def getShingles(line):
    global k
    global typeOfShingles
    global path
    
    shingleList=[]
    #line=myFile.read()
    if typeOfShingles=='word':        
        line=line.split()
    lenLine=len(line)
    if isPrint==True:
        print line
    for i in range(lenLine-k+1):
        shingle=[]
        for j in range(k):
            shingle.append(line[i+j])    
        shingle="".join(shingle)
        if shingle not in shingleList:
            shingleList.append(shingle)
    shingleList.sort()
    return shingleList

def compare(list1,list2,listType):
    intersection=0
    if listType=="shingles":
        for shingle in list1:
            if shingle in list2:
                intersection +=1
    else:
        for i in range(len(list1)):
            if list1[i]==list2[i]:
                intersection+=1
    return intersection

def JacSim(list1, list2,listType):
    len1=len(list1)
    len2=len(list2)
    if len1<=len2:
        intersection=compare(list1,list2,listType)        
    else:
        intersection=compare(list2,list1,listType)
    if listType=="shingles":
        union=len1+len2-intersection
    else:
        union=len1
    sim=float(intersection)/float(union)
    #print "I:%d  U:%d  S:%f"%(intersection,union,sim)
    return sim

def createColMatrix(inList):
    global uniqueShingleList
    colMatrix=[]
    for shingle in uniqueShingleList:
        if shingle in inList:
            colMatrix.append(1)
        else:
            colMatrix.append(0)
    return colMatrix

def createHashColMatrix(i):
    global uniqueShingleList
    tempList=[]
    for j in range(len(uniqueShingleList)):
        val=((i*j)+1)%len(uniqueShingleList)
        tempList.append(val)
    return tempList

def fillCol():
    tempList=[]
    for i in range(hashes):
        tempList.append(len(uniqueShingleList))
    #print tempList  #
    return tempList

def createSigCol(inList):
    global hashMatrix
    sigCol=fillCol()
    for i in range(len(inList)):
        if inList[i]==1:
            for j in range(hashes):
                if sigCol[j]>hashMatrix[j][i]:
                    sigCol[j]=hashMatrix[j][i]   
            
    return sigCol
    
def inRange(v,s):
    global weight
    lowLimit=s-weight
    upLimit=s+weight
    #weight +=0.05
    if v>lowLimit and v<upLimit:
        return True
    return False

#Code
if __name__=='__main__':

#################
#Task1:Shingling#
#################
    path=path+'/'
    for fileName in os.listdir(path): #Enter the path       
        if fileName.endswith(".txt"): # Grep for files ending with .txt
            fileName=path+fileName
            fileList.append(fileName)
            myFile=open(fileName,"r+")
            shingleListTemp=[]
            line=myFile.read()  #Read the line from the file
            shingleListTemp=getShingles(line)      #Get shingles from the line      
            print "No of Shingles in File %s:%d"%(fileName,len(shingleListTemp))
            shingleList.append(shingleListTemp) #Maintain a list of lists - each list having shingles from each file
            
    if isPrint==True:
        print shingleList
            

    for i in range(len(shingleList)-1):
        for j in range(i+1,len(shingleList)): #Compare shingles of pair of files 
            sim=JacSim(shingleList[i],shingleList[j],"shingles") #Compute Jacard similarity
            print "Jaccard Similarity between %s and %s:%.12f"%(fileList[i],fileList[j],sim)


###################
#Task2:Min Hashing#
###################
    #Get unique shingles from all files and store it in uniqueShingleList
    uniqueShingleList=[]
    for i in range(len(shingleList)):        
        for j in range(len(shingleList[i])):
            if shingleList[i][j] not in uniqueShingleList:
                    uniqueShingleList.append(shingleList[i][j])

    uniqueShingleList.sort() #Sort the list
    if isPrint==True:
        print uniqueShingleList 
        print
        print shingleList
    for i in range(len(fileList)):
        colMatrix=createColMatrix(shingleList[i]) #Create a boolean vector for each file; If Shingle from uniqueShingleList is present in current file, mark 1 else 0
        if isPrint==True:
            print "ShingleList[%d]:"%(i) #
            print shingleList[i]    #
            print colMatrix     #
        Matrix.append(colMatrix)  # Append the boolean vectors representing each file to a list; Maintain a boolean matrix

    if isPrint==True:
        print
        print
        print Matrix

#For each row index, generate its hash value (based on hash function) and generate a column vector for each hash Function        
    for i in range(1,hashes+1):        
        tempList=createHashColMatrix(i)
        hashMatrix.append(tempList) # Append all column vectors and create a matrix
        
    if isPrint==True:
        print hashMatrix

#Now for each boolean vector, check if it 1 in its row. If 1, then get the corresponding hash value from the hash column vector
#Make sure to enter the lowest hash value for each row    
    tempList=[]    
    print "\nMin-Hash Signature for the Documents"
    for i in range(len(fileList)):
        tempList=createSigCol(Matrix[i])
        print "%s:"%(fileList[i]),
        print tempList
        sigMatrix.append(tempList) # Append all column vectors and create a matrix

#Compare each pair of list in the above matrix and generate Jacard similarity    
    for i in range(len(sigMatrix)-1):
        for j in range(i+1,len(sigMatrix)):
            sim=JacSim(sigMatrix[i],sigMatrix[j],"vectors")
            print "Jaccard Similarity between %s and %s:%.12f"%(fileList[i],fileList[j],sim)
            tempList=[]
            if sim>s: #Pairs which satisfy the threshold s are truely similar
                tempList.append(fileList[i])
                tempList.append(fileList[j])
                tempList.sort()
                tempTup=tuple(tempList)
                if tempTup not in simDocs:
                    simDocs.append(tempTup) #Maintain a list of all pairs of similar documents

    
#################################
#Task3:Locally Sensitive Hashing#    
#################################
    n=hashes
    flag=True

#COmpute the optimum value of band b and row r. n is the no. of hash functions
    noOfRows=0
    while flag:
        noOfRows+=1
        for r in range(noOfRows,hashes,noOfRows): #Start with minimum value for rows and increment until s~(1/b)^(1/r)
            b = float(n)/float(r)
            b=math.ceil(b)
            base=float(1)/float(b)
            exp=float(1)/float(r)
            val = float((base)**(exp)) #Using the formula, (1/b)^(1/r)
            if isPrint==True:
                print "b:%d  r:%d  val:%f"%(b,r,val)
            if inRange(val,s): #if (1/b)^(1/r)~s, then break the loop
                flag=False
                break
    b=int(b)
    r=int(r)
    #if isPrint==True:
    print "b:%d  r:%d"%(b,r)

#Generate a empty list for storing bands of each file
    lshMatrix=[]
    for i in range(len(fileList)):
        lshMatrix.append([])

    
    for i in range(len(sigMatrix)):
        colList=sigMatrix[i] # Get the column containing hash values for each file
        offset=0
        for band in range(b): #For each file, Split the column containing hash values into bands
            tempList=[]
            for row in range(r):
                tempList.append(colList[row+offset])
            tempList.sort()#Sort rows in each band
            offset+=r
            lshMatrix[i].append(tuple(tempList))#Store the bands into appropriate lists in lshMatrix
    if isPrint==True:
        print lshMatrix

#Create a dictionary  that contains unique bands from all documents
#Key is the band
#Value is the document name
    lshDict={}
    for i in range(len(sigMatrix)):
        for j in range(b):
            if lshMatrix[i][j] not in lshDict:
                lshDict[lshMatrix[i][j]]= [fileList[i]] 
            else:
                if fileList[i] not in lshDict[lshMatrix[i][j]]:
                    lshDict[lshMatrix[i][j]].append(fileList[i]) #Append multiple filenames if the band(key) is found in those documents
    if isPrint==True:
        print lshDict

#Create a list of pairs of similar documents
    pairList=[]
    for key in lshDict:
        if len(lshDict[key])>1: #Keys having more than one file name indicate their occurance in multiple files
            tempPairs=list(itertools.combinations(lshDict[key],2))#Generate pairs from the value of those keys using itertools
            for pair in tempPairs:
                if pair not in pairList:
                    pairList.append(pair)
    if isPrint==True:
        print pairList

#Cross check if the pairs are truely similar, by checking if they satisfy threshold value s
    print "\nCandidate pairs obtained using LSH"
    for i in range(len(simDocs)):
        if simDocs[i] in pairList :
            print simDocs[i]








    
