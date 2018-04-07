// including standard math library
#include <math.h>
#include <limits>
#include <stdexcept>

// header include
#include "alignment.h"

extern "C"
void cow_align(double* v, int v_len, int* v_segments, int v_segs_len, double* ref, int ref_len, int* ref_segments, int ref_segs_len, int slack, double* result)
{
    std::vector<double> v_vector;
    v_vector.assign(v, v + v_len);

    std::vector<int> v_segments_vector;
    v_segments_vector.assign(v_segments, v_segments + v_segs_len);

    std::vector<double> ref_vector;
    ref_vector.assign(ref, ref + ref_len);

    std::vector<int> ref_segments_vector;
    ref_segments_vector.assign(ref_segments, ref_segments + ref_segs_len);

    std::vector<double> v_cow = cow(v_vector, v_segments_vector, ref_vector, ref_segments_vector, slack);

    for (size_t i = 0; i < v_cow.size(); i++)
        result[i] = v_cow[i];
}

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
std::vector<double> cow(std::vector<double> v, std::vector<int> v_segments, std::vector<double> ref, std::vector<int> ref_segments, int slack)
{
	// validating parameters (specific COW validation here)
	if (v.size() != ref.size())
		throw std::invalid_argument("The vector 'v' and the reference 'ref' must have the same size.");

	// validating the slack
	if (slack <= 1)
		throw std::invalid_argument("The slack must be greater than one.");

//	// there must be at least 2 segments (start and end)
//	if (ref_segments.size() < 2)
//		throw std::invalid_argument("There must be at least 2 segments (start and end).");

	// segment sizes must match
	if (v_segments.size() != ref_segments.size())
		throw std::invalid_argument("The same amount of points must be chosen for the reference and the sample.");

	// defining the final result
	int ref_length = (int)ref.size();
	std::vector<double> cow_aligned(ref_length);

	// auxiliar variables
	int seg_count;									// the amount of segments to analyze
	int ref_seg_count = (int)ref_segments.size();	// the amount of segments of the sample
	std::vector<int> seg1_lengths;					// the lengths of the segments belonging to the reference sample
	std::vector<int> seg2_lengths;					// the lengths of the segments belonging to the  sample to align

	#pragma region Building the segment length vectors
	// if the segments should be determined automatically
	if (ref_seg_count == 1)
	{
		// setting the segments sizes to process
		int seg_sizes = ref_segments[0];
		seg_count = (int)floor((double)((ref_length - 1) / (seg_sizes - 1)));

		// creating the segment lengths vectors
		seg1_lengths = std::vector<int>(seg_count);
		seg2_lengths = std::vector<int>(seg_count);

		// computing the length of the segments
		for (int i = 0; i < seg_count; i++)
			seg1_lengths[i] = seg2_lengths[i] = seg_sizes - 1;

		// correcting the size of the last segment
		int offset = (ref_length - 1) % (seg_sizes - 1);
		seg1_lengths[seg_count - 1] += offset;
		seg2_lengths[seg_count - 1] += offset;
	}
	else
	{
		// setting the amount of segments to process
		seg_count = v_segments.size() - 1;

		// creating the segment lengths vectors
		seg1_lengths = std::vector<int>(seg_count);
		seg2_lengths = std::vector<int>(seg_count);

		// computing the length of the segments
		for (int i = 0; i < seg_count; i++)
		{
			seg1_lengths[i] = ref_segments[i + 1] - ref_segments[i];
			seg2_lengths[i] = v_segments[i + 1] - v_segments[i];
		}
	}

	#pragma endregion

    #pragma region Computing slack indexes and coefficients
	// getting slack bounds
	int slack_lb = -slack;
	int slack_ub = slack;
	int slack_count = 2 * slack + 1;

	// declaring slacks coefficients and indexes
	std::vector<double> slack_idxs(slack_count);
	std::vector<double> slack_coefs1(slack_count);
	std::vector<double> slack_coefs2(slack_count);

	// computing slack indexes and coefficients
	for (double i = slack_lb; i <= slack_ub; i++)
	{
		// computing the index
		int idx = (int)(i - slack_lb);

		// setting the current slack index
		slack_idxs[idx] = i;

		// this vectors are required to compute the interpolation coefficients later
		slack_coefs1[idx] = i + seg2_lengths[0] + 1;				// i have my doubts on the expression (ask Diana or Noslen)
		slack_coefs2[idx] = i + seg2_lengths[seg_count - 1] + 1;	// i have my doubts on the expression (ask Diana or Noslen)
	}
	#pragma endregion

    #pragma region Computing interpolation coefficients and corresponding indexes
	// creating a vector for all the interpolation information
	std::vector<InterpData> interp_datas(seg_count);
	// if the segments should be determined automatically
	if (ref_seg_count == 1)
	{
        // computing interpolation data
		InterpData tmp_interp_data = compute_interpolation_coefficients(seg1_lengths[0] + 1, slack_coefs1, slack_idxs);

        // assigning interpolation data to each item in the vector (except the last one)
		for (int l = 0; l < seg_count - 1; l++)
			interp_datas[l] = tmp_interp_data;

		// setting the last one
		interp_datas[seg_count - 1] = compute_interpolation_coefficients((int)(seg1_lengths[seg_count - 1] + 1), slack_coefs2, slack_idxs);

	}
	else
	{
		// assigning interpolation data to each item in the vector
		for (int l = 0; l < seg_count; l++)
		{
			// computing a new vector of slack coefficients
			std::vector<double> slack_coefsB(slack_count);
			for (int s = 0; s < slack_count; s++)
				slack_coefsB[s] = slack_idxs[s] + seg2_lengths[l] + 1;

			// setting the computed coefficients
			interp_datas[l] = compute_interpolation_coefficients((int)(seg1_lengths[l] + 1), slack_coefsB, slack_idxs);
		}
	}
	#pragma endregion

    #pragma region Computing table index
	// computing the cumsum vector bt
	std::vector<double> bt_tmp(seg_count + 1);
	bt_tmp[0] = 1;
	std::copy(seg1_lengths.begin(), seg1_lengths.end(), bt_tmp.begin() + 1);
	std::vector<double> bt = cumsum(bt_tmp);

	// computing the cumsum vector bp
	std::vector<double> bp_tmp(seg_count + 1);
	bp_tmp[0] = 1;
	std::copy(seg2_lengths.begin(), seg2_lengths.end(), bp_tmp.begin() + 1);
	std::vector<double> bp = cumsum(bp_tmp);

	// computing the boundaries in the 'bounds' variable
	std::vector<std::vector<double> > bounds(2);
	bounds[0] = std::vector<double>(seg_count + 1);
	bounds[1] = std::vector<double>(seg_count + 1);

	// filling the boundaries
	int cn = seg_count;
	for (int bn = 0; bn < seg_count + 1; bn++)
	{
		// computing items for index bn
		bounds[0][bn] = std::max(bp[bn] - slack * bn, bp[bn] - slack * cn);
		bounds[1][bn] = std::min(bp[bn] + slack * bn, bp[bn] + slack * cn);

		// decrement cn
		cn--;
	}

	// actually computing the table index
	std::vector<double> bounds_diff = vector_diff(bounds[0], bounds[1]);
	std::vector<double> tbl_idx_tmp(seg_count + 2);
	tbl_idx_tmp[0] = 0;
	for (int g = 0; g < seg_count + 1; g++)
		tbl_idx_tmp[1 + g] = bounds_diff[g] + 1;

	// the cumulative sum of the vector difference between the bounds
	std::vector<double> table_index = cumsum(tbl_idx_tmp);
	#pragma endregion

	#pragma region Computing table
	// creating the table
	int table_cols = (int)(table_index[seg_count + 1]);	// last value of table_index
	std::vector<std::vector<double> > table(3, std::vector<double>(table_cols));

	// filling the table
	for (int seg_idx = 0; seg_idx < seg_count + 1; seg_idx++)
	{
		int v_size = (int)(bounds_diff[seg_idx] + 1);
		int v_value = (int)(bounds[0][seg_idx]);
		int idx = (int)(table_index[seg_idx]);

		// actually filling the table
		for (int iiv = 0; iiv < v_size; iiv++)
		{
			// setting the value in the table
			table[0][idx] = v_value;

			// incrementing values
			v_value++;
			idx++;
		}
	}
	#pragma endregion

	#pragma region Performing forward phase
	std::vector<std::vector<double> > bound_k_table(2);

	// computing the sample derivative
	std::vector<double> v_derivative = diff(v);

	// for each segment
	for (int seg_idx = 0; seg_idx < seg_count; seg_idx++)
	{
		// assigning b and c
		double b = (table_index[seg_idx] + 1) - bounds[0][seg_idx];
		double c = seg1_lengths[seg_idx] + 1;

		// assigning nodes
		double node_z = table_index[seg_idx + 2];
		double node_a = table_index[seg_idx + 1] + 1;
		int nodes_diff = (int)(node_z - node_a);

		// resetting the 'bound_k_table'
		bound_k_table[0] = std::vector<double>(nodes_diff + 1);
		bound_k_table[1] = std::vector<double>(nodes_diff + 1);

		// creating the t_seg array
		int bt_count = (int)(bt[seg_idx + 1] - bt[seg_idx] + 1);
		std::vector<double> t_seg(bt_count);

		// computing the mean of t_seg
		double t_seg_mean = 0.0;
		for (int seg_idx_new = 0, seg_idx_c = (int)bt[seg_idx] - 1; seg_idx_c < bt[seg_idx + 1]; seg_idx_new++, seg_idx_c++)
		{
			t_seg[seg_idx_new] = ref[seg_idx_c];
			t_seg_mean += t_seg[seg_idx_new];
		}
		t_seg_mean /= bt_count;

		// centering t_seg
		std::vector<double> t_seg_centered(bt_count);
		for (int k = 0; k < bt_count; k++)
			t_seg_centered[k] = t_seg[k] - t_seg_mean;

		// getting t_seg_centered norm
		double t_seg_norm = norm2(t_seg_centered);

		// looping over nodes
		int count = 0;
		for (int node_idx = (int)(node_a - 1); node_idx < node_z; node_idx++)
		{
			std::vector<double> prec_nodes(slack_count);
			std::vector<double> allowed_arcs(slack_count);
			double n_aa = 0.0;
			for (int nod = 0; nod < slack_count; nod++)
			{
				// computing the value of prec_nodes[nod]
				prec_nodes[nod] = table[0][node_idx] - (slack_idxs[nod] + seg2_lengths[seg_idx]);

				// setting allowed_arcs[nod] if in range
				if (prec_nodes[nod] >= bounds[0][seg_idx] && prec_nodes[nod] <= bounds[1][seg_idx])
					allowed_arcs[nod] = 1;

				// incrementing n_aa
				n_aa += allowed_arcs[nod];
			}

			// if there are allowed arcs marked
			if (n_aa >= 1)
			{
				int naa_idx = 0;
				int mov_na = 0;
				double f_cost = 0.0;

				// while 'mov_na' is smaller than 'n_aa'
				while (mov_na < n_aa)
				{
					double xi_seg_mean = 0.0;
					double xi_seg_meansqr = 0.0;
					double ccs_node = 0.0;

					// if 'naa_idx' is an allowed arc
					if (allowed_arcs[naa_idx] == 1)
					{
						// for each value of the segment with index 'seg_idx'
						int seg_idx_length = (int)(seg1_lengths[seg_idx] + 1);
						for (int nd_idx = 0; nd_idx < seg_idx_length; nd_idx++)
						{
							int index_node = (int)(table[0][node_idx] + (interp_datas[seg_idx].indexes[naa_idx][nd_idx] - seg2_lengths[seg_idx]));
							double b_coeff = interp_datas[seg_idx].coefficients[naa_idx][nd_idx];

							// getting the sample value for index 'index_node - 1' using interpolation
							double xi_seg = v[index_node - 1];
							double xi_diff = v_derivative[index_node - 1];
							xi_seg += b_coeff * xi_diff;

							// updating auxiliar parameters
							xi_seg_mean += xi_seg;
							xi_seg_meansqr += pow(xi_seg, 2.0);
							ccs_node += t_seg_centered[nd_idx] * xi_seg;
						}

						// computing final values of 'xi_seg_mean', 'xi_seg_meansqr' and 'ccs_node'
						xi_seg_mean /= seg_idx_length;													// mean of the interpolated segments
						xi_seg_meansqr = sqrt(xi_seg_meansqr - seg_idx_length * pow(xi_seg_mean, 2.0));
						ccs_node = ccs_node / (t_seg_norm * xi_seg_meansqr);

						// computing the 'pos'
						double nodes_table_ptr = b + prec_nodes[naa_idx];
						int pos = (int)(nodes_table_ptr - 1);

						// updating the 'bound_k_table' and 'f_cost'
						double f_cost_current = table[1][pos] + ccs_node;
						if (f_cost < f_cost_current)
						{
							f_cost = f_cost_current;
							bound_k_table[0][count] = f_cost;
							bound_k_table[1][count] = pos;
						}

						// incrementing 'mov_na'
						mov_na++;
					} // end of if 'allowed_arcs[naa_idx] == 1'

					// incrementing 'naa_idx'
					naa_idx++;
				} // end of while 'mov_na < n_aa'

			} // end of if of 'n_aa >= 1'

			// updating the table
			table[1][node_idx] = bound_k_table[0][count];
			table[2][node_idx] = bound_k_table[1][count];
			count++;
		} // end of for of 'node_idx'

	} // end of for of 'seg_idx'
	#pragma endregion

	#pragma region Prforming backward phase
	// declaring the warping vector
	std::vector<double> warping(seg_count + 1);
	warping[seg_count] = (int)v.size();

	// backtrace optimal boundaries using the pointers in table (comment taken from the old implementation)
	int ptr = table_cols - 1;
	for (int bound_idx = seg_count - 1; bound_idx >= 0; bound_idx--)
	{
		ptr = (int)(table[2][ptr]);
		warping[bound_idx] = table[0][ptr];
	}

	// rebuilding aligned signals
	// old comment:
	// aqui en matlab le hacen una 3ra dimension a Warping q es bT repetido para la cant de muestras, yo lo voy a dejar como bT
	for (int sego_idx = 0; sego_idx < seg_count; sego_idx++)
	{
		// creating the t indexes
		int t_len = (int)(bt[sego_idx + 1] - bt[sego_idx]);
		std::vector<int> t_indexes(t_len);

		// creating x and y indexes
		int idxs_length = (int)(warping[sego_idx + 1] - warping[sego_idx]);

		// validating idxs length (empty vector if wrong)
		if (idxs_length <= 0) {
//            printf("Returning empty spectrum!!!\n");
            return std::vector<double>();
        }

		std::vector<double> x_idxs(idxs_length);
		std::vector<double> y_idxs(idxs_length);

		// for each bt index
		int t_count = 0;
		for (int bt_idx = (int)(bt[sego_idx] - 1); bt_idx < bt[sego_idx + 1] - 1; bt_idx++)
		{
			t_indexes[t_count] = bt_idx;
			t_count++;
		}

		// for each x index
		int x_count = 0;
		for (int bx_idx = (int)(warping[sego_idx]); bx_idx < (int)(warping[sego_idx + 1]); bx_idx++)
		{
			x_idxs[x_count] = bx_idx - warping[sego_idx] + 1;
			y_idxs[x_count] = v[bx_idx - 1];
			x_count++;
		}

		// setting the values in the aligned signal
		double step = (idxs_length - 1.0) / (t_count - 1);
		double lb = x_idxs[0];
		for (int int_p = 0; int_p < t_count; int_p++)
		{
			double xi = lb + int_p * step;
			cow_aligned[t_indexes[int_p]] = interp1q(x_idxs, y_idxs, xi);
		}
	}
	#pragma endregion

	// small bug fix (duplicating second to last value)
	cow_aligned[ref_length - 1] = cow_aligned[ref_length - 2];

	// returning the aligned signal by means of the COW method
	return cow_aligned;
}

