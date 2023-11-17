# -*- coding: utf-8 -*-
"""Untitled20.ipynb

Automatically generated by Colaboratory.

Original file is located at
		https://colab.research.google.com/drive/1_Z9mQs-Hk2k-xLCzYiWINT75iOguNydf
"""

from keras.datasets.cifar10 import load_data
from matplotlib import pyplot
#load the image into the memory
(trainX, trainy), (textX, testy) = load_data()
#plot the images from the training set
for i in range(49):
	pyplot.subplot(7,7,1+i)
	#turn of axis
	pyplot.axis('off')
	#plot raw pixel data
	pyplot.imshow(trainX[i])
pyplot.show()

from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Dense
from keras.layers import Conv2D
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import LeakyReLU
from keras.layers import Conv2DTranspose
from keras.layers import Reshape
from keras.utils import plot_model
from dadapy import Data
import numpy as np
#import gudhi as gd

# define the standalone discrimantor model
def define_discriminator(in_shape = (32,32,3)):
		model = Sequential()
		#normal
		model.add(Conv2D(64, (3,3), padding = 'same', input_shape = in_shape))
		model.add(LeakyReLU(alpha = 0.2))

		#downsample
		model.add(Conv2D(128, (3,3), strides=(2,2),padding = 'same'))
		model.add(LeakyReLU(alpha = 0.2))

		#downsample
		model.add(Conv2D(128,(3,3), strides=(2,2), padding = 'same'))
		model.add(LeakyReLU(alpha=0.2))

		#downsample
		model.add(Conv2D(256,(3,3), strides=(2,2), padding = 'same'))
		model.add(LeakyReLU(alpha=0.2))

		#classifier
		model.add(Dropout(0.4))
		model.add(Flatten())
		model.add(Dense(1, activation = 'sigmoid'))

		#compile model
		opt = Adam(lr = 0.0002, beta_1 = 0.5)
		model.compile(loss="binary_crossentropy",optimizer = opt, metrics = ['accuracy'])
		return model

#define model
#model = define_discriminator()
#model.summary()
#plot the model
#plot_model(model, to_file = 'discriminator_plot.png', show_shapes= True, show_layer_names = True)

# Now we want to train the Discriminator there is two type of data original and fake

def load_real_samples():
	# load cifar10 dataset
	(trainX, _), (_, _) = load_data()
	# Take only cat image 
	trainX = trainX[trainy.ravel() == 3]

	# covert from unsigned ints to floats
	X = trainX.astype('float32')
	#scale from [0,255] to [-1,1]
	X = (X - 127.5)/ 127.5
	return X

#X = load_real_samples()
#X.shape

# select real samples
def generate_real_samples(dataset, n_samples):
				# choose random instances
				ix = np.random.randint(0, dataset.shape[0], n_samples)
				X = dataset[ix]
				# generate 'real' class labels (1)
				y = np.ones((n_samples, 1))
				return X,y

# generate fake samples
def generate_fake_samples(g_model,latent_dim ,n_samples):
	# generate uniform random numbers in [0,1]
	X_input = generate_latent_points(latent_dim, n_samples)
	#X = np.random.rand(32*32*3*n_samples)
	# update to have the range [-1,1]
	#preditcs outputs
	X = g_model.predict(X_input)
	# reshape into batch of colour images
	#X = X.reshape((n_samples, 32,32, 3))
	# generate 'fake' class labels (0)
	y = np.zeros((n_samples, 1))
	return X,y


# define generator model ( it's a neural network) the output is a image of shape (32x32x3) input is a noise
# What Conv2DTranspose make the image upscale bigger
# Noise is known as latent variable
def define_generator(latent_dim):
	 model = Sequential()
	 # foundation for 4x4 image
	 n_nodes = 256 * 4 *4
	 model.add(Dense(n_nodes, input_dim = latent_dim))
	 model.add(LeakyReLU(alpha=0.2))
	 model.add(Reshape((4,4,256))) # 4x4 image and depth is 256
	 #upsample to 8x8
	 model.add(Conv2DTranspose(128,(4,4), strides = (2,2), padding='same'))
	 model.add(LeakyReLU(alpha =0.2))
	 #upsample to 16 x16
	 model.add(Conv2DTranspose(128,(4,4), strides = (2,2), padding='same'))
	 model.add(LeakyReLU(alpha =0.2))
	 #upsample to 32x32
	 model.add(Conv2DTranspose(128,(4,4), strides = (2,2), padding='same'))
	 model.add(LeakyReLU(alpha =0.2))
	 #Output layer
	 model.add(Conv2D(3,(3,3), activation='tanh',padding='same'))
	 return model

