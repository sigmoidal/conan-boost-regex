from conans import ConanFile, tools, os


class BoostRegexConan(ConanFile):
    name = "Boost.Regex"
    version = "1.64.0"
    generators = "boost"
    settings = "os", "arch", "compiler", "build_type"
    short_paths = True
    url = "https://github.com/bincrafters/conan-boost-regex"
    description = "Please visit http://www.boost.org/doc/libs/1_64_0/libs/libraries.htm"
    license = "www.boost.org/users/license.html"
    lib_short_names = ["regex"]
    options = {"shared": [True, False], "use_icu": [True, False]}
    default_options = "shared=False", "use_icu=False"
    build_requires = "Boost.Generator/1.64.0@bincrafters/stable"
    requires =  "Boost.Assert/1.64.0@bincrafters/stable", \
                      "Boost.Concept_Check/1.64.0@bincrafters/stable", \
                      "Boost.Config/1.64.0@bincrafters/stable", \
                      "Boost.Core/1.64.0@bincrafters/stable", \
                      "Boost.Functional/1.64.0@bincrafters/stable", \
                      "Boost.Integer/1.64.0@bincrafters/stable", \
                      "Boost.Iterator/1.64.0@bincrafters/stable", \
                      "Boost.Mpl/1.64.0@bincrafters/stable", \
                      "Boost.Predef/1.64.0@bincrafters/stable", \
                      "Boost.Smart_Ptr/1.64.0@bincrafters/stable", \
                      "Boost.Static_Assert/1.64.0@bincrafters/stable", \
                      "Boost.Throw_Exception/1.64.0@bincrafters/stable",\
                      "Boost.Type_Traits/1.64.0@bincrafters/stable"    

                      #assert1 concept_check5 config0 core2 functional5 integer3 iterator5 mpl5 predef0 smart_ptr4 static_assert1 throw_exception2 type_traits3

    def requirements(self):
        if self.options.use_icu:
            self.requires("icu/59.1@bincrafters/stable")

    def source(self):
        boostorg_github = "https://github.com/boostorg"
        archive_name = "boost-" + self.version
        for lib_short_name in self.lib_short_names:
            tools.get("{0}/{1}/archive/{2}.tar.gz"
                .format(boostorg_github, lib_short_name, archive_name))
            os.rename(lib_short_name + "-" + archive_name, lib_short_name)

    def build(self):
        self.run(self.deps_user_info['Boost.Generator'].b2_command)

    def package(self):
        self.copy(pattern="*", dst="lib", src="stage/lib")
        for lib_short_name in self.lib_short_names:
            include_dir = os.path.join(lib_short_name, "include")
            self.copy(pattern="*", dst="include", src=include_dir)

    def package_info(self):
        self.user_info.lib_short_names = ",".join(self.lib_short_names)
        self.cpp_info.libs = tools.collect_libs(self)()
        self.cpp_info.defines.append("BOOST_ALL_NO_LIB=1")
