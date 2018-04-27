import numpy as np
from scipy import sparse as sp
import six
import tensorflow as tf


def create_tensorrec_iterator(name):
    return tf.data.Iterator.from_structure(
            output_types=(tf.int64, tf.float32, tf.int64, tf.int64),
            output_shapes=([None, 2], [None], [], []),
            shared_name=name
    )


def create_tensorrec_dataset_from_sparse_matrix(sparse_matrix):
    if not isinstance(sparse_matrix, sp.coo_matrix):
        sparse_matrix = sp.coo_matrix(sparse_matrix)

    indices = np.array([[pair for pair in six.moves.zip(sparse_matrix.row, sparse_matrix.col)]], dtype=np.int64)
    values = np.array([sparse_matrix.data], dtype=np.float32)
    n_dim_0 = np.array([sparse_matrix.shape[0]], dtype=np.int64)
    n_dim_1 = np.array([sparse_matrix.shape[1]], dtype=np.int64)

    tensor_slices = (indices, values, n_dim_0, n_dim_1)

    return tf.data.Dataset.from_tensor_slices(tensor_slices)


def get_dimensions_from_tensorrec_dataset(dataset, session):
    iterator = create_tensorrec_iterator('dims_iterator')
    initializer = iterator.make_initializer(dataset)
    _, _, tf_d0, tf_d1 = iterator.get_next()

    session.run(initializer)
    d0, d1 = session.run([tf_d0, tf_d1])

    return d0, d1
