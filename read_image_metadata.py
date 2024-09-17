import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter
import piexif
from PIL import Image
from tabulate import tabulate

# allows Pillow to open and manipulate images in the HEIF (i.e. HEIC) format
from pillow_heif import register_heif_opener
register_heif_opener()

def extract_metadata(dir_path):
    """
    Extracts metadata from all the image files in the specified directory and
    returns it as a pandas dataframe.

    Args:
        dir_path (str): The path to the directory containing the image files.

    Returns:
        pandas.DataFrame: A dataframe containing the metadata of all the image files.
    """
    metadata_list = []
    print(len(os.listdir(dir_path)))
    for file in os.listdir(dir_path):
        file = file.lower()
        print("[+] Processing {}".format(file))
        if (file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".png") or file.endswith(".tiff")
                or file.endswith(".bmp") or file.endswith(".gif") or file.endswith(".webp") or file.endswith(".psd")
                or file.endswith(".raw") or file.endswith(".cr2") or file.endswith(".nef") or file.endswith(".heic")
                or file.endswith(".sr2")):
            print("[+] Extracting metadata from {}".format(file))

            with Image.open(os.path.join(dir_path, file)) as img:
                exif_data = piexif.load(img.info["exif"])
                print("[+] Metadata extracted from {}".format(file))

                metadata = {}

                try:
                    metadata['filename'] = file
                except:
                    metadata['filename'] = None

                try:
                    metadata['datetime'] = exif_data['0th'][piexif.ImageIFD.DateTime].decode('utf-8')
                except:
                    metadata['datetime'] = None

                try:
                    metadata['make'] = exif_data['0th'][piexif.ImageIFD.Make].decode('utf-8').strip()
                except:
                    metadata['make'] = None

                try:
                    metadata['model'] = exif_data['0th'][piexif.ImageIFD.Model].decode('utf-8').strip()
                except:
                    metadata['model'] = None

                try:
                    f_number = tuple(exif_data['Exif'][piexif.ExifIFD.FNumber])
                    metadata['f_number'] = f_number[0] / f_number[1]
                except:
                    metadata['f_number'] = None

                try:
                    metadata['iso_speed_ratings'] = exif_data['Exif'][piexif.ExifIFD.ISOSpeedRatings]
                except:
                    metadata['iso_speed_ratings'] = None

                try:
                    focal_length = tuple(exif_data['Exif'][piexif.ExifIFD.FocalLength])
                    metadata['focal_length'] = focal_length[0] / focal_length[1]
                except:
                    metadata['focal_length'] = None

                try:
                    exposure_time = tuple(exif_data['Exif'][piexif.ExifIFD.ExposureTime])
                    metadata['exposure_time (1/)'] = exposure_time[1] / exposure_time[0]
                except:
                    metadata['exposure_time'] = None

                print("-----------------------------")

                metadata_list.append(metadata)

    # Convert the metadata list to a pandas dataframe
    metadata_df = pd.DataFrame(metadata_list)

    return metadata_df

def charting(df):
    """
    Generates and saves histogram distributions for F-Number, ISO, Focal Length and Exposure Time for all camera models
    in the metadata dataframe.

    Args:
        df: The pandas DataFrame containing the extracted metadata of all the image files.
    """
    models = np.unique(df['model'])

    for model in models:
        dfm = df[df['model'] == model]

        plt.hist(dfm['f_number'], bins=20)
        plt.title('{} F-Number Distribution'.format(model))
        plt.savefig('{} F-Number Distribution'.format(model))
        plt.clf()

        plt.hist(dfm['iso_speed_ratings'], bins=40)
        plt.title('{} ISO Distribution'.format(model))
        plt.savefig('{} ISO Distribution'.format(model))
        plt.clf()

        plt.hist(dfm['focal_length'], bins=40)
        plt.title('{} Focal Length Distribution'.format(model))
        plt.savefig('{} Focal Length Distribution'.format(model))
        plt.clf()

        plt.hist(dfm['exposure_time (1/)'], bins=40)
        plt.title('{} Exposure Time (1/T) Distribution'.format(model))
        plt.savefig('{} Exposure Time Distribution'.format(model))
        plt.clf()

if __name__ == "__main__":
    # Define the directory containing the image files
    dir_path = 'C:\\Users\snd21\Pictures\ALL_PHOTOS'
    # Extract the metadata from the image files
    metadata_df = extract_metadata(dir_path)
    print("[+] Metadata extracted from all image files")
    print(metadata_df.columns)

    # Print the dataframe
    print(tabulate(metadata_df, headers="keys", tablefmt="psql"))
    metadata_df.to_csv('metadata.csv')

    # Run charts
    charting(metadata_df)

