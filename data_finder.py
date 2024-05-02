import os
import pandas as pd
from zipfile import ZipFile 
import csv


def get_model(df, idx):
    """
    Uses the dex of the csv to find the unzipped model file
    
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
    model_path = model_path.replace("/", "\\")
    return model_path

def get_sprite(dex_no):
    local_dir = os.path.dirname(__file__)
    sprite_folder_path = os.path.join(local_dir, "sprites")
    sprite_path = os.path.join(sprite_folder_path, "{}.png".format(int(dex_no)))
    return sprite_path



csv_df = pd.read_csv("train_labels.csv")
csv_df = csv_df.drop(["Unnamed: 0"], axis=1)

pokedex = pd.read_csv("pokedex.csv")
pokedex = pokedex[["National\nDex", "Pokemon\nName"]]
pokedex.columns = ["dex_no", "name"]

df = pd.merge(csv_df, pokedex, left_on="label", right_on="name")
df = df[df['dex_no'].apply((lambda x: x.is_integer()))]
df['dex_no'] = df['dex_no'].apply((lambda x: int(x)))


#generating csv
with open('data_loc.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["dex_no", "label", "model_path", "sprite_path"]
    writer.writerow(field)

    for idx, row in df.iterrows():
        model_path = get_model(csv_df, idx)
        if model_path != None:
            if "\\Pokemon XY\\" in model_path:
                sprite_path = get_sprite(row["dex_no"])
                writer.writerow([row["dex_no"], row["label"], model_path, sprite_path])
    
