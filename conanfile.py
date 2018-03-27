import os, shutil, distutils
from semver import SemVer
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

    @property
    def _major_version(self):
        return SemVer(self.version, loose=True).major

    @property
    def _is_dev(self):
        try:
            return self.develop
        except AttributeError:
            try:
                return self.scope.dev
            except AttributeError:
                return False

## replace url and rename
    def source(self):
        download_url = 'https://github.com/CppMicroServices/CppMicroServices/archive/v{!s}.zip'.format(self.version)
        print('cpp-micro-services-{!s}.zip'.format(self.version) + ' is being used for download')
        download(download_url, 'cpp-micro-services-{!s}.zip'.format(self.version))
        check_sha256('cpp-micro-services-{!s}.zip'.format(self.version),'5f203a0bde3dc862b0506d2b4a8ff55693b1870e422c653eec0d61c7413d14b8')
        unzip('cpp-micro-services-{!s}.zip'.format(self.version))
        os.unlink('cpp-micro-services-{!s}.zip'.format(self.version))
        shutil.move('CppMicroServices-{!s}'.format(self.version), 'cppmicroservices')


    def build(self):
        #os.chdir('cppmicroservices')
        cmake = CMake(self)
        cmake.configure(source_folder='cppmicroservices')
        cmake.build()

    def package(self):
        self.copy(pattern='*', dst='bin', src='bin', keep_path=False)
        self.copy(pattern='*', dst='lib', src='lib', keep_path=False)
        self.copy(pattern='*.h', dst='include', src='include', keep_path=True)
        self.copy(pattern='*.h', dst='include', src='framework/include', keep_path=True)
        self.copy(pattern='*.h', dst='include', src='cppmicroservices/framework/include', keep_path=True)
        self.copy(pattern='*.h', dst='include', src='httpservice/include', keep_path=True)
        self.copy(pattern='*.h', dst='include', src='cppmicroservices/httpservice/include', keep_path=True)
        self.copy(pattern='*.h', dst='include', src='shellservice/include', keep_path=True)
        self.copy(pattern='*.h', dst='include', src='cppmicroservices/shellservice/include', keep_path=True)
        self.copy(pattern='CMakeLists.txt', dst='.', src='.', keep_path=False)
        if self.settings.compiler == 'Visual Studio' and self.settings.build_type == 'Debug':
            self.copy(pattern='*.pdb', dst='bin', src='.', keep_path=False)

    def package_info(self):
        # let consuming projects know what library name is used for linking
        base_lib_name = '{!s}{!s}'.format(self.name, self._major_version)
        self.cpp_info.release.libs = [base_lib_name]
        self.cpp_info.debug.libs = [base_lib_name + 'd']