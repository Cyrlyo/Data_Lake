import kaggle
from kaggle.api.kaggle_api_extended import KaggleApi
import os, subprocess

KAGGLE_CONFIG_DIR = os.path.join(os.path.expandvars('$HOME'), '.kaggle')
cmd = f"chmod 600 {KAGGLE_CONFIG_DIR}/kaggle.json"
output = subprocess.check_output(cmd.split(" "))
output = output.decode(encoding='UTF-8')
print(output)


print("coucou1")
api = KaggleApi()
api.authenticate()
print("coucou2")
api.dataset_download_file("shmalex/instagram-dataset",
                          file_name="instagram_locations.csv")
print("coucou3")