from subprocess import call
import os, sys

# python build_all.py > build_all.log
#
# MSVC++ 4.x  _MSC_VER == 1000
# MSVC++ 5.0  _MSC_VER == 1100
# MSVC++ 6.0  _MSC_VER == 1200
# MSVC++ 7.0  _MSC_VER == 1300
# MSVC++ 7.1  _MSC_VER == 1310 (Visual Studio 2003)
# MSVC++ 8.0  _MSC_VER == 1400 (Visual Studio 2005)
# MSVC++ 9.0  _MSC_VER == 1500 (Visual Studio 2008)
# MSVC++ 10.0 _MSC_VER == 1600 (Visual Studio 2010)
# MSVC++ 11.0 _MSC_VER == 1700 (Visual Studio 2012)
# MSVC++ 12.0 _MSC_VER == 1800 (Visual Studio 2013)
# MSVC++ 14.0 _MSC_VER == 1900 (Visual Studio 2015)
# MSVC++ 14.1 _MSC_VER >= 1910 (Visual Studio 2017)
#  

def usage():
    print("Usage: %s [win | linux | macosx]" % sys.argv[0]) 
    
def main(target_os):
    name = "Boost.Regex"
    version = "1.65.1"
    channel = "bincrafters/testing"
    archs = [ "x86", "x86_64" ]
    build_types = [ "Release", "Debug" ]
    shared = [ True, False ]
    compiler_versions = [ "15", "14" ]
    
    if target_os == 'win':
        # process arguments
        for arch in archs:
            for compiler_version in compiler_versions:
                for build_type in build_types:
                    for link in shared:
                        cmd = 'conan create {channel} -k \
                               -s arch={arch} \
                               -s build_type={build_type} \
                               -s compiler.version={compiler} \
                               -o {name}:shared={link} \
                               -o icu:shared={link} \
                               -o {name}:use_icu=True > {name}-{version}-{arch}-{build_type}-{link_str}-{used_compiler}.log'.format(name=name,
                                                                                                                                    version=version,
                                                                                                                                    channel=channel, 
                                                                                                                                    arch=arch, 
                                                                                                                                    compiler=compiler_version,
                                                                                                                                    used_compiler="vs2017" if compiler_version == "15" else "vs2015",
                                                                                                                                    build_type=build_type,
                                                                                                                                    link=str(link),
                                                                                                                                    link_str='shared' if link else 'static')
                        print("[{os}] {cmdstr}".format(os=target_os, cmdstr=" ".join(cmd.split())))
                        os.system( cmd )
                            
    elif target_os == 'macosx':
    
        #compiler_versions = [ "3.7", "3.8", "3.9", "4.0" ]
        #compiler_versions = [ "4.0" ]
    
        compiler = "apple-clang"
        compiler_versions = [ "9.0" ]
    
        # process arguments
        for arch in archs:
            for compiler_version in compiler_versions:
                for build_type in build_types:
                    for link in shared:
                        cmd = 'conan create {channel} -k \
                               -s arch={arch} \
                               -s build_type={build_type} \
                               -s compiler={compiler} \
                               -s compiler.version={compiler_v} \
                               -o {name}:use_icu=True \
                               -o {name}:shared={link} \
                               -o icu:shared={link} 2>&1 | tee {name}-{version}-{arch}-{build_type}-{link_str}-{used_compiler}.log'.format(name=name,
                                                                                                                                           version=version,
                                                                                                                                           channel=channel, 
                                                                                                                                           arch=arch, 
                                                                                                                                           compiler=compiler,
                                                                                                                                           compiler_v=compiler_version,
                                                                                                                                           used_compiler=compiler + '-' + compiler_version,
                                                                                                                                           build_type=build_type,
                                                                                                                                           link=str(link),
                                                                                                                                           link_str='shared' if link else 'static')
                        print("[{os}] {cmdstr}".format(os=target_os, cmdstr=" ".join(cmd.split())))
                        os.system( cmd )
    else:
        usage()
        exit(1)
        
    os.system("conan search {name}/{version}@{channel} --table=file.html".format(name=name, version=version, channel=channel) )


if len(sys.argv) < 2:
    usage()
    exit(1)

target_os=sys.argv[1]

if target_os == 'win' or target_os == 'linux' or target_os == 'macosx':
    main(target_os)
else:
    usage()
    
