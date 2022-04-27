import sys
import time
from math import log2

class LZWAlgorithm:
    def encode(self,file):
        result=[]
        dictionary={}
        code=256
        for i in range(code):
            dictionary[bytes([i])] = i
        with open(file, "rb") as f:
            current=f.read(1)
            while True:
                next=f.read(1)
                if dictionary.get(current+next) is not None:
                    current=current+next
                else:
                    result.append(dictionary.get(current))
                    dictionary[current+next]=code
                    code=code+1
                    current=next
                if not next:
                    break
        result.append(dictionary.get(current))
        return result

        
    def decode(self,encoded):
        result=[]
        dictionary={}
        code=256
        for i in range(code):
            dictionary[i]=bytes([i])
        previous=encoded[0]
        previousDict=dictionary.get(previous)
        byte=previousDict
        result.append(previousDict)

        for current in encoded[1:]:
            previousDict=b""
            if current not in dictionary:
                previousDict=dictionary.get(previous)
                previousDict+=byte
            else:
                previousDict=dictionary.get(current)
            result.append(previousDict)
            byte=b""
            byte+=bytes([previousDict[0]])
            dictionary[code]=dictionary.get(previous)+byte
            code=code+1
            previous=current

        return result

def getEntropy(file):
    with open(file,"rb") as f:
        chars={}
        counter=0
        byte=f.read(1)
        while byte:
            if chars.get(byte) is None:
                chars[byte]=1
            else:
                chars[byte] +=1
            counter=counter+1
            byte=f.read(1)

        entropy=0
        for c in list(chars.values()):
            entropy=entropy+c*(-log2(c))
        entropy=entropy/counter
        return entropy+log2(counter)
def main():

    if len(sys.argv) < 5:
        sys.exit("python lzw.py <encode|decode> <delta|gamma|omega|fibonacci> <input> <output>")

    mode = sys.argv[1]
    coding=sys.argv[2]
    inputFile = sys.argv[3]
    outputFile = sys.argv[4]
    lzw = LZWAlgorithm()
    if mode == "encode":
        result=lzw.encode(inputFile)
        codingResult=[x+1 for x in result]
        with open(outputFile,"w") as out:
            for item in codingResult:
                out.write(str(item))
                out.write(" ")

        entropy=getEntropy(inputFile)
        print("Entropia: ",entropy)
    elif mode=="decode":
        with open(inputFile,"r") as inp:
            for line in inp:
                data=line.split()
        numbers=[int(x)-1 for x in data]
        result=lzw.decode(numbers)
        with open(outputFile,"wb+") as out:
            for item in result:
                out.write(item)
    else:
        print("Unsupported option, please choose one from list down below: ")
        print("encode")
        print("decode")




if __name__ == "__main__":
    main()
