#include <boost/regex.hpp>
#include <string>
#include <iostream>

int main() {
    const std::string s = "Boost Libraries";
    boost::regex expr("\\w+\\s\\w+");
    return !boost::regex_match(s, expr);
}
