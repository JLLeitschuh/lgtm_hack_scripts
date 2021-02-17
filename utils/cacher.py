from typing import List

def write_project_ids_to_file(project_ids: List[str], file_name: str):
    file = open("cache/" + file_name + ".txt", "a")
    for project_id in project_ids:
        file.write(project_id + "\n")
    file.close()
