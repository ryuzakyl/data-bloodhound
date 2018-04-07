#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <math.h>
#include <string>
#include <algorithm>
#include <numeric>
#include <iterator>
#include <stdio.h>
#include <sys/types.h>
#include <complex>

using namespace std;

vector<double> presence(vector<double> vector_origin);

double dist_presence(vector<double> vector_incognita, vector<double> vector_origin);

double correlation(vector<double> vector_incognita, vector<double> vector_origin);

vector<vector<double>> Definition_Signature(vector<double> vector_origin);

vector<vector<vector<double>>> Extended_Signature(vector<double> vector_incognita, vector<double> vector_origin);

double dist_nominal(vector<double> vector_incognita, vector<double> vector_origin);

double dist_ordinal(vector<double> vector_incognita, vector<double> vector_origin);

double dnom_vec(vector<double> x, vector<double> y);

extern "C"
double dnom(double* x, double* y, int count);

double dord_vec(vector<double> x, vector<double> y);

extern "C"
double dord(double* x, double* y, int count);
