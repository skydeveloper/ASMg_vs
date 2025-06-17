# make_archive.py
import shutil
import os
from datetime import datetime

project_dir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.dirname(project_dir)
now = datetime.now().strftime("%Y%m%d_%H%M%S")
archive_name = os.path.join(parent_dir, f"ASMg_{now}")

shutil.make_archive(archive_name, 'zip', project_dir)
print(f"Архивът е създаден: {archive_name}.zip")