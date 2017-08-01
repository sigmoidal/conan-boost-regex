from conans import ConanFile, tools, os

class BoostRegexConan(ConanFile):
    name = "Boost.Regex"
    version = "1.64.0"
    generators = "txt"
    url = "https://github.com/boostorg/regex"
    description = "For a description of this library, please visit http://boost.org/regex "
    license = "www.boost.org/users/license.html"
    lib_short_name = "regex"

    def source(self):
        self.run("git clone --depth=50 --branch=boost-{0} {1}.git"
                 .format(self.version, self.url))

    def package(self):
        include_dir = src=os.path.join(os.getcwd(), self.lib_short_name, "include")
        self.copy(pattern="*", dst="", src=include_dir)
