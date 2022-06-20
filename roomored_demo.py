#!/usr/bin/env python3

import os
import json
import pkgutil
import pathlib
import logging

from slideshow.SlideManager import SlideManager


logging.basicConfig()
logger = logging.getLogger("kburns-slideshow")
logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(os.path.dirname(os.path.realpath(__file__)) + '/kburns-slideshow.log')
# handler.setLevel(logging.DEBUG)
# formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
# handler.setFormatter(formatter)
# logger.addHandler(handler)


if __name__ == "__main__":

    config = {}
    with open(os.path.dirname(os.path.realpath(__file__)) + '/config.json') as config_file:
        config = json.load(config_file)

    work_directory_path = pathlib.Path("../temp/kburns")

    config.update({
        "output_width": 1024,
        "output_height": 768,
        "output_codec": "",
        "output_parameters": "",
        "slide_duration": 8,
        "slide_duration_min": 1,
        "fade_duration": 1.0,
        "transition_bars_count": 10,
        "transition_cell_size": 50,
        "fps": 30,
        "overwrite": True,
        "temp_file_folder": str(work_directory_path / "temp"),
        "generate_temp": True
    })

    transitions = [package_name for importer, package_name, _ in pkgutil.iter_modules(["transitions"])]


    input_files = [
        {
            "file": str(input_file_path.absolute()),
            "transition": "fade",
            "overlay_text": {
                "title": f"Image {index}",
                "font": "Helvetica",
                "font_size": 32,
                "duration": 8,
                "offset": 0,
            }
        }
        for index, input_file_path in enumerate(work_directory_path.glob("*.jpeg"))
    ]

    sm = SlideManager(config, input_files, [])

    sm.createVideo(str(work_directory_path / "test.mp4"))
