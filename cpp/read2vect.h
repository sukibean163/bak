#include <fstream>
#include <iostream>
#include <sstream>
#include <vector>

using namespace std;
template <class T = string> vector<vector<T>> read2vec(string strFileName) {

  std::ifstream file_data(strFileName);
  std::string strLine;
  T data;
  std::vector<T> lines;
  std::vector<vector<T>> result;
  result.clear();

  while (!file_data.eof()) {
    getline(file_data, strLine);
    stringstream stringin(strLine);
    lines.clear();
    while (stringin >> data) {
      lines.push_back(data);
    }
    if (lines.size() > 0) {
      result.push_back(lines);
    }
  }
  file_data.close();

  return result;
}
