import argparse
import os
import time
from os import PathLike
from pathlib import Path
from typing import List, AnyStr, LiteralString

from pydicom import dcmread


class Data:
    """
    Class for storing data related to a patient's medical information.

    Attributes:
        path (Path | None): The path to the data file. Defaults to None.
        patient_name (str | None): The name of the patient. Defaults to None.
        patient_id (str | None): The ID of the patient. Defaults to None.
        plan_name (str | None): The name of the medical plan. Defaults to None.
        plan_label (str | None): The label of the medical plan. Defaults to None.
    """
    def __init__(self):
        self.path: Path | None = None
        self.patient_name: str | None = None
        self.patient_id: str | None = None
        self.plan_name: str | None = None
        self.plan_label: str | None = None


class DataFormatter:
    """
    :class:`DataFormatter` class provides methods to format and display data in a tabular format.

    The class has the following internal attributes:

        - `_column_names` : dict
            A dictionary that maps each column name to its corresponding header name.

        - `_widths` : dict
            A dictionary that maps each column name to its width.

        - `_line` : str
            A string representing a horizontal line.

    The class provides the following methods:

        - `__init__` method initializes the `_column_names`, `_widths`, and `_line` attributes.

        - `set_width_path` method sets the width of the 'path' column.

        - `set_widths` method sets the widths of all data columns based on the maximum length of data elements.

        - `header` method generates the header string for the columns.

        - `value` method formats the given data into a string.

        - `values` method returns a string representation of the values of the data.

        - `hline` method draws a horizontal line.

    Example usage:

    ```python
    formatter = DataFormatter()
    formatter.set_width_path(50)
    formatter.set_widths(datas)
    header = formatter.header()
    formatted_values = formatter.values(datas)
    line = formatter.hline()
    ```
    """

    def __init__(self):
        self._column_names = {'path': 'File path', 'patient_id': 'patient ID', 'patient_name': 'patient name',
                              'plan_name': 'plan name', 'plan_label': 'plan label'}
        self._widths = {'path': 40, 'patient_id': 15, 'patient_name': 25, 'plan_name': 25, 'plan_label': 25}
        self._line = ""
        assert (len(self._column_names) == len(self._widths))
        assert (self._column_names.keys() == self._widths.keys())

    def set_width_path(self, width: int):
        self._widths['path'] = width

    def set_widths(self, datas: List[Data]):
        """
        Set the widths of the different data columns based on the maximum length of data elements.

        :param datas: List of Data instances.
        :type datas: List[Data]
        """
        for data in datas:
            n = len(data.patient_id)
            if n >= self._widths['patient_id']:
                self._widths['patient_id'] = n
            n = len(data.patient_name)
            if n >= self._widths['patient_name']:
                self._widths['patient_name'] = n
            n = len(data.plan_name)
            if n >= self._widths['plan_name']:
                self._widths['plan_name'] = n
            n = len(data.plan_label)
            if n >= self._widths['plan_label']:
                self._widths['plan_label'] = n

    def header(self) -> str:
        """
        Generate the header string for the given columns.

        :return: The formatted header string.
        :rtype: str
        """
        ls = []
        for key in self._column_names.keys():
            ls.append(f"| {self._column_names[key]:<{self._widths[key]}}")
        ls.append('|')
        s = " ".join(f"{s}" for s in ls)
        n = len(s)
        self._line = '-' * n
        return f'{self._line}\n{s}\n{self._line}'

    def value(self, data: Data) -> str:
        """
        Formats the given data into a string.

        :param data: The data to be formatted.
        :type data: Data
        :return: The formatted string.
        :rtype: str
        """
        try:
            p = str(data.path)
            n = len(p)
            if n >= self._widths['path']:
                t = p[-self._widths['path'] + 3:]
                p = f'...{t}'
            s = f'| {p:<{self._widths['path']}} |'
            s += f' {data.patient_id:<{self._widths['patient_id']}} |'
            s += f' {str(data.patient_name):<{self._widths['patient_name']}} |'
            s += f' {data.plan_name:<{self._widths['plan_name']}} |'
            s += f' {data.plan_label:<{self._widths['plan_label']}} |'
            return s
        except Exception as ex:
            print(f"{ex}")

    def values(self, datas: List[Data]) -> str:
        """
        Return a string representation of the values of the data.

        :param datas: A list of Data objects.
        :return: A string representing the values of the data, separated by newline.
        """
        return '\n'.join([self.value(data) for data in datas])

    def hline(self) -> str:
        """
        Draws a horizontal line.

        :return: The horizontal line represented as a string.
        """
        return self._line