# define the size of the latent space
#latent_dim = 100
# define the generator model
#model = define_generator(latent_dim)
#summarize the model
#model.summary()
#plot the model
#plot_model(model, to_file='generator_plot.png',show_shapes=True, show_layer_names=True)

# Generator gives data to discriminator and want to improve to become as good as real image
def generate_latent_points(latent_dim, n_samples):
	# generate points in the latent space
	x_input = np.random.randn(latent_dim * n_samples)
	#reshape into a batch of inputs for the network
	x_input = x_input.reshape(n_samples, latent_dim)
	return x_input



# size of the latent space
#latent_dim = 100
# define the discriminator model
#model = define_generator(latent_dim)
# generate samples
#n_samples = 49
#X, _ = generate_fake_samples(model, latent_dim, n_samples)
#scale pixel values from [-1,1] to [0,1]
#X = (X+1)/2
# plot the generated samples
#for i in range(n_samples):
	#define subplot
#	pyplot.subplot(7,7,i+1)
#	pyplot.axis('off')
#	pyplot.imshow(X[i])
#pyplot.show()

def define_gan(g_model, d_model):
	#make weights in the discriminator not trainable
	#very important, else will modify discriminator weights as well (i.e. get good generation score by crippling discriminator)!!!
	d_model.trainable = False
	model = Sequential()
	# add generator
	model.add(g_model)
	# add discriminator
	model.add(d_model)
	#compile model
	opt = Adam(lr = 0.0002, beta_1 = 0.5)
	model.compile(loss = 'binary_crossentropy', optimizer = opt)
	return model


# train the generator and discriminator
def train(g_model, d_model, gan_model, dataset, latent_dim, n_epochs=200, n_batch=128):
	bat_per_epo = int(dataset.shape[0]/n_batch)
	half_batch = int(n_batch/2)
	# manually enumerate epochs
	for i in range(n_epochs):
		#enumerate batches over the training set
		for j in range(bat_per_epo):
			# get randomly selected 'real' images
			X_real, y_real = generate_real_samples(dataset, half_batch)
			#generate 'fake' examples
			X_fake, y_fake = generate_fake_samples(g_model, latent_dim, half_batch)
			# create training set for the discriminator
			X, y = np.vstack((X_real, X_fake)), np.vstack((y_real, y_fake))
			# update discrinator model weights
			d_loss, _ = d_model.train_on_batch(X, y)
			#prepare points in latent space as iput for the generator
			X_gan = generate_latent_points(latent_dim, n_batch)
			# create inverted labels for the fake samples
			y_gan = np.ones((n_batch,1))
			#update the generator via the discriminators's error
			g_loss = gan_model.train_on_batch(X_gan, y_gan)
			# summarise loss on this batch
			print('>%d, %d/%d, d1=%.3f,g=%.3f' % (i+1, j+1, bat_per_epo, d_loss, g_loss))
		#evaluate the model perfomance, sometime
		if (i+1) % 10 == 0:
		#if i % 10 == 0:
			summarize_performance(i,g_model, d_model, dataset, latent_dim)
			intr_dim(i,g_model, d_model, dataset, latent_dim)


# write headers for intrinsic_dim file
with open("intrinsic_dim.csv", "w") as file:
	file.write(f"epoch,intrinsic_dim,err1\n")

