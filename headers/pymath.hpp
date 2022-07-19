#include <cmath>

class Math{
    public:
        long double e = 2.718281828459045;
        long double pi = 3.141592653589793;

        long long int factorial(int n){
            long long int f = 1.0;

            for(int i = 1; i <= n; ++i) {
                f *= i;
            }

            return f;
        }

        long double sqrt(long double root){
            return sqrtf128(root);
        }

        long double exp(long double x){
            return pow(e, x);

        } long double exp(long long int x){
            return pow(e, x);
        }
};