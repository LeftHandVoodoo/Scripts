"""
This script connects to a Plex server and gathers information about the movies you have stored there.
It looks at both the 'Movies' and 'Adult' sections in your Plex library.

Here's what it does in detail:

1. Connects to your Plex server using a URL and a token.
2. Fetches the list of movies from both the 'Movies' and 'Adult' sections.
3. For each movie, it gathers various details like the title, release year, runtime, rating, genre, and more.
   It also finds out on which drive the movie is stored and what's its highest resolution.
4. All this data is then organized into a table (DataFrame in Python terms).
5. The script then moves any existing CSV files from a 'Current_List' folder to an 'Old_List' folder.
6. A new CSV file is created in the 'Current_List' folder, containing the table of movie data.
7. Finally, it generates some statistics about your movie collection, like how many movies you have in each rating category and genre. 
   These statistics are saved in another CSV file.

To speed things up, it uses 'multiprocessing' to fetch details of multiple movies at the same time.
"""

from plexapi.server import PlexServer
import pandas as pd
from multiprocessing import freeze_support, Pool
import math
import os
from datetime import datetime
import subprocess

print("Imports loaded")

PLEX_URL = 'http://69.140.114.253:13163'
TOKEN = 'd5MGkJKH31LDHTxG-XqU'

print("Connecting to Plex server...")
plex = PlexServer(PLEX_URL, TOKEN)
print("Connected")

def fetch_section_movies(section_name):
    try:
        section = plex.library.section(section_name)
        movies = section.all()
        return movies
    except Exception as e:
        error_message = f"Error getting Plex {section_name} section: {e}"
        print(error_message)
        return []

print("Getting Movies section...")
all_movies = fetch_section_movies('Movies')

print("Getting Adult section...")
adult_movies = fetch_section_movies('Adult')

# Merge all_movies and adult_movies
all_movies.extend(adult_movies)

movie_titles = [movie.title for movie in all_movies]
print(f"Total movies: {len(movie_titles)}")

def map_resolution(resolution):
    width, height = map(int, resolution.split('x'))
    print(f"width: {width}, height: {height}")
    
    if width >= 3840 and height >= 2160:
        print("Resolution: 4K")
        return '4K'
    elif width >= 2560 and height >= 1440:
        print("Resolution: 2K")
        return '2K'
    elif width >= 1920 and height >= 1080:
        print("Resolution: 1080p")
        return '1080p'
    elif width >= 1280 and height >= 720:
        print("Resolution: 720p")
        return '720p'
    else:
        print("Resolution: SD")
        return 'SD'

import subprocess

import subprocess

import subprocess

def get_highest_resolution(file_path):
    try:
        command = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'csv=p=0',
            file_path
        ]
        result = subprocess.check_output(command, encoding='utf-8')
        output = result.strip()
        print(f"Output: {output}")  # Added print statement for debugging
        return map_resolution(output)
    except subprocess.CalledProcessError as e:
        print(f"Error getting resolution: {e}")
        return 'N/A'

get_highest_resolution("path/to/file.mp4")  # Added example usage for debugging

import os

def get_movie_metadata(title):
    try:
        movie = plex.library.section('Movies').get(title)
        runtime_minutes = math.ceil(movie.duration / 60000)
        drive_letter, full_path = os.path.splitdrive(movie.media[0].parts[0].file)
        drive_letter = drive_letter.upper()
        highest_resolution = get_highest_resolution(full_path)

        metadata = {
            'Title': movie.title,
            'Year': movie.year,
            'Runtime': f"{runtime_minutes} minutes",
            'Rating': movie.contentRating,
            'Genre': movie.genres[0].tag if movie.genres else '',
            'Drive Letter': drive_letter,
            'Highest Resolution': highest_resolution,
            'Full Path': full_path
        }

        print(f"Metadata for movie {title}: {metadata}")
        return metadata
    except Exception as e:
        print(f"Error getting metadata for movie {title}: {e}")
        return None

import pandas as pd
from datetime import datetime
import os

import pandas as pd
import os
from datetime import datetime

import pandas as pd
from datetime import datetime
import os

def generate_movie_stats(df):
    rating_columns = ['X', 'NC-17', 'R', 'NR', 'PG-13', 'PG', 'G']
    rating_count = {rating: 0 for rating in rating_columns}
    rating_count['Other'] = 0
    genre_count = {}
    
    for _, row in df.iterrows():
        rating = row['Rating']
        genre = row['Genre']
        
        if pd.notnull(rating):
            if rating in rating_columns:
                rating_count[rating] += 1
            else:
                rating_count['Other'] += 1

        if pd.notnull(genre):
            genre_count[genre] = genre_count.get(genre, 0) + 1
    
    stats_data = {
        'Total Movies': [len(df)],
        **rating_count,
        **genre_count
    }
    
    stats_df = pd.DataFrame(stats_data)
    stats_file_path = r'C:\Users\bax11\OneDrive\Desktop\Script_Tasks\Stats\Movie_Stats.csv'
    
    if os.path.exists(stats_file_path):
        existing_df = pd.read_csv(stats_file_path)
        new_row = pd.DataFrame(stats_data)
        new_row['Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        updated_df = pd.concat([existing_df, new_row], ignore_index=True)
        updated_df.to_csv(stats_file_path, index=False)
    else:
        stats_df['Date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        stats_df.to_csv(stats_file_path, index=False)
    
    print(f"Movie stats saved to {stats_file_path}")

if __name__ == '__main__':
    print("Initializing multiprocessing...")
    freeze_support()

    print("Creating multiprocessing pool...")
    pool = Pool(processes=32)
    print("Pool created")

    print("Extracting metadata in parallel...")
    try:
        movies_data = pool.map(get_movie_metadata, movie_titles)
        movies_data = [data for data in movies_data if data is not None]
        print("Metadata extracted")
    except Exception as e:
        print(f"Error extracting movie metadata: {e}")
        exit()

    print("Creating DataFrame...")
    df = pd.DataFrame(movies_data)
    print("DataFrame created")

    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    existing_csv_files = os.listdir(r'C:\Users\bax11\OneDrive\Desktop\Script_Tasks\Current_List')
    for csv_file in existing_csv_files:
        if csv_file.endswith('.csv'):
            src_path = os.path.join(r'C:\Users\bax11\OneDrive\Desktop\Script_Tasks\Current_List', csv_file)
            dest_path = os.path.join(r'C:\Users\bax11\OneDrive\Desktop\Script_Tasks\Old_List', csv_file)
            try:
                os.rename(src_path, dest_path)
                print(f"Moved existing file: {csv_file}")
            except Exception as e:
                print(f"Error moving existing file: {e}")

    output_file_path = rf'C:\Users\bax11\OneDrive\Desktop\Script_Tasks\Current_List\Plex_Movie_List_as_of_{current_datetime}.csv'

    print("Writing to CSV...")
    try:
        df.to_csv(output_file_path, index=False)
        print("CSV file saved successfully")
    except Exception as e:
        print(f"Error exporting to CSV: {e}")

    generate_movie_stats(df)

    print("Plex movie metadata and stats exported successfully")
