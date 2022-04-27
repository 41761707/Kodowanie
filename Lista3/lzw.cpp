#include<iostream>
#include<map>
#include<vector>
#include<fstream>
#include<cmath>
#include<algorithm>
#include <unistd.h>
#include<typeinfo> //Testing

class EliasCodes
{
    public:
    std::vector<bool> gammaCoding(std::vector<int> &numbers); 
    std::vector<bool> deltaCoding(std::vector<int> &numbers);
    std::vector<bool> omegaCoding(std::vector<int> &numbers);
    std::vector<bool> fibonacciCoding(std::vector<int> &numbers);
    std::vector<int>  gammaDecoding(std::vector<bool>&result,int reminder);
    std::vector<int>  deltaDecoding(std::vector<bool>&result, int reminder);
    std::vector<int>  omegaDecoding(std::vector<bool>& result, int reminder);
    std::vector<int>  fibonacciDecoding(std::vector<bool>& result, int reminder);
};

std::string decToBin(int number)
{
    if(number==0) return "0";
    std::string result="";
    while(number>0)
    {
        result=result+std::to_string(number%2);
        number=number/2;
    }
    std::reverse(result.begin(),result.end());
    return result;
}

int binToDec(std::string text)
{
    int result=0;
    for(int i=0;i<text.size();i++)
    {
        result += (text[i] - '0') * (1 << (text.size() - 1 - i));
    }
    return result;
}

std::vector<bool> EliasCodes::gammaCoding(std::vector<int> &numbers)
{
    std::vector<bool>result{};
    for(int i=0;i<numbers.size();i++)
    {
        std::string current=decToBin(numbers[i]);
        for(int j=0;j<current.size()-1;j++)
        {
            result.push_back(0);
        }
        for(int j=0;j<current.size();j++)
        {
            result.push_back(current[j]-'0');
        }
    }
    return result;
}

std::vector<bool> EliasCodes::deltaCoding(std::vector<int> &numbers)
{
    std::vector<bool>result{};
    for(int i=0;i<numbers.size();i++)
    {
        std::string current=decToBin(numbers[i]);
        int n=current.size();
        std::string nString=decToBin(n);
        for(int j=0;j<nString.size();j++)
        {
            result.push_back(0);
        }
        for(int j=0;j<nString.size();j++)
        {
            result.push_back(nString[j]-'0');
        }
        for(int j=1;j<current.size();j++)
        {
            result.push_back(current[j]-'0');
        }
    }
    return result;
}

std::vector<int> EliasCodes::gammaDecoding(std::vector<bool>&result,int reminder)
{
    std::vector<int>numbers;
    int counter=0;
    for(int i=0;i<result.size()-(9-reminder);i++)
    {
        if(result[i]==0)
        {
            counter=counter+1;
        }
        else
        {
            counter=counter+1;
            std::string digit="";
            while(counter>0)
            {
                digit.append(std::to_string(result[i]));
                i++;
                counter--;
            }
            i--;
            numbers.push_back(binToDec(digit));
        }

    }
    return numbers;
}

std::vector<int> EliasCodes::deltaDecoding(std::vector<bool>& result, int reminder)
{
    std::vector<int> numbers;
    int counter = 0;
    for (int i = 0; i < result.size() - (9 - reminder); i++)
    {
        if (result[i] == 0)
            counter++;
        else
        {
            if (counter == 0)
                numbers.push_back(1);
            else 
            {
                std::string temp = "";
                while (counter > 0)
                {
                    temp.append(std::to_string(result[i]));
                    i++;
                    counter--;
                }
                int n = binToDec(temp);
                std::string res = "1";
                for (int j = 1; j < n; j++)
                {
                    res.append(std::to_string(result[i]));
                    i++;
                }
                i--;
                numbers.push_back(binToDec(res));
            }
        }
    }
    return numbers;
}
std::vector<bool> EliasCodes::omegaCoding(std::vector<int>& numbers)
{
    std::vector<bool> result{};
    for (int i = 0; i < numbers.size(); i++)
    {
        std::string outcome = "0";
        std::string temp="";
        int number = numbers[i];
        while (number > 1)
        {
            temp = decToBin(number);
            outcome = temp + outcome;
            number = temp.size() - 1;
        }
        for (int j = 0; j < outcome.size(); j++)
        {
            result.push_back(outcome[j] - '0');
        }
    }
    return result; 
}

std::vector<int> EliasCodes::omegaDecoding(std::vector<bool>& result, int reminder)
{
    std::vector<int> numbers;
    for (int i = 0; i < result.size() - (9 - reminder); i++)
    {
        int res = 1;
        for (int j = i; j < result.size() - (9 - reminder); j++)
        {
            if (result[j] == 0)
                break;
            int temp = 0;
            for (int k = j; k < j+res+1; k++)
                temp += result[k] * (1 << (j+res - k));
            j = j+res;
            i = j+1;
            res = temp;
        }
        numbers.push_back(res);
    }
    return numbers;
}

