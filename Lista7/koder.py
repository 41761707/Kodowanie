import sys

def main():
    generating_matrix = [[1,1,0,1,0,0,0,1],[0,1,1,0,1,0,0,1],[0,0,1,1,0,1,0,1],[0,0,0,1,1,0,1,1]]
    filename = sys.argv[1]
    output=sys.argv[2]
    input = []
    result = []
    with open(filename,"rb+") as f:
        inp = f.read(1)
        while inp:
            inp=ord(inp)
            input.append(inp)
            inp=f.read(1)
    #print(input)
    for i in range(len(input)):
        indicator = 0b10000000
        bits = [0,0,0,0,0,0,0,0]
        first = [0,0,0,0,0,0,0,0]
        second = [0,0,0,0,0,0,0,0]
        for j in range(8):
            bits[j] = 1 if input[i] & indicator else 0
            indicator = indicator >> 1
            #print(bits[j])
        for j in range(8):
            first[j] = 0
            second[j] = 0
            for k in range(4):
                first[j] ^= (generating_matrix[k][j] & bits[k])
                second[j] ^= (generating_matrix[k][j] & bits[k+4])

        #print(first)
        #print(second)
        result.append(first[7] + first[6]*2 + first[5]*4 + first[4]*8 + first[3]*16 + first[2]*32 + first[1]*64 + first[0]*128)
        result.append(second[7] + second[6]*2 + second[5]*4 + second[4]*8 + second[3]*16 + second[2]*32 + second[1]*64 + second[0]*128)

    with open(output,"wb+") as out:
        for number in result:
            out.write(number.to_bytes(1, byteorder='big'))

if __name__=="__main__":
    main()