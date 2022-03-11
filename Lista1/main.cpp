#include <iostream>
#include <fstream>
#include <map>
#include <string>
#include <cmath>

double h1(int alphabet[256], int predecessor[256][256],int sum);

double entropia(int alphabet[256],int sum);

int main(int argc, char *argv[])
{
	int alphabet[256]={0};
	int predecessor[256][256]={0};
	std::string line;
	std::ifstream file(argv[1],std::ios::binary);
	int previousNumber=0;
	int sum=0;
	char byte;
	unsigned char prevByte = { 0 };


	if(file.is_open())
	{
		while(file.get(byte))
		{
			unsigned char ubyte = byte;

			// Wystąpienie symbolu
			alphabet[ubyte]++;

			// Wystąpienie symbolu po danym symbolu
			predecessor[prevByte][ubyte]++;
			prevByte = ubyte;

			sum++;
		}
		
	    int temp=0;
	    for(int i=0;i<256;i++)
	    {
	    	temp=temp+alphabet[i];
	    }
	    std::cout << "Częstości: " << temp << " ; Wszystkie znaki: " << sum << std::endl;
	    double entropiaValue=entropia(alphabet,sum);
		std::cout << "Entropia: " << entropiaValue << std::endl;
		double h=h1(alphabet,predecessor,sum);
		std::cout << "Entropia warunkowa: " << h << std::endl;
		std::cout << "Entropia - Entropia warunkowa: " << entropiaValue-h << std::endl;
		file.close();
	}
	else
	{
		std::cout << "uruchamianie: ./a.out <nazwa_pliku>.<rozszerzenie>" << std::endl;
	}

	return 0;
}

//H(Y|X)
double h1(int alphabet[256], int predecessor[256][256],int sum)
{
	if(sum==0)
	{
		return -1.0;
	}
	double result=0.0;
	for(int i=0;i<256;i++)
	{
		double innerResult=0.0;
		for(int j=0;j<256;j++)
		{
			if(alphabet[i]!=0 && predecessor[i][j]!=0)
			{
				double value=(predecessor[i][j]*1.0/alphabet[i]);
				innerResult=innerResult+(value)*(-1)*log2(value);
			}
		}
		result=result+(alphabet[i]*1.0/sum)*innerResult;
	}
	return result;
}

double entropia(int alphabet[256],int sum)
{
	if(sum==0)
	{
		return -1.0;
	}
	double result=0.0;
	for(int i=0;i<256;i++)
	{
		if(alphabet[i]!=0)
		{
			double value=(double)alphabet[i];
			result=result+(value)*log2(value);
		}
	}
	return log2(sum)-result/sum;
}