std::vector<bool> EliasCodes::fibonacciCoding(std::vector<int>& numbers)
{
    std::vector<bool> result{};
    std::vector<int> fibb{1,2};
    std::vector<bool> tempRes{};
    for (int i = 0; i < numbers.size(); i++)
    {
        while (numbers[i] >= fibb[fibb.size() - 1])
            fibb.push_back(fibb[fibb.size() - 1] + fibb[fibb.size() - 2]);
        for (int j = 0; j < fibb.size(); j++)
        {
            if (numbers[i] < fibb[j])
                break;
            tempRes.push_back(0);
        }
        int temp = numbers[i];
        while (temp > 0)
        {
            for (int j = 0; j < fibb.size(); j++)
            {
                if (temp < fibb[j])
                {
                    temp -= fibb[j-1];
                    tempRes[j-1] = 1;
                    break;
                }
            }
        }
        tempRes.push_back(1);
        result.insert(result.end(), tempRes.begin(), tempRes.end());
        tempRes.clear();
    }
    return result; 
}

std::vector<int> EliasCodes::fibonacciDecoding(std::vector<bool>& result, int reminder)
{
    std::vector<int> numbers;
    std::vector<bool> tempRes{};
    std::vector<int> fibb{1,2};
    for (int i = 0; i < result.size() - 9 + reminder; i++){
        bool prev = 0;
        while ((prev && result[i]) == 0){
            prev = result[i];
            tempRes.push_back(prev);
            i++;
        }
        while (tempRes.size() > fibb.size())
            fibb.push_back(fibb[fibb.size() - 1] + fibb[fibb.size() - 2]);
        int val = 0;
        for (int j = 0; j < tempRes.size(); j++)
            val += tempRes[j] * fibb[j];
        numbers.push_back(val);
        tempRes.clear();
    }
    return numbers;
}

enum Option
{
    encode,
    decode,
    invalid
};

enum Coding
{
    gammaG,
    delta,
    omega,
    fibonacci,
    wrong
};

Option resolveOption(std::string input)
{
    if(input=="encode") return encode;
    if(input=="decode") return decode;
    return invalid;
}

Coding resolveCoding(std::string input)
{
    if(input=="gamma") return gammaG;
    if(input=="delta") return delta;
    if(input=="omega") return omega;
    if(input=="fibonacci") return fibonacci;
    return wrong;
}

