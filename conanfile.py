from conans import ConanFile, tools, os

class BoostRegexConan(ConanFile):
    name = "Boost.Regex"
    version = "1.64.0"
    generators = "boost"
    settings = "os", "arch", "compiler", "build_type"
    url = "https://github.com/bincrafters/conan-boost-regex"
    source_url = "https://github.com/boostorg/regex"
    description = "Please visit http://www.boost.org/doc/libs/1_64_0/libs/libraries.htm"
    license = "www.boost.org/users/license.html"
    lib_short_name = "regex"
    build_requires = "Boost.Generator/0.0.1@bincrafters/testing"
    requires =  "Boost.Assert/1.64.0@bincrafters/testing", \
                      "Boost.Concept_Check/1.64.0@bincrafters/testing", \
                      "Boost.Config/1.64.0@bincrafters/testing", \
                      "Boost.Core/1.64.0@bincrafters/testing", \
                      "Boost.Functional/1.64.0@bincrafters/testing", \
                      "Boost.Integer/1.64.0@bincrafters/testing", \
                      "Boost.Iterator/1.64.0@bincrafters/testing", \
                      "Boost.Mpl/1.64.0@bincrafters/testing", \
                      "Boost.Predef/1.64.0@bincrafters/testing", \
                      "Boost.Smart_Ptr/1.64.0@bincrafters/testing", \
                      "Boost.Static_Assert/1.64.0@bincrafters/testing", \
                      "Boost.Throw_Exception/1.64.0@bincrafters/testing",\
                      "Boost.Type_Traits/1.64.0@bincrafters/testing"

                      #assert1 concept_check5 config0 core2 functional5 integer3 iterator5 mpl5 predef0 smart_ptr4 static_assert1 throw_exception2 type_traits3

    def source(self):
        self.run("git clone --depth=50 --branch=boost-{0} {1}.git"
                 .format(self.version, self.source_url))

    def build(self):
        boost_build = self.deps_cpp_info["Boost.Build"]
        b2_bin_name = "b2.exe" if self.settings.os == "Windows" else "b2"
        b2_bin_dir_name = boost_build.bindirs[0]
        b2_full_path = os.path.join(boost_build.rootpath, b2_bin_dir_name, b2_bin_name)

        toolsets = {
          'gcc': 'gcc',
          'Visual Studio': 'msvc',
          'clang': 'clang',
          'apple-clang': 'darwin'}

        b2_toolset = toolsets[str(self.settings.compiler)]

        self.run(b2_full_path + " -j4 -a --hash=yes toolset=" + b2_toolset)

    def package(self):
        include_dir = os.path.join(self.build_folder, self.lib_short_name, "include")
        self.copy(pattern="*", dst="include", src=include_dir)
        lib_dir = os.path.join(self.build_folder, "stage/lib")
        self.copy(pattern="*", dst="lib", src=lib_dir)

    def package_info(self):
        self.cpp_info.libs = self.collect_libs()
