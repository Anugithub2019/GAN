#!/bin/bash
#SBATCH --job-name="tune"
#SBATCH --output=tune_fid.out
#SBATCH --error=tune_fid.err
#SBATCH --nodes=1
#SBATCH --partition=gpu
#SBATCH --gres=gpu:v100:2
#SBATCH --mem=80G
#SBATCH --cpus-per-task=12
#SBATCH --mail-type=ALL
#SBATCH --mail-user=anupam.chaudhuri@deakin.edu.au

module purge
module load Anaconda3
source activate pytorch
python3 FID_test.py 

