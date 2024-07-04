
from keras.datasets.cifar10 import load_data
from matplotlib import pyplot
import os

(trainX, trainy), (textX, testy) = load_data()
trainX = trainX[trainy.ravel() == 3]

def save_images_for_real(examples, n_samples=4000, n=10):
	
# Create a directory for the current epoch

	dir_path = 'real'
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	
	#   # Scale from [-1,1] to [0,1]
	# 	X = (X + 1) / 2.0
	#examples = (examples + 1) / 2.0
	# 	# Save each image to the directory
	for i in range(n_samples):
		pyplot.imshow(examples[i])
		pyplot.axis('off')
	# Save the pyplot figure to a file
		filename = f'{dir_path}/image_{i+1:03d}.png'
		pyplot.savefig(filename)
		pyplot.close()  # Close the plot to free up memory

	print(f'Saved {n_samples} images to directory {dir_path}')
 
save_images_for_real(trainX)