/// <summary>
/// Computes interpolation coefficients and corresponding indexes
/// </summary>
/// <param name="n">The length of the segment</param>
/// <param name="slack_coeffs">Slack coefficients</param>
/// <param name="slack_idxs">Slack indexes</param>
/// <returns>The interpolation coefficients and corresponding indexes</returns>
/// <remarks>Taken from the old implementation</remarks>
InterpData compute_interpolation_coefficients(int n, std::vector<double> slack_coeffs, std::vector<double> slack_idxs)
{
	// validating input parameters
	if (slack_coeffs.size() != slack_idxs.size())
		throw std::invalid_argument("The 'slack_coeffs' and 'slack_idxs' vector's sizes must match.");

	// getting the amount of final coefficients and indexes
	int interp_data_length = (int)slack_coeffs.size();

	// creating and initializing interpolation data
	InterpData interp_data;
	interp_data.coefficients = std::vector<std::vector<double> >(interp_data_length);
	interp_data.indexes = std::vector<std::vector<double> >(interp_data_length);

	// creating the x vector
	std::vector<double> x(n);

	// creating the p_bin vector
	std::vector<double> p_bin(n);

    // for each one of the coefficients in 'slack_coeffs'
	for (int i = 0; i < interp_data_length; i++)
	{
		// creating and filling the edges vector
		int edges_size = (int)slack_coeffs[i];
		std::vector<double> edges(edges_size);
		for (int k = 0; k < edges_size; k++)
			edges[k] = k + 1;

		// creating the N vector
		std::vector<double> N(edges_size);

		// filling the p_bin vector
		for (int j = 0; j < n; j++)
			x[j] = j * (slack_coeffs[i] - 1) / (n - 1) + 1;

		// looping over histogram (leyendo histogram count)
		histogram_loop(x, edges, N, p_bin, 1, n);

		// setting new vectors for coefficients and indexes
		interp_data.coefficients[i] = std::vector<double>(n);
		interp_data.indexes[i] = std::vector<double>(n);

		// for each x value
		for (int h = 0; h < n; h++)
		{
			if (x[h] < 1)
				p_bin[h] = 0;

			if (x[h] >= slack_coeffs[i])
				p_bin[h] = slack_coeffs[i] - 2;

			// filling coefficients and indexes
			interp_data.coefficients[i][h] = x[h] - p_bin[h] - 1;
			interp_data.indexes[i][h] = p_bin[h] - slack_idxs[i];
		}
    }

	// returning the computed interpolation data
	return interp_data;
}

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
void histogram_loop(std::vector<double> x, std::vector<double> edges, std::vector<double>& N, std::vector<double>& p_bin, int stride, int mx)
{
	// getting the sizes of x and edges
	int x_size = (int)x.size();
	int edges_size = (int)edges.size();

	// setting the values for n1, n2, x_offset and y_offset
	double n1 = stride == 1 ? stride : x_size / mx;
	double n2 = stride == 1 ? x_size / mx : stride;
	int x_offset = stride == 1 ? 0 : stride * mx - 1;
	int y_offset = stride == 1 ? 0 : stride * edges_size - 1;

	int x_idx = 0;
	int y_idx = 0;
	int bin_idx = 0;
	int y_step = stride * edges_size - y_offset;
	int x_page = x_offset - stride + 1;
	int y_page = y_offset - stride + 1;

	for (int i = 0; i < n1; i++)
	{
		for (int j = 0; j < n2; j++)
		{
			for (int k = 0; k < mx; k++)
			{
				// getting the position of x[x_idx]
				int bin = find_bin(edges, x[x_idx]);

				if (bin >= 0)
				{
					bin_idx = y_idx + stride * bin;
					N[bin_idx] += 1;
				}

				p_bin[x_idx] = bin;
				x_idx += stride;
			}

			x_idx -= x_offset;
			y_idx += y_step;
		}

		// go to next page of input and output arrays
		x_idx += x_page;
		y_idx += y_page;
	}
}

