from pathlib import Path

current_working_directory = (
    Path()
)  # current working directory, i.e., where Python was launched from
script_path = Path(__file__)  # full path to this script
script_dir = script_path.parent  # folder containing the script

print(f"current_working_directory = {current_working_directory.resolve()}")
print(f"script_path = {script_path.resolve()}")
print(f"script_dir = {script_dir.resolve()}")
