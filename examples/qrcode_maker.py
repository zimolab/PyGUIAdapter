import os.path

import qrcode

from pyguiadapter.exceptions import ParameterError
from pyguiadapter.adapter import ulogging, GUIAdapter


def make_qrcode(
    text: str,
    box_size: int,
    border: int,
    color: str,
    background: str,
    error_correction: str,
    save_path: str,
    allow_overwrite: bool,
):

    if not text:
        raise ParameterError(
            parameter_name="text", message="text to encode cannot be empty"
        )

    if not save_path or save_path.strip() == "":
        raise ParameterError(
            parameter_name="output_filename", message="output filename cannot be empty"
        )

    if not allow_overwrite and os.path.isfile(save_path):
        ulogging.critical(
            "[Critical] Output file exists, while overwriting it is not allowed!"
        )
        raise ParameterError(
            parameter_name="output_filename",
            message="output filename already exists, please specify another one",
        )

    if error_correction not in ["L", "M", "Q", "H"]:
        raise ParameterError(
            parameter_name="error_correction",
            message="error correction level must be one of L, M, Q, H",
        )

    if box_size <= 0:
        box_size = 10
        ulogging.warning(
            f"[Warning] box size must be > 0, using default value: {box_size}"
        )

    if border < 0:
        border = 1
        ulogging.warning(
            f"[Warning] border size must be >= 0, using default value: {border}"
        )

    if not color or color.strip() == "":
        color = "#000000"
        ulogging.warning(
            f"[Warning] foreground color cannot be empty, using default value: {color}"
        )

    if not background or background.strip() == "":
        background = "#FFFFFF"
        ulogging.warning(
            f"[Warning] background color cannot be empty, using default value: {background}"
        )

        error_corrections = {
            "L": qrcode.constants.ERROR_CORRECT_L,
            "M": qrcode.constants.ERROR_CORRECT_M,
            "Q": qrcode.constants.ERROR_CORRECT_Q,
            "H": qrcode.constants.ERROR_CORRECT_H,
        }

        qr = qrcode.QRCode(
            version=None,
            box_size=box_size,
            border=border,
            error_correction=error_corrections.get(error_correction, "H"),
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color=color, back_color=background)


if __name__ == "__main__":
    adapter = GUIAdapter()
    adapter.add(make_qrcode)
    adapter.run()
