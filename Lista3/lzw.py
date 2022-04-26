import sys
import time


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
        output = []

        dictionary = {}
        for i in range(0, 256):
            dictionary[i] = bytes([i])

        # next codeword to be inserted into the `_dict` will get this index
        new_codeword_index = 256
        # first number
        prev = encoded[0]
        prev_value = dictionary.get(prev)
        single = prev_value
        output.append(prev_value)

        for curr in encoded[1:]:
            prev_value = b""
            if curr not in dictionary:
                prev_value = dictionary.get(prev)
                prev_value += single
            else:
                prev_value = dictionary.get(curr)
            output.append(prev_value)
            single = b""
            single += bytes([prev_value[0]])
            dictionary[new_codeword_index] = dictionary.get(prev) + single
            new_codeword_index += 1
            prev = curr

        return output
        

class IO:
    pass


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
