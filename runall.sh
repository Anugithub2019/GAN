#!/bin/bash
#SBATCH --job-name="tune"
#SBATCH --output=tune.out
#SBATCH --error=tune.err
#SBATCH --nodes=1
#SBATCH --partition=gpu
#SBATCH --gres=gpu:v100:2
#SBATCH --mail-type=ALL
#SBATCH --mail-user=anupam.chaudhuri@deakin.edu.au

module purge
module load Anaconda3
source activate tensorflow-gpu-2 
python3 GAN.py 
