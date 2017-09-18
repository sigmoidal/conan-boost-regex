from conans import ConanFile, CMake, tools
import os


class BoostRegexTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    username = os.getenv("CONAN_USERNAME", "bincrafters")
    channel = os.getenv("CONAN_CHANNEL", "testing")
    requires = "Catch/1.9.6@uilianries/stable"

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()
        
    def imports(self):
        self.copy("*", dst="bin", src="lib")
        
    def test(self):
        cmake = CMake(self)
        cmake.test()