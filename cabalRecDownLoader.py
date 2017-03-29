#!/usr/bin/python

import os, sys
import subprocess, sys, re
import urllib2, re, sys, Queue
from sys import argv

pkgName = sys.argv[1]
pkgVersion = sys.argv[2]
sandboxPath = sys.argv[3]
pkgFolder = pkgName+"-"+pkgVersion

queue=[]
downQueue=[]
print pkgName
print pkgVersion
print sandboxPath

# fun to resolve dependency of main package
def resolveDep(listOfDep):
    for x in listOfDep:
        #if (len(listOfDep) < 0):
        wrapper(x[0],x[1].strip(),sandboxPath)

# fun to get the exact version from html page for downloading package
def getVerFromHTML(listOfDep):
    semiQueue = []
    def getVerList(string,pkg,ver):
        temp = []
        for x in range(0,len(string)):
            if string[x]=='o' and string[x+1]=='n' and string[x+2]=='s' and (ord(string[x+3]) > 47 and ord(string[x+3]) < 58):
                y=x+3
                break
        for x in range(y,len(string)):
            if (string[x])=='C' or (string[x]=='('):
                    break
            temp.append(string[x])
        temp = ((''.join(temp)).split(','))
        exact = []
        for x in temp:
            if (cmp(ver,x)) == 1:
                exVer = x
        return (pkg,exVer)
    print listOfDep
    for x in listOfDep:
        text = subprocess.check_output("python internetBackup3.py "+x[0],shell=True)
        if (text != "Not Found\n") or (x[0] != "rts"):
            dep = getVerList(text,x[0],x[1])
            semiQueue.append(dep)
        return resolveDep(semiQueue)

# function to get list of dependency and give list of to be downloade
def getDepList(listOfDep):
    exPack = subprocess.check_output("ghc-pkg list",shell=True)
    exPack = filter(None,exPack.split('\n'))
    del exPack[0]
    def removeSpcae(string):return(string.replace(' ',''))
    exPack = map(removeSpcae,exPack)
    def makeTupple(string):
        outString1 = []
        outString2 = []
        for x in range(0,len(string)-1):
            if(string[x]=='-'):
                if((ord(string[x+1])) > 47 and (ord(string[x+1])) < 59):
                    y=x+1
                    break
            outString1.append(string[x])
        for x in range(y,len(string)-1):
            outString2.append(string[x])
        return ((''.join(outString1)),(''.join(outString2)))
    exPack = map(makeTupple,exPack)

    #exPack has existing Packages and
    #listOfdep has dependency packages

    tobeDown = [] # to be downloaded packages
    existPkg = [] # existed with exact version
    def checkIfExist(depPack,exPack):
        for x in depPack:
            for y in exPack:
                if(x[0] == y[0]):
                    ver1 = x[1]
                    ver2 = y[1]
                    ver2 = ver2[:len(ver1)]
                    if (cmp(ver1,ver2)) == 0:
                        existPkg.append(x)
    def checkNoExist(depPack,existPkg):
        for x in depPack:
            if (x in existPkg) == False:
                tobeDown.append(x)

    checkIfExist(listOfDep,exPack)
    checkNoExist(listOfDep,existPkg)
    # Here i got list of package which are either not present or version of them is not matching with existing package

    getVerFromHTML(tobeDown)



    

# function to analyze cabal file and gives dependecny list
def cabalAnalyzer(pkgName,pkgVersion):
    def removeSpcae(string):return(string.replace(' ',''))
    text = subprocess.check_output("python internetBackup2.py "+pkgName+" "+pkgVersion,shell=True)
    firstIndex = 0
    secondIndex = 0
    for x in range(0,len(text)-1):
        if (text[x]=='c') and (text[x+1]=='i'):
            if (text[x+2]=='e') and (text[x+3]=='s'):
                firstIndex = x+4
                break
    for x in range(firstIndex,len(text)-1):
        if (text[x]=='[') and (text[x+1]=='d'):
            if (text[x+2]=='e') and (text[x+3]=='t'):
                secondIndex = x
                break
    text = text[firstIndex:secondIndex]
    text = removeSpcae(text)
    text = text.split(',')

    def makeTupple(string):
       first = 0
       firstTup = []
       sndTup = []
       for x in range(0,len(string)-1):
           if (string[x]=='('):
               first = x
               break
           firstTup.append(string[x])
       for x in range(0,len(string)-1):
           if ord(string[x]) > 45 and ord(string[x]) < 58:
               sndTup.append(string[x])
       #for x in range(first,len(sndTup)-1):
           #if (ord(string[x])) > 45 and  (ord(string[x])) < 58:
       return ((''.join(firstTup)),(''.join(sndTup)))

    text = map(makeTupple,text)
    return getDepList(text)


def downLoadPkg(pkgName,pkgVersion,sandboxPath):
    os.system("mkdir -p "+sandboxPath)
    url = "wget -c https://hackage.haskell.org/package/"+pkgName+"-"+pkgVersion+"/"+pkgName+"-"+pkgVersion+".tar.gz -P "+sandboxPath+"/"+pkgName+"-"+pkgVersion
    print "\n"+url+"\n"
    downId = os.system(url)
    print sandboxPath+"/"+pkgName+"-"+pkgVersion+"/"+pkgName+"-"+pkgVersion+".tar.gz"
    tarPath = sandboxPath+"/"+pkgName+"-"+pkgVersion+"/"+pkgName+"-"+pkgVersion+".tar.gz"

    os.system("tar -xzf "+tarPath +" -C "+sandboxPath)
    if downId != 0:
        print "Package or version is invalid"
    tup = ((pkgName,pkgVersion),(url))
    queue.append(pkgName)
    downQueue.append(tup)
    cabalFilePath = sandboxPath+"/"+pkgName+"-"+pkgVersion+"/"+pkgName+".cabal"
    print cabalFilePath
    return cabalAnalyzer(pkgName,pkgVersion)


def wrapper(pkgName,pkgVersion,sandboxPath):
    downLoadPkg(pkgName,pkgVersion,sandboxPath)
wrapper(pkgName,pkgVersion,sandboxPath)
#print (downQueue)
print (queue)

# in wrapper function while giving recursive call i have to check the package is already downloaded or not.
# better maintain seperate list for that
