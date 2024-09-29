import subprocess
import pandas as pd

def get_fid_scores(start, end, step, base_dir):
    """
    Retrieves FID scores for directories named 'epoch_x' from start to end with a given step.
    """
    data = []
    python_path = "/sw/software/Anaconda3/2020.11/bin/python"  # Adjust this to the path of the Python interpreter with pytorch_fid installed
    
    for epoch in range(start, end + 1, step):
        dir_name = f"epoch_{epoch}"
        path = f'"{base_dir}/{dir_name}"'  # Construct path to directory, quoted in case there are spaces
        
        # Construct the command to run
        command = f"{python_path} -m pytorch_fid real {path}"
        print(f"Running command: {command}")  # Debug print

        # Run the command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Debug prints
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        
        if result.returncode != 0:
            print(f"Command failed with return code {result.returncode}")
            continue
        
        # Extract FID score from the output
        try:
            fid_score = float(result.stdout.strip().split()[-1])  # Assumes the last word in output is the FID score
            data.append({"Epoch": epoch, "FID": fid_score})
            print({"Epoch": epoch, "FID": fid_score})
        except ValueError:
            print(f"Failed to extract FID from output: '{result.stdout.strip()}'")
            continue
    
    # Create a DataFrame
    df = pd.DataFrame(data)
    return df

# Example usage
base_dir = "."  # Adjust this as necessary
fid_df = get_fid_scores(9, 499, 10, base_dir)
print(fid_df)
fid_df.to_csv('CAT_FID_score.csv', index=False)
