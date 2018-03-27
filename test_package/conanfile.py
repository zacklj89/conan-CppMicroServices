from conans import ConanFile, CMake
import os

class CppMicroServicesConanTestPackage(ConanFile):
    settings =  {
                    'os': None,
                    'compiler': None,
                    'arch': None,
                    'build_type': ['Release', 'Debug']
                }
    generators = 'cmake'
    build_policy = 'missing'

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()

    def imports(self):
        self.copy(pattern='*', dst='bin', src='bin')
        self.copy(pattern='*', dst='lib', src='lib')
        self.copy(pattern='*.dylib', dst='bin', src='lib')

    def test(self):
        self.run(os.sep.join(['.', 'bin', 'CppMicroServicesConanTestPackage']))
