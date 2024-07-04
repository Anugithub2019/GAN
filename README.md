# GAN

# Experiment: Evaluating GAN Performance Using Topological Data Analysis

This experiment aims to train a Generative Adversarial Network (GAN) and evaluate its performance using Topological Data Analysis (TDA). The focus is on assessing the topological consistency of generated images with the real image set.

## Experiment Overview

To train a GAN, we start with a set of images referred to as the 'real image set', denoted by `Ir`. Each image in `Ir` has dimensions of 32 × 32 × 3, which we embed into a vector space `$R^{32×32×3}$`, representing each pixel as a dimension. This results in a point cloud representation for the real image set.

We apply TDA to characterize this point cloud with features such as persistence homology diagrams (`PD_{rk}`). We quantify this set using measures like entropy or the Wasserstein distance. For example, the entropy associated with `PD_{rk}` can be represented as `E_{rk}`.

We hypothesize that the performance of a GAN can be evaluated by examining the point cloud for the generated images at the `i-th` epoch (`I_i`). The corresponding persistence diagram is `PDkgi`, and its associated entropy value is `Egik`. This approach allows us to quantitatively assess the GAN’s performance in generating images that are topologically consistent with the real image set.

We also hypothesize that this convergence should hold for other metrics that quantify the manifold, such as the number of intrinsic dimensions.

## Dataset and Model

We perform a preliminary evaluation using a GAN trained on cat images from the CIFAR-10 dataset, following a popular [online tutorial](https://machinelearningmastery.com/how-to-develop-a-generative-adversarial-network-for-a-cifar-10-small-object-photographs-from-scratch/).

### Data Loading and Visualization

- CIFAR-10 dataset is loaded, and cat images are extracted.
- We use the 5000 cat images available in the CIFAR-10 training set.

### Discriminator Model

- The discriminator is a convolutional neural network (CNN) that takes (32, 32, 3) images as input.
- Uses LeakyReLU activations, down-sampling, dropout for regularization, and outputs binary classification results.
- Binary cross-entropy loss and the Adam optimizer are used for training.

### Generator Model

- The generator takes a noise vector of size 100 as input.
- Dense layers upscale the noise into a 3D tensor, and transpose convolutional layers (Conv2DTranspose) up-sample the data.
- The output layer uses a tanh activation function to generate pixel values in the range [-1, 1].

### GAN Model

- The GAN model combines the generator and discriminator.
- The discriminator’s weights are set as non-trainable.
- Compiled with binary cross-entropy loss and the Adam optimizer.

### Training Process

- Real and fake samples are generated for training the discriminator.
- The discriminator and generator models are trained iteratively.
- The discriminator is trained on both real and fake samples.
- The generator is trained to minimize the ability of the discriminator to distinguish real from fake samples.
- Model performance and generated images are periodically summarized during training.

### Training Loop

- The training loop runs for 500 epochs with a batch size of 128.
- Performance and results are periodically summarized.

## Metric Calculation

At every 10th epoch, we use the GAN to generate a sample of 1000 fake images and calculate the intrinsic dimensions and topological features based on this sample. We also calculate these metrics for a random sample of 1000 real cat images to determine if the metrics of the learned manifold on which the generated fake images lie converge towards that of the manifold on which the real data lies.

For comparison to existing work, we also compute the Fréchet Inception Distance (FID) between a sample of 5000 generated images and the full dataset of 5000 real images. We employ the official implementation of the FID score, available at this [GitHub repository](https://github.com/bioinf-jku/TTUR), to calculate the FID score for each epoch.

To verify if our findings are applicable to images other than cats, we also tested on images of dogs from the CIFAR-10 dataset using the same GAN architecture and evaluation metrics.

## References

- [TDA Documentation](https://giotto-ai.github.io/gtda-docs/)
- [GAN Tutorial](https://machinelearningmastery.com/how-to-develop-a-generative-adversarial-network-for-a-cifar-10-small-object-photographs-from-scratch/)

