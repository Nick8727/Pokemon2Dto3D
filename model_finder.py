import pandas
import os
from zipfile import ZipFile 



def get_model(df, idx):
    """
    Uses the idx of the csv to find the unzipped model file
    
    Args:
        csv: The pandas dataframe with the format of train_labels.csv
        idx: the index of the pokemon

    Returns:
        The path to the model in the models folder, returns None if it cannot be found (only finds .FBX files)
    """
    filename = df["filename"][idx]

    local_dir = os.path.dirname(__file__)
    zip_path = os.path.join(local_dir, "zips")
    model_path = os.path.join(local_dir, "models")
    zip_file_path = os.path.join(zip_path, filename)

    subpath = None
    with ZipFile(zip_file_path) as pokefile:
        names = pokefile.namelist()
        for name in names:
            if name.endswith(".FBX"):
                subpath = name
                break

    if subpath == None:
        return None

    model_path = os.path.join(model_path, subpath)
    return model_path


csv_df = pandas.read_csv("train_labels.csv")
csv_df = csv_df.drop(["Unnamed: 0"], axis=1)

filename = get_model(csv_df, 5)
filename = filename.replace("/", "\\")
print(filename)
