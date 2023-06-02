#ifndef GRADIENTDESCENT_H
#define GRADIENTDESCENT_H

#include <vector>
#include <string>

class GradientDescent {
public:
  void generateData(std::string filename);
  void displayData();
  void batchTrain(float* m, float* b, float learningRate);
  
private:
  void gradientDescent(float* m, float* b, float learningRate);
  std::vector<std::vector<float>> points;
};
#endif
