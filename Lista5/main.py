import sys
import math
import time
from collections import Counter
#from sklearn.metrics import mean_squared_error


def read_TGA(filename):
    with open(filename,"rb") as f:
        byte=f.read()
        data=[int(x) for x in byte]
        image_width = data[13]*256 + data[12]
        image_height = data[15]*256 + data[14]
        header = byte[:18]
        source = data[18:18+(3*image_height*image_width)]
        footer = byte[18+(3*image_height*image_width):] 
        source.reverse() #Własność tych plików, bez reverse byłoby B G R
        pixels_list=[]
        for i in range(image_height):
            for j in range(image_width):
                index = (image_width*i+j)*3
                pixels_list.append((source[index],
                                    source[index+1],
                                    source[index+2])
                                    )
        return(header,footer,pixels_list, image_width, image_height)

def write_TGA(header,source_to_bytes,footer,filename):
    with open(filename,"wb") as out:
        out.write(header)
        out.write(source_to_bytes)
        out.write(footer)

def avg(pixels):
    size=len(pixels)
    average = [0,0,0]
    for item in pixels:
        for i in range(3):
            average[i] += item[i]/size
    return average

def distance_manhattan(source,variable):
    return sum(abs(sourceElement-variableElement) 
    for sourceElement, variableElement 
    in zip(source, variable))

def distance_euclid(source,variable):
    return sum((sourceElement-variableElement) ** 2
    for sourceElement, variableElement 
    in zip(source, variable))

def first_distortion(pixels,point,size):
    distance=0
    for list in pixels:
        distance=(distance+distance_euclid(list,point))/size

    return(distance)


def evaluate_distortion(pixels, point, size):
    distance = 0
    for i,list in enumerate(pixels):
        for element in list:
            distance = (distance + distance_euclid(point[i],element))/size
    return distance

def new_vector(vector,perturbation):
    #return [i * (1.0 + perturbation) for i in vector]
    for i in range(3):
        vector[i]=vector[i]+perturbation
        if vector[i] > 255:
            vector[i] = 255
        if vector[i] < 0:
            vector[i] = 0
    return vector

def divide(pixels,codebook,eps,distortion,size):
    divided_codebook=[]

    for element in codebook:
        c1 = new_vector(element[:], 0.001)
        divided_codebook.append(c1)
        c2 = new_vector(element[:], -0.001)
        divided_codebook.append(c2)
        #print("CODEBOOK: ",codebook)
        #print("DIVIDED: ",divided_codebook)
    codebook = divided_codebook
    current_distortion = 0
    limit = 1
    iter=0
    while iter < 10:
    #while abs(limit) > eps:
        centers=[ [] for _ in range(len(codebook)) ]
        for i,vertex in enumerate(pixels):
            min_distance=None
            min_point=0
            for j,point in enumerate(codebook):
                distance=distance_manhattan(point,vertex)
                if min_distance is None or distance < min_distance:
                    min_distance = distance
                    min_point = j
                centers[min_point].append(vertex)
        tmp_distortion = evaluate_distortion(centers, codebook, size)
        for i in range(len(centers)):
            if len(centers[i])==0:
                continue
            centers[i]=avg(centers[i])
            new_center=round_centers(centers[i])
            if new_center in codebook:
                continue
            codebook[i]=centers[i]
        previous_distortion=0
        if(current_distortion>0):
            previous_distortion = current_distortion
        else:
            previous_distortion = distortion
        current_distortion = tmp_distortion
        if current_distortion == 0:
            limit = 0.0
        else:
            limit = abs((current_distortion - previous_distortion) / current_distortion)
        limit = 0
        iter=iter+1
    return codebook,distortion

def LBG(pixels, iterations,eps):
    size=len(pixels)
    codebook = []
    codebook.append(avg(pixels))
    distortion = first_distortion(pixels, codebook[0], size)
    while(len(codebook)<iterations):
        codebook, distortion = divide(pixels,codebook,eps,distortion,size)
    return codebook

def round_centers(centers):
    for i in range(3):
        centers[i] = round(centers[i])
    return centers

def round_result(result):
    for list in result:
        for i in range(len(list)):
            list[i] = round(list[i])
    return result


def convert(pixels,result):
    source = []
    for pixel in pixels:
        distances = [distance_manhattan(item,pixel) for item in result]
        source.append(result[min(range(len(distances)), key=distances.__getitem__)])
    return source

def pixels_to_bytes(pixels):
    pixels.reverse()
    pixels_bytes = [] 
    for pixel in pixels:
        for color in reversed(pixel):
            pixels_bytes.append(color)

    return bytes(pixels_bytes)

def mse(original, new):
    return (1 / len(original)) * sum(
        [distance_euclid(original[i], new[i]) for i in range(len(original))]
    )


def snr(x, mserr):
    currentSum = 0
    for element in x:
        for pixel in element:
            currentSum += pixel
    snr = currentSum * currentSum
    snr = snr / (3*len(x))
    snr = snr / mserr
    return 10 * math.log10(snr)


def main():
    if(len(sys.argv)!=4):
        print("Usage: jpegls.py <plik_wejsciowy> <plik_wyjsciowy> <liczba_kolorow>")
        return
    file = sys.argv[1]
    out = sys.argv[2]
    iterations = int(sys.argv[3])
    eps = 0.001
    header,footer,pixels, image_width, image_height=read_TGA(file)
    result=LBG(pixels, 2 ** iterations, eps)
    result=round_result(result)
    source = convert(pixels,result)
    #mseLib = mean_squared_error(pixels,source)
    #print(mseLib)
    mserr = mse(pixels, source)
    snratio = snr(pixels, mserr)
    print("MSE:", mserr)
    print("SNR:", snratio)
    source_to_bytes = pixels_to_bytes(source)
    write_TGA(header,source_to_bytes,footer,out)
if __name__=='__main__':
    main()