/// <summary>
/// Binary search over a vector
/// </summary>
/// <param name="v">The vector of interest</param>
/// <param name="x">The value to search for</param>
/// <returns>The index 'corresponding' to that value</returns>
/// <remarks>If x is out of bounds, then -1 is returned</remarks>
int find_bin(std::vector<double> v, double x)
{
	// performing binary search
	int index = binary_search(v, x);

	// setting -1 if x wasn't found
	index = (x < v[0] || x > v[v.size() - 1]) ? -1 : index;

	// finally returning the index
	return index;
}

/// <summary>
/// Cummulative sum at each position
/// </summary>
/// <param name="v">The vector of interest</param>
/// <returns>The projective integral for the specified vector</returns>
/// <remarks>The resulting vector has the same size</remarks>
/// <remarks>It's basically a projective integral</remarks>
std::vector<double> cumsum(std::vector<double> v)
{
	// getting vector length
	int v_length = (int)v.size();

	// validating input vector
	if (v_length < 1)
		return std::vector<double>();

	// computing the cummulative sums
	std::vector<double> v_cum(v_length);
	v_cum[0] = v[0];
	for (int i = 1; i < v_length; i++)
		v_cum[i] = v_cum[i - 1] + v[i];

	// returning the cummulative sum
	return v_cum;
}

