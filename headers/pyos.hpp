#include "iostream"
#include "stdio.h"

#if defined(_WIN32)
    #define PLATFORM_NAME "windows"
#elif defined(_WIN64)
    #define PLATFORM_NAME "windows"
#elif defined(__linux__)
    #define PLATFORM_NAME "linux"
#elif defined(__unix__) || !defined(__APPLE__) && defined(__MACH__)
    #include <sys/param.h>
    #if defined(BSD)
        #define PLATFORM_NAME "bsd"
    #endif
#elif defined(__hpux)
    #define PLATFORM_NAME "hp-ux"
#elif defined(_AIX)
    #define PLATFORM_NAME "aix"
#elif defined(__APPLE__) && defined(__MACH__)
    #include <TargetConditionals.h>
    #elif TARGET_OS_MAC == 1
        #define PLATFORM_NAME "osx" 
    #endif

class Os{
    private:
        const char *get_platform_name() {
            return (PLATFORM_NAME == NULL) ? "" : PLATFORM_NAME;
        }
        
        const char *platform = get_platform_name();

        std::string filenotfound = "pycom: FileNotFoundError: ";

    public:
        int system(const char * cmd){
            int code = std::system(cmd);
            return code;
        }

        int remove(const char * filename){
            int code = std::remove(filename);
            if(code != 0){throw std::runtime_error{filenotfound.c_str()}; exit(1);}
            return code;
        }

        int rename(const char * old, const char * _new){
            int code = std::rename(old, _new);
            if(code != 0){throw std::runtime_error{filenotfound.c_str()}; exit(1);}
            return code;
        }
};