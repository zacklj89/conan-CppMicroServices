cmake_minimum_required( VERSION  3.0 )

project( CppMicroServicesConanTestPackage
         VERSION       0.0.1
         LANGUAGES     C  CXX
)

# set c++ std version
set( CMAKE_CXX_STANDARD  14 )
# don't fail if c++14 is not available
set( CMAKE_CXX_STANDARD_REQUIRED  OFF )
# disable compiler-specific extensions
set( CMAKE_CXX_EXTENSIONS  OFF )

include( "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake" )
conan_basic_setup( TARGETS KEEP_RPATHS)
# supress cmake warnings about unused variables that conan passes in
set( _ignore_me  ${CONAN_EXPORTED} )

add_executable( CppMicroServicesConanTestPackage
    main.cpp
)
target_link_libraries( CppMicroServicesConanTestPackage
    PRIVATE  CONAN_PKG::CppMicroServices
)