int main(int argc, char* argv[])
{
    if(argc<5)
    {
        std::cout << "Usage: ./lista3 <option> <coding> <input_file> <output_file>\n";
    }
    std::ifstream file(argv[3],std::ios::binary);

    Option mode=resolveOption(argv[1]);
    Coding coding=resolveCoding(argv[2]);
    EliasCodes elias;
    std::string text;
    char byte;
    std::vector<bool> toFile{};
    std::vector<int>numbers;
    std::vector<int>encodedNumbers;
    char encoded = 0b00000000;
    char temp = 0b00000001;
    char reminder = 0b11111111;
    std::ofstream out;
    int8_t decodeReminder;
    unsigned char ubyte;
    int a;
    std::vector<bool> data{};
    out.open(argv[4], std::ios::out | std::ios::trunc | std::ios::binary);
    switch(mode)
    {
        case encode:
            switch(coding)
            {
                case gammaG:
                    while (file >> a)
                    {
                        numbers.push_back(a);
                    }
                    toFile=elias.gammaCoding(numbers);
                    /*for(int i=0;i<toFile.size();i++)
                    {
                        std::cout<<toFile[i];
                    }*/
                    reminder &=(toFile.size()%8)+1;
                    out.write(&reminder,1);
                    for(int i=0;i<toFile.size();i++)
                    {
                        if(toFile[i])
                        {
                            encoded |= (temp << 7-(i%8));
                        }
                        if((i+1)%8==0)
                        {
                            out.write(&encoded,1);
                            encoded=0b00000000;
                        }
                    }
                    if(reminder>0)
                    {
                        out.write(&encoded,1);
                    }
                break;
                case delta:
                    while (file >> a)
                    {
                        numbers.push_back(a);
                    }
                    toFile=elias.deltaCoding(numbers);
                    /*for(int i=0;i<toFile.size();i++)
                    {
                        std::cout<<toFile[i];
                    }*/
                    reminder &=(toFile.size()%8)+1;
                    out.write(&reminder,1);
                    for(int i=0;i<toFile.size();i++)
                    {
                        if(toFile[i])
                        {
                            encoded |= (temp << 7-(i%8));
                        }
                        if((i+1)%8==0)
                        {
                            out.write(&encoded,1);
                            encoded=0b00000000;
                        }
                    }
                    if(reminder>0)
                    {
                        out.write(&encoded,1);
                    }
                break;
                case omega:
                    while (file >> a)
                    {
                        numbers.push_back(a);
                    }
                    toFile=elias.omegaCoding(numbers);
                    /*for(int i=0;i<toFile.size();i++)
                    {
                        std::cout<<toFile[i];
                    }*/
                    reminder &=(toFile.size()%8)+1;
                    out.write(&reminder,1);
                    for(int i=0;i<toFile.size();i++)
                    {
                        if(toFile[i])
                        {
                            encoded |= (temp << 7-(i%8));
                        }
                        if((i+1)%8==0)
                        {
                            out.write(&encoded,1);
                            encoded=0b00000000;
                        }
                    }
                    if(reminder>0)
                    {
                        out.write(&encoded,1);
                    }
                break;
                case fibonacci:
                    while (file >> a)
                    {
                        numbers.push_back(a);
                    }
                    toFile=elias.fibonacciCoding(numbers);
                    /*for(int i=0;i<toFile.size();i++)
                    {
                        std::cout<<toFile[i];
                    }*/
                    reminder &=(toFile.size()%8)+1;
                    out.write(&reminder,1);
                    for(int i=0;i<toFile.size();i++)
                    {
                        if(toFile[i])
                        {
                            encoded |= (temp << 7-(i%8));
                        }
                        if((i+1)%8==0)
                        {
                            out.write(&encoded,1);
                            encoded=0b00000000;
                        }
                    }
                    if(reminder>0)
                    {
                        out.write(&encoded,1);
                    }
                break;
                default:
                    std::cout << "Unsupported coding, choose one from the list down below: \n";
                    std::cout << "gamma\n";
                    std::cout << "delta\n";
                    std::cout << "omega\n";
                    std::cout << "fibonacci\n";
            }
        break;

        case decode:
            switch(coding)
            {
                case gammaG:
                    while(file.get(byte))
                    {
                        ubyte=byte;
                        break;
                    }
                    while(file.get(byte))
                    {
                        for(int i=0;i<8;i++)
                        {
                            if((byte>>(7-i)) &0b1)
                            {
                                data.push_back(1);
                            }
                            else
                            {
                                data.push_back(0);
                            }
                        }
                    }
                    /*for(int i=0;i<data.size()-(9-int(ubyte));i++)
                    {
                        std::cout<<data[i];
                    }*/
                    numbers=elias.gammaDecoding(data,int(ubyte));
                    for(int i=0;i<numbers.size();i++)
                    {
                        out << numbers[i] << " ";
                    }
                break;
                case delta:
                    while(file.get(byte))
                    {
                        ubyte=byte;
                        break;
                    }
                    while(file.get(byte))
                    {
                        for(int i=0;i<8;i++)
                        {
                            if((byte>>(7-i)) &0b1)
                            {
                                data.push_back(1);
                            }
                            else
                            {
                                data.push_back(0);
                            }
                        }
                    }
                    /*for(int i=0;i<data.size()-(9-int(ubyte));i++)
                    {
                        std::cout<<data[i];
                    }*/
                    numbers=elias.deltaDecoding(data,int(ubyte));
                    for(int i=0;i<numbers.size();i++)
                    {
                        out << numbers[i] << " ";
                    }
                break;
                case omega:
                    while(file.get(byte))
                    {
                        ubyte=byte;
                        break;
                    }
                    while(file.get(byte))
                    {
                        for(int i=0;i<8;i++)
                        {
                            if((byte>>(7-i)) &0b1)
                            {
                                data.push_back(1);
                            }
                            else
                            {
                                data.push_back(0);
                            }
                        }
                    }
                    /*for(int i=0;i<data.size()-(9-int(ubyte));i++)
                    {
                        std::cout<<data[i];
                    }*/
                    numbers=elias.omegaDecoding(data,int(ubyte));
                    for(int i=0;i<numbers.size();i++)
                    {
                        out << numbers[i] << " ";
                    }
                break;
                case fibonacci:
                    while(file.get(byte))
                    {
                        ubyte=byte;
                        break;
                    }
                    while(file.get(byte))
                    {
                        for(int i=0;i<8;i++)
                        {
                            if((byte>>(7-i)) &0b1)
                            {
                                data.push_back(1);
                            }
                            else
                            {
                                data.push_back(0);
                            }
                        }
                    }
                    /*for(int i=0;i<data.size()-(9-int(ubyte));i++)
                    {
                        std::cout<<data[i];
                    }*/
                    numbers=elias.fibonacciDecoding(data,int(ubyte));
                    for(int i=0;i<numbers.size();i++)
                    {
                        out << numbers[i] << " ";
                    }
                break;
                default:
                    std::cout << "Unsupported coding, choose one from the list down below: \n";
                    std::cout << "gamma\n";
                    std::cout << "delta\n";
                    std::cout << "omega\n";
                    std::cout << "fibonacci\n";
            }
        break;
        default:
            std::cout << "Unsupported type, choose one from the list down below: \n";
            std::cout << "encode\n";
            std::cout << "decode\n";
    }
    out.close();
}