/// <summary>
/// Derivative for 1-D discrete data
/// </summary>
/// <param name="v">The vector of interest</param>
/// <returns>The derivative of a vector v</returns>
/// <remarks>The resulting vector has 1 less component</remarks>
/// <remarks>The 'derivative' is computed by d[i] = v[i+1] - v[i]</remarks>
std::vector<double> diff(std::vector<double> v)
{
	// getting vector length
	int v_length = (int)v.size();

	// validating input vector
	if (v_length <= 1)
		return std::vector<double>();

	// computing the successive differences
	std::vector<double> v_diff(v_length - 1);
	for (int i = 1; i < v_length; i++)
		v_diff[i - 1] = v[i] - v[i - 1];

	// returning the discrete derivative
	return v_diff;
}

/// <summary>
/// Difference betwwen vectors
/// </summary>
/// <param name="x">The first vector</param>
/// <param name="y">The second vector</param>
/// <returns>The vector resulting from y - x</returns>
std::vector<double> vector_diff(std::vector<double> x, std::vector<double> y)
{
	// validating input vectors
	if (x.size() != y.size())
		throw std::invalid_argument("Mismatch in vector's sizes.");

	// declaring the difference vector
	std::vector<double> diff(x.size());

	// computing componentwise differences
	for (size_t i = 0; i < x.size(); i++)
		diff[i] = y[i] - x[i];

	// returning the difference
	return diff;
}

