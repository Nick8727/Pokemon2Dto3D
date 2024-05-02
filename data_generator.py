import os
import pandas as pd
import csv
import shutil
from pathlib import Path

df = pd.read_csv("data_loc.csv", encoding="latin-1")

if not os.path.exists('final_data'):
  os.makedirs('final_data')
if not os.path.exists('final_data/sprites'):
  os.makedirs('final_data/sprites')
if not os.path.exists('final_data/models'):
  os.makedirs('final_data/models')





with open('final_data/data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    field = ["dex_no", "name", "model_path", "sprite_path"]
    writer.writerow(field)

    for _, row in df.iterrows():
        new_path = "final_data/models/{}".format(row["dex_no"])
        shutil.copytree(Path(row["model_path"]).parent, new_path)
        files = os.listdir(new_path)
        for name in files:
            if name.endswith(".FBX"):
               src_path = "{}/{}".format(new_path , name)
               dest_path = "{}/{}.FBX".format(new_path, row["dex_no"])
               os.rename(src_path, dest_path)
               break
        model_path = "final_data/models/{}/{}.FBX".format(row["dex_no"], row["dex_no"])
        
        shutil.copy(row["sprite_path"], "final_data/sprites/{}.png".format(row["dex_no"]))
        sprite_path = "final_data/sprites/{}.png".format(row["dex_no"])

        writer.writerow([row["dex_no"], row["label"], model_path, sprite_path])