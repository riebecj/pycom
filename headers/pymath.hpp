#include <cmath>

long long int factorial(int n){
    int n;
    long long int factorial = 1.0;

    for(int i = 1; i <= n; ++i) {
        factorial *= i;
    }
    
    return factorial;
}