#include "iostream"
#include "stdio.h"
#include "fstream"

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
        } int system(std::string cmd){
            int code = std::system(cmd.c_str());
            return code;
        }

        void remove(const char * filename){
            int code = std::remove(filename);
            if(code != 0){throw std::runtime_error{filenotfound + std::string(filename) + " does not exist"}; exit(1);}
            
        } void remove(std::string filename){
            int code = std::remove(filename.c_str());
            if(code != 0){throw std::runtime_error{filenotfound + std::string(filename) + " does not exist"}; exit(1);}
            
        }

        void rename(const char * old, const char * _new){
            int code = std::rename(old, _new);
            if(code != 0){throw std::runtime_error{filenotfound + std::string(old) + " does not exist"};}
            
        } void rename(std::string old, const char * _new){
            int code = std::rename(old.c_str(), _new);
            if(code != 0){throw std::runtime_error{filenotfound + std::string(old) + " does not exist"};}
            
        } void rename(std::string old, std::string _new){
            int code = std::rename(old.c_str(), _new.c_str());
            if(code != 0){throw std::runtime_error{filenotfound + std::string(old) + " does not exist"};}
            
        } void rename(const char * old, std::string _new){
            int code = std::rename(old, _new.c_str());
            if(code != 0){throw std::runtime_error{filenotfound + std::string(old) + " does not exist"};}
        }

        
};