def intr_dim(epoch, g_model, d_model, dataset, latent_dim, n_samples=300):
	x_fake, _ = generate_fake_samples(g_model, latent_dim, n_samples)

	# unravel each x_fake tensor into a flat vector (datapoint) so that we have a set of n_samples datapoints
	x_fake_flat = x_fake.reshape(n_samples, -1)  # Reshaping to (n_samples, 3072)

	# calculate intrinsic dimensions of x_fake
	intrinsic_dim,err1,_ = calculate_intrinsic_dimension(x_fake_flat)
	# Note: You'll need to define `calculate_intrinsic_dimension` based on your chosen method

	# save result to file (or print it out), include the epoch in the file name
	filename = f"intrinsic_dim_epoch_{epoch}.txt"
	with open(filename, "w") as file:
		file.write(f"Intrinsic Dimension at epoch {epoch}: {intrinsic_dim} Standard error: {err1}\n")

	# save result to file (or print it out), include the epoch in the file name
	with open("intrinsic_dim.csv", "a") as file:
		file.write(f"{epoch},{intrinsic_dim},{err1}\n")


	# Alternatively, just print it out
	print(f"Intrinsic Dimension at epoch {epoch}: {intrinsic_dim} Standard error: {err1}\n")


def calculate_intrinsic_dimension(data):
    """
    Estimate the intrinsic dimension of a dataset using the 2NN method from GUDHI.

    Parameters:
    data (numpy.ndarray): The dataset, where each row is a datapoint.

    Returns:
    float: The estimated intrinsic dimension.
    """
    

    # Fit the model on the data and estimate the dimension
    ID1, err1, scale1 = Data(data).compute_id_2NN(decimation = 1)
    return ID1, err1, scale1

# evaluate the discriminator, plot generted images, save generator model
def summarize_performance(epoch, g_model, d_model, dataset, latent_dim, n_samples=150):
	# prepare real samples
	X_real, y_real = generate_real_samples(dataset, n_samples)
	# evalute discrimator on real examples
	_, acc_real = d_model.evaluate(X_real, y_real, verbose =0)
	# prepare fake examples
	x_fake, y_fake = generate_fake_samples(g_model, latent_dim, n_samples)
	# evaluate discriminator on fake examples
	#print(x_fake.shape, y_fake.shape)
	#import pdb; pdb.set_trace()
	_, acc_fake = d_model.evaluate(x_fake, y_fake, verbose =0 )
	# summarise discrimator performance
	print('>Accuracy real:%.0f%%, fake: %.0f%%' % (acc_real*100, acc_fake*100))

	save_plot_with_probs(X_real, d_model, 'real_images_%03d.png' %(epoch +1))
	save_plot_with_probs(x_fake, d_model, 'fake_images_%03d.png' %(epoch +1))

	#save plot
	save_plot(x_fake, epoch)
	#save the generator model tile file
	filename = 'generator_model_%03d.h5' %(epoch +1)
	g_model.save(filename)


# ChatGPT generated code to save images with discriminator probability of real underneath
def save_plot_with_probs(examples, model, filename, n=7):
	# Scale from [-1,1] to [0,1]
	examples = (examples + 1) / 2.0

	for i in range(n * n):
		# Define subplot
		pyplot.subplot(n, n, 1 + i)
		# Turn off axis
		pyplot.axis('off')
		# Plot raw pixel data
		pyplot.imshow(examples[i])
		
		# Get the probability from the model
		probability = model.predict(np.expand_dims(examples[i], axis=0))[0][0]
		pyplot.text(2, 2, f"{probability:.4f}", color='white', fontsize=8, bbox=dict(facecolor='black', alpha=0.7))
	
	# Save plot to file
	pyplot.savefig(filename)
	pyplot.close()



#create and save a plot of generated images
def save_plot(examples, epoch, n =7):
	#scale from [-1,1] to [0,1]
	examples = (examples + 1)/2
	#plot images
	for i in range(n*n):
		# define subplot
		pyplot.subplot(n,n,1+i)
		#turn off axis
		pyplot.axis('off')
		#plot raw pixel data
		pyplot.imshow(examples[i])
		#save plot to file
		filename = 'generated_plot_e%3d.png'% (epoch + 1)
		pyplot.savefig(filename)
		pyplot.close


#size of the latent space
latent_dim = 100
# create the discriminator
d_model = define_discriminator()
# create generator
g_model = define_generator(latent_dim)
#create the gan
gan_model = define_gan(g_model, d_model)
#summarize gan model
gan_model.summary()
#plot gan model
#plot_model(gan_model, to_file='gan_plot.png',show_shapes= True, show_layer_names=True)
dataset = load_real_samples()


train(g_model, d_model, gan_model, dataset, latent_dim, n_epochs=200, n_batch=128)