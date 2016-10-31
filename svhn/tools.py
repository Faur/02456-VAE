import numpy as np
import matplotlib.pyplot as plt
import theano
import theano.tensor as T
import lasagne 
import lasagne.layers as L


def onehot(t, num_classes):
	""" Convert integer encodeing into one hot encoding. """
	out = np.zeros((t.shape[0], num_classes))
	for row, col in enumerate(t):
		out[row, col] = 1
	return out

def shared_dataset(data_xy, borrow=True):
	""" Function that loads the dataset into shared variables

	The reason we store our dataset in shared variables is to allow
	Theano to copy it into the GPU memory (when code is run on GPU).
	Since copying data into the GPU is slow, copying a minibatch everytime
	is needed (the default behaviour if the data is not in a shared
	variable) would lead to a large decrease in performance.
	"""
	data_x, data_y = data_xy
	shared_x = theano.shared(np.asarray(data_x,
										   dtype=theano.config.floatX),
							 borrow=borrow)
	shared_y = theano.shared(np.asarray(data_y,
										   dtype=theano.config.floatX),
							 borrow=borrow)
	# When storing data on the GPU it has to be stored as floats
	# therefore we will store the labels as ``floatX`` as well
	# (``shared_y`` does exactly that). But during our computations
	# we need them as ints (we use labels as index, and if they are
	# floats it doesn't make sense) therefore instead of returning
	# ``shared_y`` we will have to cast it to int. This little hack
	# lets ous get around this issue
	return shared_x, T.cast(shared_y, 'int32')


def plot_svhn(x, t=10, title='SVHN visualizer', IMG_LEN=32, gray = False):
    
    idx = [np.random.randint(0, x.shape[0]) for i in range(t*t)]

    if gray:
        canvas= np.zeros((IMG_LEN*t, IMG_LEN*t))
    else:
        canvas= np.zeros((IMG_LEN*t, IMG_LEN*t, 3))
    for i in range(t):
        for j in range(t):
            img = x[idx[i*t + j]].reshape((IMG_LEN, IMG_LEN, 3))
            if gray:
                img = img.sum(axis=-1)
                canvas[i*IMG_LEN:(i+1)*IMG_LEN, j*IMG_LEN:(j+1)*IMG_LEN] = img
            else:
                canvas[i*IMG_LEN:(i+1)*IMG_LEN, j*IMG_LEN:(j+1)*IMG_LEN, :] = img
    
    plt.figure(figsize=(7, 7))
    if gray:
        plt.imshow(canvas, cmap='gray')
    else:
        plt.imshow(canvas)
    plt.title(title)
    plt.show()





		
