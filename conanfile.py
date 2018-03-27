import os, shutil, distutils
from conans import ConanFile, CMake, tools
from conans.tools import download, check_sha256, unzip

class CppMicroServicesConan(ConanFile):
    name = 'CppMicroServices'
    version = '3.3.0'
    description = 'C++ dynamic module system and service registry'
    url = 'https://github.com/CppMicroServices/CppMicroServices'
    license = 'https://github.com/CppMicroServices/CppMicroServices/blob/development/LICENSE'
    settings = 'os', 'compiler', 'arch', 'build_type'
    exports_sources = 'CMakeLists.txt', 'cmake*', 'include*', 'src*'
    generators = 'cmake'

    @property
    def _archive_dirname(self):
        return 'cpp-micro-services-{!s}'.format(self.version)

    def _get_build_dir(self):
        return os.getcwd()

## replace url and rename
    def source(self):
        download_url = 'https://github.com/CppMicroServices/CppMicroServices/archive/v{!s}.zip'.format(self.version)
        print('cpp-micro-services-{!s}.zip'.format(self.version) + ' is being used for download')
        download(download_url, 'cpp-micro-services-{!s}.zip'.format(self.version))
        check_sha256('cpp-micro-services-{!s}.zip'.format(self.version),'5f203a0bde3dc862b0506d2b4a8ff55693b1870e422c653eec0d61c7413d14b8')
        unzip('cpp-micro-services-{!s}.zip'.format(self.version))
        os.unlink('cpp-micro-services-{!s}.zip'.format(self.version))
        # distutils.dir_util.copy_tree('CppMicroServices-{!s}'.format(self.version), '.')
        # fileList = os.listdir('CppMicroServices-{!s}'.format(self.version))
        # fileList = ['CppMicroServices-{!s}/'.format(self.version)+filename for filename in fileList]
        # for f in fileList:
        #     shutil.copy2(f, '.')
        #shutil.copytree('CppMicroServices-{!s}'.format(self.version), '.')
        #shutil.rmtree('CppMicroServices-{!s}'.format(self.version))
        shutil.move('CppMicroServices-{!s}'.format(self.version), 'cppmicroservices')


    def build(self):
        #os.chdir('cppmicroservices')
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        cmake.test()

    def package(self):
        self.copy(pattern='*', dst='bin', src='bin', keep_path=False)
        self.copy(pattern='*', dst='lib', src='lib', keep_path=False)
        self.copy(pattern='*.h', dst='include', src='include')
        # TODO: remove once dependency libraries are available as conan packages
        self.copy(pattern='*.h', dst='include', src='vendor')
        self.copy(pattern='CMakeLists.txt', dst='.', src='.', keep_path=False)
        if self.settings.compiler == 'Visual Studio' and self.settings.build_type == 'Debug':
            self.copy(pattern='*.pdb', dst='bin', src='.', keep_path=False)

    # def package_id(self):
    #     #self.cpp_info.libs = [self.name]