import os
import re

if __name__ == '__main__':
    path = os.path.abspath(os.path.dirname(__file__))
    out_dir = os.path.join(path, "out")
    os.makedirs(out_dir, exist_ok=True)
    filename_pattern = r"^.*_(.+\.svg)$"
    for dirpath, _, filenames in os.walk(path):
        for filename in filenames:
            if not filename.endswith(".svg"):
                continue
            new_filename = re.sub(filename_pattern, r"\1", filename)
            new_filepath = os.path.join(out_dir, new_filename)
            os.rename(os.path.join(dirpath, filename), new_filepath)