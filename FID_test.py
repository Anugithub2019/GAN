#import subprocess
import pandas as pd
from pytorch_fid.fid_score import *
def get_fid_scores(start, end, step, base_dir):
    """
    Retrieves FID scores for directories named 'epoch_x' from start to end with a given step.

    Args:
    start (int): Starting epoch number.
    end (int): Ending epoch number.
    step (int): Step between epoch.
    base_dir (str): Base directory containing epoch subdirectories.

    Returns:
    pd.DataFrame: A DataFrame with columns 'Epoch' and 'FID' containing the scores.
    """
    data = []
    
    for epoch in range(start, end + 1, step):
        dir_name = f"epoch_{epoch}"
        path = f"{base_dir}/{dir_name}"  # Construct path to directory

        # Construct the command to run
        command = f"python -m pytorch_fid real_2000 {path}"
        result = calculate_fid_given_paths(['real',path], 50, 'cuda', 2048, 8)
        
        # Run the command
        #result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # # Extract FID score from the output
        # #output = result.stdout.strip()
        # try:
        #     fid_score = float(output.split()[-1])  # Assumes the last word in output is the FID score
        # except ValueError:
        #     print(f"Failed to extract FID from output: {output}")
        #     continue
        fid_score = result
        # Append the result
        data.append({"Epoch": epoch, "FID": fid_score})
        print({"Epoch": epoch, "FID": fid_score})
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    
    return df

# Example usage
base_dir = "."
fid_df = get_fid_scores(9, 499, 10, base_dir)
#print(fid_df)
fid_df.to_csv('CAT_FID_score.csv', index=False)
