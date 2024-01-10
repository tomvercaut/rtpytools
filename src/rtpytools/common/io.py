import os
from pathlib import Path
from typing import List


def ls(p: Path) -> List[str]:
    """
    List all files in the given directory and its subdirectories.

    :param p: The path to the directory.
    :type p: Path object
    :return: A list of paths to all the files found.
    :rtype: List[Path]
    :raises IOError: If the input directory does not exist.
    """
    if not p.exists():
        raise IOError(f"Input directory does not exist: {p}")
    lf = []
    for root, dirs, files in os.walk(p):
        for file in files:
            lf.append(os.path.join(root, file))
    return lf
