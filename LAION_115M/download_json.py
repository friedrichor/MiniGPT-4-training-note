import os
import sys
import json
import requests



def LAION_115M_download_json(save_file: str):
    print("connecting...")
    LAION_115M_url = "https://storage.googleapis.com/sfr-vision-language-research/BLIP/datasets/laion_synthetic_filtered_large.json"
    response = requests.get(LAION_115M_url)
    print("have get requests!")
    LAION_115M_data = response.json()
    
    print("Writing to a json file...")
    with open(save_file, 'w', encoding='utf-8') as fout:
        json.dump(LAION_115M_data, fout, indent=4)



if __name__ == "__main__":
    # Download LAION_115M from the url to your local directory
    LAION_115M_file = os.path.join(sys.path[0], 'laion_synthetic_filtered_large.json')
    LAION_115M_download_json(LAION_115M_file)
    
    # View data format
    with open(LAION_115M_file, 'r', encoding='utf-8') as f:
        LAION_115M = json.load(f)
    print(LAION_115M[:5])