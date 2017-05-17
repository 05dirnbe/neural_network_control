#include <iostream>
#include <vector>
#include <Eigen/Dense>

#include "integer_matrix_generated.h"

using namespace Buffer;
using namespace Eigen;
using namespace std;

template < typename M, typename T >
const M generate_matrix(const unsigned int nrow, const unsigned int mcol){

	const MatrixXd m = (MatrixXd::Random(nrow,mcol) + MatrixXd::Ones(nrow,mcol) ) * 5;
	return m.cast< const T >();
}

int main() {


	typedef int32_t value_t;
	typedef uint8_t buffer_t;
	typedef Matrix< value_t, Dynamic, Dynamic, RowMajor > matrix_t;
	typedef Matrix< value_t, Dynamic, 1 > vector_t;
	
	auto matrix = generate_matrix<matrix_t, value_t>(2,3);
	
	cout << matrix << endl;

	const auto n = matrix.rows();
	const auto m = matrix.cols();
	const value_t * const flat_data = matrix.data();


	flatbuffers::FlatBufferBuilder builder(0);
	const auto data_vector = builder.CreateVector(flat_data, n * m );
	const auto mat = CreateIntegerMatrix(builder, n , m, data_vector);
	builder.Finish(mat);

	const buffer_t * const buffer = builder.GetBufferPointer();
	
	// # We now have a FlatBuffer that we could store on disk or send over a network.

	// # ...Saving to file or sending over a network code goes here...

	// # Instead, we are going to access this buffer right away (as if we just
	// # received it).

	const auto mat_restored = GetIntegerMatrix(buffer);

	const auto n_restored = mat_restored -> n();
	const auto m_restored = mat_restored -> m();
	const auto data_restored = mat_restored -> data();
	const auto data_size = data_restored -> Length();

	vector_t flat_data_restored(data_size);
	
	for (unsigned int i = 0; i < data_size; ++i)
		flat_data_restored[i] =  data_restored->Get(i);

	
	// cout << "restored n to: " << n << endl;
	// cout << "restored m to: " << m << endl;
	// cout << "restored data has size: " << data_size << endl;

	// cout << "data restored to : \n" << flat_data_restored << endl;
	
	const Map<matrix_t> matrix_restored(flat_data_restored.data(), n_restored, m_restored);

	cout << matrix_restored << endl;

	assert(matrix == matrix_restored);

}