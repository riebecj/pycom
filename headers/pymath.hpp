#include <cmath>
#include <boost/multiprecision/cpp_int.hpp>

class Math{
    public:
        long double e = 2.718281828459045;
        long double pi = 3.141592653589793;

        boost::multiprecision::cpp_int factorial(int n){
            boost::multiprecision::cpp_int f = 1;

            for(int i = 1; i <= n; ++i) {
                f *= i;
            }

            return f;
        }

        int factorial(short n){
            int f = 1;

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

        int floor(long double x){
            return floorf128(x);
        }

        int ceil(long double x){
            return ceilf128(x);
        }
};