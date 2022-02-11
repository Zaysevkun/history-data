import json
import os
from json import JSONDecodeError

from errors import InvalidJsonError

SAMPLES_FOLDER = 'samples'


def read_json_from_file(file_path: str) -> dict:
    with open(
        os.path.join(
            SAMPLES_FOLDER,
            f'{file_path}.json'
        )
    ) as file:
        try:
            return json.load(file)
        except JSONDecodeError:
            raise InvalidJsonError('oops, something went wrong(json is not valid)')
