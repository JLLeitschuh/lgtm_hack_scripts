from typing import List
import os

def create_cache_folder():
    if not os.path.exists('cache'):
        os.makedirs('cache')

def write_project_ids_to_file(project_ids: List[str], file_name: str):
    create_cache_folder()

    file = open("cache/" + file_name + ".txt", "a")

    for project_id in project_ids:
        file.write(project_id + "\n")

    file.close()
