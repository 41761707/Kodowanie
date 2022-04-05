import sys
import math
import time


class Node:

    def __init__(self, parent, weight=0, left=None, right=None, symbol=''):
        self.parent = parent
        self.weight = weight
        self.left = left
        self.right = right
        self.symbol = symbol


class AdaptiveHuffman:

    def __init__(self):
        self.NYT = Node(None, 0, symbol='NYT')
        self.root = self.NYT
        self.visited = [None] * 256
        self.nodes = []

    def insert(self, symbol):
        curr = self.visited[ord(symbol)]

        if curr is None:
            nyt = self.NYT
            old_nyt_parent = nyt.parent

            new_parent = None

            if old_nyt_parent is None:
                self.root = Node(None, left=nyt, right=None)
                nyt.parent = self.root
                new_parent = self.root
            else:
                new_parent = Node(old_nyt_parent, weight=1,
                                  left=nyt, right=None)
                old_nyt_parent.left = new_parent
                nyt.parent = new_parent

            new_node = Node(new_parent, weight=1, symbol=symbol)
            new_parent.right = new_node

            self.nodes.append(new_node)
            self.nodes.append(new_parent)

            self.visited[ord(symbol)] = new_node

            curr = new_parent.parent

        while curr is not None:

            to_swap = None
            for n in self.nodes:
                if n.weight == curr.weight:
                    to_swap = n
                    break

            if curr is not to_swap and curr is not to_swap.parent and to_swap is not curr.parent:
                self.swap(curr, to_swap)

            curr.weight += 1
            curr = curr.parent

    def swap(self, one, two):
        one_index = self.nodes.index(one)
        two_index = self.nodes.index(two)

        self.nodes[one_index], self.nodes[
            two_index] = self.nodes[two_index], self.nodes[one_index]

        parent = one.parent
        one.parent = two.parent
        two.parent = parent

        if one.parent.left is two:
            one.parent.left = one
        else:
            one.parent.right = one

        if two.parent.left is one:
            two.parent.left = two
        else:
            two.parent.right = two

    def node_code(self, node):
        code = ''
        while node.parent is not None:
            p = node.parent
            if p.left is node:
                code += '0'
            else:
                code += '1'
            node = p
        return code[::-1]

    def encode(self, symbol):
        code =""
        if self.visited[ord(symbol)] is not None:
            node = self.visited[ord(symbol)]
            code= self.node_code(node)
        else:
            code= self.node_code(self.NYT) + bin(ord(symbol))[2:].zfill(8)
        self.insert(symbol)
        return code

    def decode(self, encoded):
        output = []
        first_char = chr(int(encoded[:8], 2))

        output.append(ord(first_char))

        self.insert(first_char)

        node = self.root
        i = 8
        while i < len(encoded):
            curr = encoded[i]

            if curr == '0':
                node = node.left
            else:
                node = node.right

            symbol = node.symbol

            if symbol:
                if symbol == 'NYT':
                    symbol = chr(int(encoded[i+1:i+9], 2))
                    i += 8
                output.append(ord(symbol))
                self.insert(symbol)
                node = self.root

            i += 1

        return output

    def get_avg_code_length(self):
        lengths = []
        count = 0

        for symbol in self.visited:
            if symbol is None:
                continue
            lengths.append(len(self.node_code(symbol)))
            count += 1

        return sum(lengths) / count

    def get_entropy(self):
        entropy = 0

        for symbol in self.visited:
            if symbol is None:
                continue
            entropy = entropy + symbol.weight * (-math.log2(symbol.weight))

        entropy = entropy/self.root.weight
        entropy=entropy+math.log2(self.root.weight)
        if(entropy<0):
            entropy=0
        return entropy


def main():

    if len(sys.argv) < 4:
        sys.exit("python AdaptiveHuffman.py <encode|decode> <input> <output>")

    mode = sys.argv[1]
    inputFile = sys.argv[2]
    outputFile = sys.argv[3]


    huffman = AdaptiveHuffman()
    start=time.time()
    if mode == "decode":
        data = ""
        with open(inputFile, "rb") as inp:
            byte = inp.read(1)
            padding = ord(byte)

            byte = inp.read(1)
            while byte:
                byte = ord(byte)
                for i in range(0, 8):
                    if (byte >> (7-i)) & 0b1:
                        data += '1'
                    else:
                        data += '0'
                byte = inp.read(1)
        if(padding!=0):
            data = data[:-padding]
        result = huffman.decode(data)
        with open(outputFile, "wb+") as out:
            for b in result:
                out.write(b.to_bytes(1, byteorder="big"))

    elif mode=="encode":
        result_temp=""
        counter=1
        with open(inputFile, "rb") as inp:
            byte = inp.read(1)
            while byte:
                result_temp += huffman.encode(byte)
                byte = inp.read(1)
                counter += 1
        result = []
        padding = 0
        for i in range(0, math.ceil(len(result_temp)/8)):
            temp = result_temp[(i*8):((i+1)*8)]
            if len(temp) != 8:
                padding = 8-len(temp)
                temp += "0" * padding
            temp = int(temp, 2)
            result.append(temp)
        result = [padding] + result
        with open(outputFile, "wb+") as out:
            for b in result:
                out.write(b.to_bytes(1, byteorder='big'))

        print("Średnia długość słowa kodowego:", huffman.get_avg_code_length())
        print("Współczynnik kompresji:", counter/len(result))
        print("Entropia:", huffman.get_entropy())
    else:
        pass
    print("Czas trwania: ",time.time()-start)




if __name__ == "__main__":
    main()