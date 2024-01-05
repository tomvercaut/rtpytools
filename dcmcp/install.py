import PyInstaller.__main__


def run_pyinstaller(path: str):
    """
    Run PyInstaller to convert a Python script into a standalone executable file.

    :param path: The path to the Python script file.
    :return: None

    Example Usage:
    run_pyinstaller('path/to/my_script.py')
    """
    PyInstaller.__main__.run([
        '--hiddenimport=pydicom.encoders.gdcm',
        '--hiddenimport=pydicom.encoders.pylibjpeg',
        '--onefile', path
    ])


if __name__ == "__main__":
    script_path = 'dcmcp.py'
    run_pyinstaller(script_path)
