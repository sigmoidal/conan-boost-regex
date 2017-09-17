#define CATCH_CONFIG_MAIN
#include "catch.hpp"
#include <boost/regex.hpp>

TEST_CASE( "Match the expression", "[regex]" ) {
    const std::string string = "Boost Libraries";

    boost::regex expression{"\\w+\\s\\w+"};
    REQUIRE(boost::regex_match(string, expression));

    boost::smatch what;
    REQUIRE(boost::regex_search(string, what, expression));
}

TEST_CASE( "Replace string", "[regex]") {
    std::string string = " Boost Libraries ";
    boost::regex expression{"\\s"};
    std::string fmt{"_"};
    const std::string result = boost::regex_replace(string, expression, fmt);
    REQUIRE(result == "_Boost_Libraries_");
}
