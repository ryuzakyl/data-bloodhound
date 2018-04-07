#include "dcomb.h"

/**
Funcion que devuelve un vector  binario que describe la presencia(1) o no(0) de una sustancia de origen. 
**/
vector<double> presence(vector<double> vector_origin)
{
	vector<double> vector_presence;
		
	for( int j=0; j < vector_origin.size();j++)
	{	
		if (vector_origin[j]!=0)
		{
			vector_presence.push_back(1);
		}
		else{vector_presence.push_back(vector_origin[j]);}
	}
			
	return vector_presence;
}

double dist_presence(vector<double> vector_incognita, vector<double> vector_origin)
{
	vector<double> presence_incognita = presence(vector_incognita);
	double dist_presence=0.0;
	
	vector<double> presence_origin=presence(vector_origin);
    for (int j=0; j<vector_origin.size();j++)
    {
        dist_presence += pow(presence_incognita[j] - presence_origin[j], 2.0);
    }

	return sqrt(dist_presence);
}

/*** Funcion que calcula la distancia de correlacion de Pearson entre dos vectores***/
double correlation(vector<double> vector_incognita, vector<double> vector_origin)
{
	double den=0;
	double correlation;
	double sum=0;
	double sum2=0;
	double sum1=0;
	double sum3=0;
	double sum4=0;
	double mean_incognita;
	double mean_origin;
	for(int i=0; i < vector_origin.size();i++)
	{
		sum1 += vector_origin[i];
		sum2 += vector_incognita[i];
	}

	mean_incognita=sum2/vector_origin.size();
	mean_origin=sum1/vector_origin.size();
	for(int j=0; j < vector_origin.size();j++)
	{
		sum += (vector_origin[j] - mean_origin) * (vector_incognita[j] - mean_incognita);
		sum3 += pow(vector_origin[j] - mean_origin, 2.0);
		sum4 += pow(vector_incognita[j] - mean_incognita, 2.0);
	}
	den=sqrt(sum3*sum4);
	correlation=1-(sum/den);// define la distancia de correlacion, siendo num/den, la correlation de pearson
	
	return correlation;
}

/**
 * Funcion que define una signatura S=[S_1,...,S_n], donde dado un conjunto A, S_k(A)={w_k,m_k}
 * Resultado: Devuelve en S, las matrices w y m
 **/
vector<vector<double>> Definition_Signature(vector<double> vector_origin)
{
	vector<vector<double>> Signature;
	vector<double> w;
	vector<double> m;
	vector<double> vect;
	vector<double> vect2;
	for(int j=0; j < vector_origin.size(); j++)
	{
		if (vector_origin[j] > 0)
		{
			w.push_back(j);
			m.push_back(vector_origin[j]);
		}
	}

	Signature.push_back(w);
	Signature.push_back(m);
	return Signature;
}

vector<vector<vector<double>>> Extended_Signature(vector<double> vector_incognita, vector<double> vector_origin)
{
	vector<vector<double>> Signature1_new;
	vector<vector<double>> Signature2_new;
	vector<vector<vector<double>>> Signatures_new;
	vector<vector<double>> Signature1=Definition_Signature(vector_incognita);
	vector<vector<double>> Signature2=Definition_Signature(vector_origin);
	vector<double> w1;
	vector<double> w2;
	vector<double> m1;
	vector<double> m2;
	int i=0;
	int j=0;
	while ( i < Signature1[0].size() & j < Signature2[0].size())
	{
		if(Signature1[0][i] < Signature2[0][j] || j==Signature2[0].size() )
		{
			w1.push_back(Signature1[0][i]);//Signature1_new[1][z]= Signature1[1][i];
			w2.push_back(Signature1[0][i]);//Signature2_new[1][z]=Signature1[1][i];

			m1.push_back(Signature1[1][i]); //Signature1_new[2][z]= Signature1[2][i];
			m2.push_back(0);//Signature2_new[2][z]= 0;
			i++;

		}
		else if(Signature1[0][i] > Signature2[0][j] || i==Signature1[0].size())
		{
			w1.push_back(Signature2[0][j]);//Signature1_new[1][z]= Signature2[1][j];
			w2.push_back(Signature2[0][j]);//Signature2_new[1][z]=Signature2[1][j];

			m2.push_back(Signature2[1][j]);//Signature2_new[2][z]= Signature2[2][j];
			m1.push_back(0);//Signature1_new[2][z]= 0;
			j++;
		}
		else
		{
			w1.push_back(Signature1[0][i]);//Signature1_new[1][z]=Signature1[1][i];
			w2.push_back(Signature1[0][i]);//Signature2_new[1][z]=Signature1[1][i];

			m1.push_back(Signature1[1][i]);//Signature1_new[2][z]= Signature1[2][i];
			m2.push_back(Signature2[1][j]);//Signature2_new[2][z]= Signature2[2][j];
			i++;
			j++;
		}
	}

		Signature1_new.push_back(w1);Signature1_new.push_back(m1);
		Signature2_new.push_back(w2);Signature2_new.push_back(m2);
		Signatures_new.push_back(Signature1_new);
		Signatures_new.push_back(Signature2_new);
		//Signatures.push_back(Signatures_new);



		return Signatures_new;
}
	
double dist_nominal(vector<double> vector_incognita, vector<double> vector_origin)
{
	double distance_nominal =0.0;
	vector<vector<vector<double>>> Signatures_new=Extended_Signature(vector_incognita,vector_origin);
	for(int i=0; i < Signatures_new[0][0].size(); i++)
	{
		distance_nominal += abs(Signatures_new[0][1][i]-Signatures_new[1][1][i]);
	}

	return distance_nominal;
}
	
double dist_ordinal(vector<double> vector_incognita, vector<double> vector_origin)
{
	double distance_ordinal=0.0;
	double p=0.0;
	vector<vector<vector<double>>> Signatures_new=Extended_Signature(vector_incognita,vector_origin);
	for(int i=0; i < Signatures_new[0][0].size()-1; i++)
	{
		p+= Signatures_new[0][1][i] - Signatures_new[1][1][i];
		distance_ordinal+= (Signatures_new[0][0][i+1]-Signatures_new[0][0][i])*abs(p);
	}


	return distance_ordinal;
}

double dnom_vec(vector<double> x, vector<double> y)
{
	double d_pres = dist_presence(x, y);

	double d_corr = correlation(x, y);

	double d_hist = dist_nominal(x, y);

	return 0.5 * d_pres + 0.25 * d_corr + 0.25 * d_hist;
}

extern "C"
double dnom(double* x, double* y, int count)
{
	vector<double> vx(x, x + count);
	vector<double> vy(y, y + count);

	return dnom_vec(vx, vy);
}

double dord_vec(vector<double> x, vector<double> y)
{
	double d_pres = dist_presence(x, y);

	double d_corr = correlation(x, y);

	double d_hist = dist_ordinal(x, y);

	return 0.5 * d_pres + 0.25 * d_corr + 0.25 * d_hist;
}

extern "C"
double dord(double* x, double* y, int count)
{
	vector<double> vx(x, x + count);
	vector<double> vy(y, y + count);

	return dord_vec(vx, vy);
}
