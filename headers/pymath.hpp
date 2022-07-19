#include <cmath>

class Math{
    public:
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
};