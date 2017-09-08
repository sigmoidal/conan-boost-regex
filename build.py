from conan.packager import ConanMultiPackager
import platform


if __name__ == "__main__":
    builder = ConanMultiPackager(args="--build missing")
    builder.add_common_builds(shared_option_name="Boost.Regex:shared", pure_c=False)
    # XXX (uilianries): Only libstdc++11 is working for gcc>=5.4
    if platform.system() == "Linux":
        filtered_builds = []
        for settings, options, env_vars, build_requires in builder.builds:
            if settings["compiler.version"] < "5.4" or settings["compiler.libcxx"] == "libstdc++11":
                 filtered_builds.append([settings, options, env_vars, build_requires])
        builder.builds = filtered_builds
    builder.run()
