import argparse
import shutil
from pathlib import Path

from pydicom import dcmread
from pydicom.errors import InvalidDicomError

from rtpytools.common.io import ls


def dcm_copy_file(src: Path, dest: Path, patient_id: str, verbose: bool = False):
    """
    Copy DICOM file from source to destination if the file's PatientID matches the provided patient_id.

    :param src: Path to the source DICOM file.
    :param dest: Path to the destination directory where the copied file will be saved.
    :param patient_id: Patient ID to match with the PatientID attribute in the source DICOM file.
    :param verbose: If true, print if the file is being copied or if an error occurs
    :return: None
    """
    try:
        with dcmread(src, stop_before_pixels=True, force=True) as fd:
            if 'PatientID' in fd and fd.PatientID == patient_id:
                if verbose:
                    print(f"Copying {src} to {dest}")
                shutil.copy2(src, dest)
    except (InvalidDicomError, TypeError) as e:
        if verbose:
            print(f"{e}")


def dcm_copy_files(src: str, dest: str, patient_id: str, verbose: bool = False):
    """
    Copy DICOM files from the input directory to the output directory for a specific patient.

    :param src: The input directory where the DICOM files are located.
    :param dest: The output directory where the copied DICOM files would be saved.
    :param patient_id: The ID of the patient for whom the DICOM files are being copied.
    :param verbose: If true, print which files are copied
    :raises IOError: If the output directory does not exist.
    :raises Exception: If the patient ID is not provided.
    :return: None
    """
    pdest = Path(dest)
    if not pdest.exists():
        raise IOError(f"Output directory does not exist: {pdest}")
    if not patient_id:
        raise Exception(f"Patient ID is not provided.")

    lf = ls(Path(src))
    for f in lf:
        dcm_copy_file(Path(f), pdest, patient_id, verbose)


def main():
    parser = argparse.ArgumentParser(prog="dcmcp",
                                     description="Copy DICOM files for a specific patient from "
                                                 "one directory to another.")
    parser.add_argument("-i", "--input", required=True, help="Input directory")
    parser.add_argument("-o", "--output", required=True, help="Output directory")
    parser.add_argument("--id", required=True, help="Patient ID")
    parser.add_argument("-v", "--verbose", action='store_true', help="Output directory")
    args = parser.parse_args()

    dcm_copy_files(args.input, args.output, args.id, args.verbose)


if __name__ == "__main__":
    main()