/// <summary>
/// Norm 2 of a vector
/// </summary>
/// <param name="v">The vector of interest</param>
/// <returns>The norm 2 of v</returns>
double norm2(std::vector<double> v)
{
	// total sum squared
	double total = 0.0;

	// computing total sum squared
	for (size_t i = 0; i < v.size(); i++)
		total += pow(v[i], 2.0);

	// returning the squared root of the total
	return sqrt(total);
}

/// <summary>
/// Quick 1-D linear interpolation
/// </summary>
/// <param name="x">A monotonically increasing vector</param>
/// <param name="y">A vector with the same size of x</param>
/// <param name="xi">The value to interpolate</param>
/// <returns>The value of the 1-D function Y at the points of column vector xi using linear interpolation</returns>
/// <remarks>interp1q from MATLAB will be removed in a future release. Use INTERP1 instead</remarks>
/// <remarks>returns NaN for any values of xi that lie outside the coordinates in x</remarks>
double interp1q(std::vector<double> x, std::vector<double> y, double xi)
{
	// validating input vectors
	if (x.size() != y.size())
		throw std::invalid_argument("Mismatch in vector's sizes.");

	// getting the size of x
	int x_length = (int)x.size();

	// binary search for the value xi
	int r = find_bin(x, xi);

	// returning some sort of NAN if xi is out of range
	if (r < 0)
		return std::numeric_limits<float>::max();;

	// adjusting value of r if necessary
	r = std::min(r, x_length - 2);

	// computing the corresponding yi value
	double u = (xi - x[r]) / (x[r + 1] - x[r]);
	double yr = y[r];
	double yi = yr + ((y[r + 1] - yr) * u);

	// returning the computed value
	return yi;
}

/// <summary>
/// Gets the position in an sorted array where a value sould be
/// </summary>
int binary_search(std::vector<double> arr, double value)
{
    int lb = 0;
    int ub = arr.size() - 1;
    int half;

    // while search makes sense
    while (lb <= ub)
    {
        // computing half index
        half = (lb + ub) / 2;

        if (value < arr[half])
            ub = half - 1;
        else if (value > arr[half])
            lb = half + 1;
        else
            return half;
    }

    // if value not found, returning ub as the index
    return ub;
}