import os

class CurrentDirectory:
    def get_curr_dir(script_path: str):
        script_dir = os.path.dirname(os.path.abspath(script_path))
        curr_dir = script_dir.replace('\\', '/')
        return curr_dir