#include "cppmicroservices/FrameworkFactory.h"
#include "cppmicroservices/shellservice/ShellService.h"
#include "cppmicroservices/httpservice/HttpConstants.h"

#include <cstdlib>
#include <iostream>

using namespace cppmicroservices;

int main( int argc, char * argv[] )
{
    auto f = FrameworkFactory();
    std::cout << "Include didnt break things!!";
}
