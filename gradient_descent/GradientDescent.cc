#include "GradientDescent.h"
#include <iostream>
#include <fstream>
#include <ostream>
#include <string>

void GradientDescent::generateData(std::string fileName) {
  std::ifstream file(fileName);
  std::string line;
  while (std::getline(file, line)) {
    std::vector<float> temp;
    std::string yString = line.substr(0, line.find(','));
    std::string xString = line.substr(line.find(',') + 1);
    temp.push_back(std::stof(yString));
    temp.push_back(std::stof(xString));
    points.push_back(temp);
  }
  file.close();
}

void GradientDescent::displayData() {
  for (const auto& point : points) {
    std::cout<<"y-axis" << point[0] << std::endl;
    std::cout<<"x-axis" << point[1] << std::endl;
    std::cout<<std::endl;
  }
}

void GradientDescent::gradientDescent(float* m, float* b, float learningRate) {
  float gradM = 0;
  float gradB = 0;
  for (const auto& point : points) {
    float x = point[0];
    float y = point[1];
    gradM += -(x * (y - ((*m * x) + *b)));
    gradB += -(y - ((*m * x) + *b));
  }
  float n = static_cast<float>(points.size());
  gradM = gradM * (2.0 / n);
  gradB = gradB * (2.0 / n);
  *m = *m - (gradM * learningRate);
  *b = *b - (gradB * learningRate);
}

void GradientDescent::batchTrain(float* m, float* b, float learningRate) {
  float rM = 0;
  float rB = 0;
  int iterations = 10000;
  for (int i = 0; i < iterations; ++i)
    gradientDescent(&rM, &rB, learningRate);
  *m = rM;
  *b = rB;
}
