import os.path

from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.types import file_t, directory_t
from pyguiadapter.windows import FnExecuteWindowConfig


def encode_mp3(
    input_file: file_t, output_dir: directory_t, output_file: str, quality: int
):
    """
    This function is used to encode a mp3 file into ogg format.

    Note: **The quality parameter will affect the output file size.**

    @params
    [input_file]
    label = "Input MP3 File"
    description = "select the path of the mp3 file you want to encode."
    placeholder = "No input file"
    dialog_title = "Select MP3 File"
    filters = "MP3 Files(*.mp3)"

    [output_dir]
    label = "Output File Directory"
    description = "select the directory of the output file"
    placeholder = "Output directory not specified"
    dialog_title = "Select Output Directory"

    [output_file]
    label = "Output Filename"
    description = "The filename of output file, <b>must endswith .ogg</b>"
    placeholder = "No output filename"

    [quality]
    label = "Encoding Quality"
    default_value = 80
    description = "from 10 to 100, <font color='red'>higher value, better quality, but requires more time to encode</font>"
    min_value = 10
    max_value = 100
    step = 1
    suffix = " %"
    @end
    """
    pass


if __name__ == "__main__":

    fn_doc_path = os.path.join(os.path.dirname(__file__), "fn_doc.html")

    with open(fn_doc_path, "r") as f:
        fn_doc = f.read()

    adapter = GUIAdapter()
    adapter.add(
        encode_mp3,
        document=fn_doc,
        document_format="html",
        window_config=FnExecuteWindowConfig(
            title="Audio Encoder",
            icon="mdi.file-music",
        ),
    )
    adapter.run()
