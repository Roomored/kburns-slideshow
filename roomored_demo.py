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
        "output_width": 1280,
        "output_height": 800,
        "output_codec": "libx264",
        "output_parameters": "-preset veryslow -tune stillimage -qp 20",
        "slide_duration": 5,
        "slide_duration_min": 1,
        "fade_duration": 1.0,
        "transition_bars_count": 10,
        "transition_cell_size": 50,
        "fps": 30,
        "overwrite": True,
        "temp_file_folder": str(work_directory_path / "temp"),
        "generate_temp": True,
    })

    transitions = [package_name for importer, package_name, _ in pkgutil.iter_modules(["transitions"])]

    input_files = []

    for room_folder in sorted(
        (work_directory_path / "script").iterdir(),
        key=lambda path: path.name
    ):
        if not room_folder.is_dir():
            continue

        room_name = room_folder.name.split(" - ")[1]

        title_shown = False

        for camera_folder in sorted(
            room_folder.iterdir(),
            key=lambda path: path.name
        ):

            if not camera_folder.is_dir():
                continue

            image_file = list(camera_folder.iterdir())[0]

            spec = {
                "file": str(image_file.absolute()),
                "transition": "fade"
            }

            if not title_shown:
                title_shown = True
                spec["overlay_text"] = {
                    "title": room_name,
                    "font": "Helvetica",
                    "font_size": 32,
                    "duration": 5,
                }

            input_files.append(spec)

    sm = SlideManager(config, input_files, [ str(work_directory_path / "174_full_out-in-the-open-no-vocal-version_0151.mp3") ])

    sm.createVideo(str(work_directory_path / "test.mp4"))
