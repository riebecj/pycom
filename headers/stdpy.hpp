#include <iostream>

typedef boost::multiprecision::cpp_int bigint;

void print(std::string str){
    std::cout << str << char(10);
}
void print(int istr){
    std::cout << istr << char(10);
}
void print(float fstr){
    std::cout << fstr << char(10);
}
void print(long long int llistr){
    std::cout << llistr << char(10);
}

void print(long double ldstr){
    std::cout << ldstr << char(10);
}

void print(bigint bigintstr){
    std::cout << bigintstr << char(10);
}
bigint len(std::string str){
    return str.length();
}
bigint len(std::vector<bigint> container){
    return container.size();
}
bigint len(std::vector<std::string> container){
    return container.size();
}
bigint len(std::vector<float> container){
    return container.size();
}
std::string input(std::string prompt){
    std::cout << prompt; std::string x; std::cin >> x; return x;
}

std::string lower(std::string str){
    std::string result = ""; 
    for (auto &ch: str){
        int asciiofch = int(ch);
        if (asciiofch >= 65 && asciiofch <= 91){
            result = result + char(asciiofch + 32);
        } else {
            result = result + ch;
        }
    }
    return result;
}

std::string upper(std::string str){
    std::string result = ""; 
    for (auto &ch: str){
        int asciiofch = int(ch);
        if (asciiofch >= 97 && asciiofch <= 124){
            result = result + char(asciiofch - 32);
        } else {
            result = result + ch;
        }
    }
    return result;
}