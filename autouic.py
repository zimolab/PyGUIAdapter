import os
import sys

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "pyguiadapter/ui/generated")
DESIGNER_FILE_DIR = os.path.join(os.path.dirname(__file__), "designer/")

OUTPUT_FILE_PREFIX = "ui_"

CMD = "pyuic6"
DEBUG_FLAG = ""


def make_output_filename(
    path: str, prefix: str = OUTPUT_FILE_PREFIX, suffix: str = ".py"
) -> str:
    basename = os.path.basename(path)
    filename, _ = os.path.splitext(basename)
    return f"{prefix}{filename}{suffix}"


def main():
    for filename in os.listdir(DESIGNER_FILE_DIR):
        if not filename.endswith(".ui"):
            continue
        try:
            input_path = os.path.normpath(os.path.join(DESIGNER_FILE_DIR, filename))
            output_filename = make_output_filename(
                filename, prefix=OUTPUT_FILE_PREFIX, suffix=".py"
            )
            output_path = os.path.normpath(os.path.join(OUTPUT_DIR, output_filename))
            cmd = f"{CMD} {input_path} -o {output_path} {DEBUG_FLAG}"
            print(cmd)
            os.system(cmd)
        except BaseException as e:
            print(e)


if __name__ == "__main__":
    main()
