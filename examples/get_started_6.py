from pyguiadapter.adapter import GUIAdapter
from pyguiadapter.types import file_t, directory_t
from pyguiadapter.widgets import (
    FileSelectConfig,
    DirSelectConfig,
    LineEditConfig,
    IntSpinBoxConfig,
)


def encode_mp3(
    input_file: file_t, output_dir: directory_t, output_file: str, quality: int
):
    """
    encode_mp3
    @param input_file: select the path of the mp3 file you want to encode.
    @param output_dir: select the directory of the output file
    @param output_file: The filename of output file, <b>must endswith .ogg</b>
    @param quality: from 10 to 100, <font color='red'>higher value, better quality, but requires more time to encode</font>
    @return:
    """
    pass


if __name__ == "__main__":

    adapter = GUIAdapter()
    adapter.add(
        encode_mp3,
        widget_configs={
            "input_file": FileSelectConfig(
                label="Input MP3 File",
                placeholder="No input file",
                dialog_title="Select MP3 File",
                filters="MP3 Files(*.mp3)",
            ),
            "output_dir": DirSelectConfig(
                label="Output File Directory",
                placeholder="Output directory not specified",
                dialog_title="Select Output Directory",
            ),
            "output_file": LineEditConfig(
                label="Output Filename", placeholder="No output filename"
            ),
            "quality": IntSpinBoxConfig(
                label="Encoding Quality",
                default_value=80,
                min_value=10,
                max_value=100,
                step=1,
                suffix=" %",
            ),
        },
    )
    adapter.run()