def list_files_with_prefix(directory: PathLike | AnyStr | LiteralString,
                           prefix: str = '', sort: bool = True) -> List[PathLike | AnyStr | LiteralString | bytes]:
    """
    Retrieves a list of file paths that match the specified prefix in the given directory.

    :param directory: The directory path in which to search for files.
    :param prefix: The prefix used to filter files. Only files that start with this prefix will be included.
    :param sort: A boolean value indicating whether to sort the file paths by modification time in descending order.
    :return: A list of file paths that match the specified prefix.
    """
    lf = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.startswith(prefix):
                file_path = os.path.join(root, file)
                timestamp = os.path.getmtime(file_path)
                readable_timestamp = time.ctime(timestamp)
                lf.append((timestamp, readable_timestamp, file_path))
    if sort:
        lf.sort(key=lambda x: x[0], reverse=True)
    return [file_path for timestamp, readable_timestamp, file_path in lf]


def read_rtplans(paths: List[Path]) -> List[Data]:
    """
    :param paths: a list of paths to DICOM files
    :return: a list of Data objects containing information extracted from the DICOM files

    This method takes in a list of file paths to DICOM files.
    It reads each file using the dcmread function from the pydicom library.
    If the file is a RTPLAN, it creates a Data object and assigns
    * the following attributes:
    - path: the file path
    - patient_name: the PatientName attribute from the DICOM file
    - patient_id: the PatientID attribute from the DICOM file
    - plan_name: the RTPlanName attribute from the DICOM file
    - plan_label: the RTPlanLabel attribute from the DICOM file

    The method returns a list of all the created Data objects, representing the extracted information from the
    DICOM files.
    """
    ld = []
    for path in paths:
        with dcmread(path) as fd:
            if fd.Modality != 'RTPLAN':
                continue
            data = Data()
            data.path = path
            data.patient_name = fd.PatientName
            data.patient_id = fd.PatientID
            if 'RTPlanName' in fd:
                # data.plan_name = fd['RTPlanName']
                data.plan_name = fd.RTPlanName
            else:
                data.plan_name = ""
            if 'RTPlanLabel' in fd:
                data.plan_label = fd.RTPlanLabel
            else:
                data.plan_label = ""
            ld.append(data)
    return ld


def ls_rtplan(path: PathLike | LiteralString | AnyStr | bytes, prefix: str, limit: int, sort: bool = True) -> (
        List)[Data]:
    """
    List paths to RT plans matching the given prefix, up to the specified limit.

    :param path: The directory path to search for RT plans.
    :param prefix: The prefix to match RT plan filenames with. If empty all RTPLAN files are returned.
    :param limit: The maximum number of paths to return. If the limit is zero or negative,
                  all matching paths will be returned.
    :param sort: Optional argument to specify whether to sort the file paths by modification time in descending order.
    :return: A list of data objects representing the paths to RT plans.
    :raises IOError: If the input path does not exist or is not a directory.
    """
    if not Path(path).is_dir():
        raise IOError("Input path does not exist or is not a directory.")

    paths = list_files_with_prefix(path, prefix, sort)
    if limit > 0:
        del paths[limit:]
    return read_rtplans(paths)


def print_ls_rtplan(path: PathLike | LiteralString | AnyStr | bytes, prefix: str, limit: int,
                    sort: bool = True) -> None:
    """
    Print the directory listing with specific prefix in a formatted way.

    :param path: The directory path to search for RT plans.
    :param prefix: The prefix to match RT plan filenames with. If empty all RTPLAN files are returned.
    :param limit: The number of files to limit the output to.
    :param sort: Flag indicating whether to sort the files by modification time in descending order.
    :return: None
    """
    datas = ls_rtplan(path, prefix, limit, sort)
    fmt = DataFormatter()
    fmt.set_widths(datas)
    print(f"{fmt.header()}")
    print(f"{fmt.values(datas)}")
    print(f'{fmt.hline()}')


def main():
    parser = argparse.ArgumentParser(
        prog="ls_rtplan",
        description="Print an overview of the RTPLANs in a directory.")
    parser.add_argument('-d', '--dir', default='.', help="Path to the directory.")
    parser.add_argument('-p', '--prefix', default='', help="Prefix of the RTPLAN files.")
    parser.add_argument('-l', '--limit', default=0, help="Limit the number of RTPLANs to list.")
    # parser.add_argument('-s', '--sort', default=True, action='store_true',
    #                     help="Sort the RTPLANS based on the last modified timestamp in descending order.")
    args = parser.parse_args()

    print_ls_rtplan(args.dir, args.prefix, int(args.limit), True)


if __name__ == "__main__":
    main()
