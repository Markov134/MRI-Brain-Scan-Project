import sqlite3
import os
from PIL import Image

dataset_path = 'data/raw/Brain-Tumor-MRI-Dataset'

def connect_db():
    # Makes a database if there isnt one already
    return sqlite3.connect('data/database/mri_dataset.db')

def create_tables(conn):

    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS mri_images (
        id INTEGER PRIMARY KEY,
        filename TEXT NOT NULL,
        filepath TEXT NOT NULL,
        diagnosis TEXT NOT NULL,
        split TEXT NOT NULL,
        width INTEGER,
        height INTEGER,
        filesize INTEGER
        )"""
    )

    conn.commit()

    conn.close()

def populate_database(conn):

    cursor = conn.cursor()
    
    for split in os.listdir(dataset_path):
        split_folder = os.path.join(dataset_path, split)

        if not os.path.isdir(split_folder):
            continue

        for diagnosis in os.listdir(split_folder):
            class_folder = os.path.join(split_folder, diagnosis)

            if not os.path.isdir(class_folder):
                continue

            for filename in os.listdir(class_folder):

                if filename.lower().endswith(".jpg"):
                    filepath = os.path.join(class_folder, filename)

                    with Image.open(filepath) as img:
                        width, height = img.size

                    filesize = os.path.getsize(filepath)

                    cursor.execute("""INSERT INTO mri_images (
                        filename, 
                        filepath, 
                        diagnosis, 
                        split, 
                        width, 
                        height, 
                        filesize) VALUES (?, ?, ?, ?, ?, ?, ?)""", (
                            filename,
                            filepath,
                            diagnosis,
                            split,
                            width,
                            height,
                            filesize)
                        )

    conn.commit()
    conn.close()







