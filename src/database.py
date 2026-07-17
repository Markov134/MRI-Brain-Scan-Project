import sqlite3
import os
from PIL import Image

# ----------------------------
# NOTE: Make sure to close the database connection after using these functions.
# ----------------------------

DATASET_PATH = 'data/raw/Brain-Tumor-MRI-Dataset'
DATABASE_PATH = 'data/database/mri_dataset.db'

def connect_db():
    # Makes a database if there isnt one already
    return sqlite3.connect(DATABASE_PATH)

def create_tables(conn):

    # A Cursor is an object used to execute SQL queries on an SQLite database
    cursor = conn.cursor()

    # Creates table inside the database
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

def populate_database(conn):

    cursor = conn.cursor()

    # Prevents duplicates by checking if the database is populated
    cursor.execute("SELECT COUNT(*) FROM mri_images")

    if cursor.fetchone()[0] > 0:
        print("Database already populated.")
        return
    
    # This goes through the dataset and assigns the values inside the database
    for split in os.listdir(DATASET_PATH):
        split_folder = os.path.join(DATASET_PATH, split)

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

                    # Inserts values into the columns of the mri_images table
                    cursor.execute("""INSERT INTO mri_images (
                        filename, 
                        filepath, 
                        diagnosis, 
                        split, 
                        width, 
                        height, 
                        filesize
                        ) 
                        VALUES (?, ?, ?, ?, ?, ?, ?)""", (
                            filename,
                            filepath,
                            diagnosis,
                            split,
                            width,
                            height,
                            filesize
                            )
                        )

    conn.commit()







