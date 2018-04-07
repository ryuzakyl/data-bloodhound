#ifndef __ALIGNMENT_H__
#define __ALIGNMENT_H__

// std includes
#include <vector>

extern "C"
void cow_align(double* v, int v_len, int* v_segments, int v_segs_len, double* ref, int ref_len, int* ref_segments, int ref_segs_len, int slack, double* result);

/// <summary>
/// Interpolation data for the COW method
/// </summary>
struct InterpData
{
	// the coefficients
	std::vector<std::vector<double> > coefficients;

	// the indexes
	std::vector<std::vector<double> > indexes;
};

/// <summary>
/// Performs alignment by means of Correlation Optimized Warping
/// </summary>
/// <param name="v">The vector to align by COW.</param>
/// <param name="v_segments">The points selected for alignment in the sample v</param>
/// <param name="ref">The reference sample to use as a pattern</param>
/// <param name="ref_segments">The points selected for alignment in the reference sample</param>
/// <param name="slack">Flexibility or tolerance</param>
/// <returns>The vector aligned by the COW method</returns>
/// <remarks>The slack describes how much the spectrum can move in each direction</remarks>
std::vector<double> cow(std::vector<double> v, std::vector<int> v_segments, std::vector<double> ref, std::vector<int> ref_segments, int slack);

/// <summary>
/// Computes interpolation coefficients and corresponding indexes
/// </summary>
/// <param name="n">The length of the segment</param>
/// <param name="slack_coeffs">Slack coefficients</param>
/// <param name="slack_idxs">Slack indexes</param>
/// <returns>The interpolation coefficients and corresponding indexes</returns>
/// <remarks>Taken from the old implementation</remarks>
InterpData compute_interpolation_coefficients(int n, std::vector<double> slack_coeffs, std::vector<double> slack_idxs);

/// <summary>
/// ???
/// </summary>
/// <param name="x">The x vector</param>
/// <param name="edges">The edges vector</param>
/// <param name="N">The first output vector</param>
/// <param name="p_bin">The second output vector</param>
/// <param name="stride">Stride along active dimension</param>
/// <param name="mx">Amount of elements in the active direction X</param>
/// <remarks>Taken from the old implementation</remarks>
void histogram_loop(std::vector<double> x, std::vector<double> edges, std::vector<double>& N, std::vector<double>& p_bin, int stride, int mx);

/// <summary>
/// Binary search over a vector
/// </summary>
/// <param name="v">The vector of interest</param>
/// <param name="x">The value to search for</param>
/// <returns>The index 'corresponding' to that value</returns>
/// <remarks>If x is out of bounds, then -1 is returned</remarks>
int find_bin(std::vector<double> v, double x);

/// <summary>
/// Cummulative sum at each position
/// </summary>
/// <param name="v">The vector of interest</param>
/// <returns>The projective integral for the specified vector</returns>
/// <remarks>The resulting vector has the same size</remarks>
/// <remarks>It's basically a projective integral</remarks>
std::vector<double> cumsum(std::vector<double> v);

/// <summary>
/// Derivative for 1-D discrete data
/// </summary>
/// <param name="v">The vector of interest</param>
/// <returns>The derivative of a vector v</returns>
/// <remarks>The resulting vector has 1 less component</remarks>
/// <remarks>The 'derivative' is computed by d[i] = v[i+1] - v[i]</remarks>
std::vector<double> diff(std::vector<double> v);

/// <summary>
/// Difference betwwen vectors
/// </summary>
/// <param name="x">The first vector</param>
/// <param name="y">The second vector</param>
/// <returns>The vector resulting from y - x</returns>
std::vector<double> vector_diff(std::vector<double> x, std::vector<double> y);

/// <summary>
/// Norm 2 of a vector
/// </summary>
/// <param name="v">The vector of interest</param>
/// <returns>The norm 2 of v</returns>
double norm2(std::vector<double> v);

/// <summary>
/// Quick 1-D linear interpolation
/// </summary>
/// <param name="x">A monotonically increasing vector</param>
/// <param name="y">A vector with the same size of x</param>
/// <param name="xi">The value to interpolate</param>
/// <returns>The value of the 1-D function Y at the points of column vector xi using linear interpolation</returns>
/// <remarks>interp1q from MATLAB will be removed in a future release. Use INTERP1 instead</remarks>
/// <remarks>returns NaN for any values of xi that lie outside the coordinates in x</remarks>
double interp1q(std::vector<double> x, std::vector<double> y, double xi);

/// <summary>
/// Gets the position in an sorted array where a value sould be
/// </summary>
int binary_search(std::vector<double> arr, double value);

#endif