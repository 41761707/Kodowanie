'''Radosław Wojtczak, JPEG-ls (bezstratny)
    Skróty kierunków geograficznych tradycyjne
      NW |  N
      -------
       W |  X
    7 schematów predykcji:
    1. X=W
    2. X=N
    3. X=NW
    4. X=N+W-NW
    5. X=N+(W-NW)
    6. X=W+((N-NW)/2)
    7. X=(N+W)/2
    8. Nowy standard

'''
import sys
import math

class Pixel:
    red = 0
    green = 0
    blue = 0
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
    def __repr__(self):
        return "({},{},{})".format(self.red, self.green, self.blue)
    def __str__(self):
        return "({},{},{})".format(self.red, self.green, self.blue)
    def __sub__(self, other):
        return Pixel((self.red-other.red) % 256, (self.green-other.green) % 256, (self.blue-other.blue) % 256)
    def __add__(self, other):
        return Pixel((self.red+other.red) % 256, (self.green+other.green) % 256, (self.blue+other.blue) % 256)
    def __floordiv__(self, other):
        return Pixel(self.red//other, self.green//other, self.blue//other)

def get_entropy(pixels, type):
    result = {}
    for i in range(256):
        result[i] = 0
    size = 0
    if type=='basic':
        for pixel in pixels:
            result[pixel.red] += 1
            result[pixel.green] += 1
            result[pixel.blue] += 1
            size += 3
    else:
        for pixel in pixels:
            result[getattr(pixel, type)] += 1
            size += 1
    entropy  =0
    '''
    for key,value in result.items():
        print(key,value)
    '''
    for item in result.values():
        if item==0:
            continue
        entropy = entropy+item * (-math.log2(item))
    entropy = entropy/size + math.log2(size)
    return entropy

def encode(pixels, image_width, image_height, mode):
    encoded = []
    for i in range(image_width):
        for j in range(image_height):
            if j==0:
                w = Pixel(0,0,0)
            else:
                w = pixels[image_width*i + (j-1)]
            if i==0:
                n = Pixel(0,0,0)
            else:
                n = pixels[image_width*(i-1) + j]
            if j==0 or i==0:
                nw = Pixel(0,0,0)
            else:
                nw = pixels[image_width*(i-1) + (j-1)]
            encoded.append(pixels[image_width*i + j] - predict_option(mode,w,n,nw))
        
    return encoded

def new_standard(w, n, nw):
    if nw >= max(w, n):
        return min(w, n)
    if nw <= min(w, n):
        return max(w, n)
    return w+n-nw



def predict_option(mode, w, n, nw):
    return {
        1: w,
        2: n,
        3: nw,
        4: n+w-nw,
        5: n+(w-nw),
        6: w + ((n-nw)//2),
        7: (n+w)//2,
        8: Pixel(new_standard(w.red, n.red, nw.red),
                new_standard(w.green, n.green, nw.green),
                new_standard(w.blue, n.blue, nw.blue),
                )
    }[mode]
            

def read_TGA(filename):
    with open(filename,"rb") as f:
        byte=f.read()
        data=[int(x) for x in byte]
        image_width = data[13]*256 + data[12]
        image_height = data[15]*256 + data[14]
        source = data[18:] 

        pixels_list=[]
        for i in range(image_height):
            for j in range(image_width):
                index = (image_width*i+j)*3
                pixels_list.append(Pixel
                                    (source[index],
                                    source[index+1],
                                    source[index+2])
                                    )
        return(pixels_list, image_width, image_height)
              

def main():
    predict={
        0:'basic',
        1:'W',
        2:'N',
        3:'NW',
        4:'N+W-NW',
        5:'N+(W-NW)',
        6:'W+(N-NW)/2',
        7:'(N+W)/2',
        8:'NewStandard'
    }
    if(len(sys.argv)<2):
        print("Usage: jpegls.py <plik_wejsciowy>")
        return
    file = sys.argv[1]
    pixels, image_width, image_height=read_TGA(file)
    types = ['basic','red','green','blue']
    modes = [1,2,3,4,5,6,7,8]
    outcome = []
    for x in types:
        print(x,(0,x,get_entropy(pixels, x)))
        for i in modes:
            outcome.append((i,x,get_entropy(encode(pixels, image_width, image_height, i), x)))

    for item in outcome:
            print(predict[item[0]],item[1],item[2])

    for x in types:
        temp = []
        for item in outcome:
            if item[1]==x:
                temp.append(item)
        print(min(temp, key = lambda t: t[2]))
        
    
    

if __name__=="__main__":
    main()