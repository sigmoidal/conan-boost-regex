from conans import ConanFile, CMake
import os

class BoostRegexTestConan(ConanFile):
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    username = os.getenv("CONAN_USERNAME", "bincrafters")
    channel = os.getenv("CONAN_CHANNEL", "testing")
    requires = "Catch/1.9.6@uilianries/stable", "Boost.Regex/1.64.0@%s/%s" % (username, channel)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()

    def imports(self):
        self.copy("*.so*", dst="bin", src="lib")
        self.copy("*.dll", dst="bin", src="bin")
        self.copy("*.dylib*", dst="bin", src="lib")

    def test(self):
        cmake = CMake(self)
        cmake.configure(source_dir=self.conanfile_directory, build_dir="./")
        cmake.build()
        cmake.test()
