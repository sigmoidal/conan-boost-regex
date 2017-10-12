from conans import ConanFile, tools, os


class BoostRegexConan(ConanFile):
    name = "Boost.Regex"
    version = "1.65.1"
    generators = "boost"
    settings = "os", "arch", "compiler", "build_type"
    short_paths = True
    url = "https://github.com/bincrafters/conan-boost-regex"
    description = "Please visit http://www.boost.org/doc/libs/1_65_1/libs/libraries.htm"
    license = "www.boost.org/users/license.html"
    lib_short_names = ["regex"]
    options = {"shared": [True, False], "use_icu": [True, False]}
    default_options = "shared=False", "use_icu=False"
    build_requires = "Boost.Generator/1.65.1@bincrafters/testing"
    requires =  "Boost.Assert/1.65.1@bincrafters/testing", \
                      "Boost.Concept_Check/1.65.1@bincrafters/testing", \
                      "Boost.Config/1.65.1@bincrafters/testing", \
                      "Boost.Core/1.65.1@bincrafters/testing", \
                      "Boost.Functional/1.65.1@bincrafters/testing", \
                      "Boost.Integer/1.65.1@bincrafters/testing", \
                      "Boost.Iterator/1.65.1@bincrafters/testing", \
                      "Boost.Mpl/1.65.1@bincrafters/testing", \
                      "Boost.Predef/1.65.1@bincrafters/testing", \
                      "Boost.Smart_Ptr/1.65.1@bincrafters/testing", \
                      "Boost.Static_Assert/1.65.1@bincrafters/testing", \
                      "Boost.Throw_Exception/1.65.1@bincrafters/testing",\
                      "Boost.Type_Traits/1.65.1@bincrafters/testing"    

                      #assert1 concept_check5 config0 core2 functional5 integer3 iterator5 mpl5 predef0 smart_ptr4 static_assert1 throw_exception2 type_traits3
                      
    def requirements(self):
        if self.options.use_icu:
            self.requires("icu/59.1@bincrafters/testing")
            
    def source(self):
        boostorg_github = "https://github.com/boostorg"
        archive_name = "boost-" + self.version
        for lib_short_name in self.lib_short_names:
            tools.get("{0}/{1}/archive/{2}.tar.gz"
                .format(boostorg_github, lib_short_name, archive_name))
            os.rename(lib_short_name + "-" + archive_name, lib_short_name)
            
        if self.options.use_icu:
            # we need to patch the Jamfile.v2 of Boost.Regex (has_icu_test) when building static on windows 
            #if not self.options.shared and self.settings.os == 'Windows':
            tools.download(r'https://raw.githubusercontent.com/sigmoidal/conan-boost-regex/testing/1.65.1/patch/Jamfile.v2.patch', 'Jamfile.v2.patch');
             
            src_path = os.path.join(self.conanfile_directory, 'regex')
            jamfile_to_patch = os.path.join(src_path, 'build', 'Jamfile.v2')
            self.output.info("Patching: " + jamfile_to_patch)
            #self.output.info("cur: " + os.path.join(os.getcwd(), 'regex', 'build'))
            
            # to apply in subfolder
            tools.patch(base_path=os.path.join('regex', 'build'), patch_file="Jamfile.v2.patch") 
            exit
            
    def build(self):
        if self.options.use_icu:
            os.environ["ICU_PATH"] = self.deps_cpp_info["icu"].rootpath
            self.output.info("Using ICU_PATH: " + os.environ["ICU_PATH"])
            
        self.run(self.deps_user_info['Boost.Generator'].b2_command)

    def package(self):
        self.copy(pattern="*", dst="lib", src="stage/lib")
        for lib_short_name in self.lib_short_names:
            include_dir = os.path.join(lib_short_name, "include")
            self.copy(pattern="*", dst="include", src=include_dir)

    def package_info(self):
        self.user_info.lib_short_names = ",".join(self.lib_short_names)
        self.cpp_info.libs = tools.collect_libs(self)
        self.cpp_info.defines.append("BOOST_ALL_NO_LIB=1")

        self.env_info.PATH.append(os.path.join(self.package_folder, 'lib'))