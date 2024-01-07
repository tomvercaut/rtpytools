import json
from typing import List, Dict

import pandas as pd
from pandas import DataFrame


class Dvh:
    """
    Dvh class represents a Dose-Volume Histogram.
    It stores volume and dose data in a DataFrame and provides methods for manipulating and analyzing the data.

    Example Usage:
        dvh = Dvh()
        dvh.name = "Example Dvh"
        dvh.volume = 200.0
        dvh.add(100.0, 50.0)
        dvh.add(50.0, 70.0)
        dvh.add(20.0, 90.0)
        dvh.sort()
        print(dvh)
    """
    name: str
    volume: float
    _sorted: bool
    data: DataFrame

    def __init__(self):
        self.name = ""
        self.volume = 0.0
        self._sorted = False
        self.data = pd.DataFrame(columns=["Volume", "Dose"])

    def add(self, volume: float, dose: float):
        """
        Add a new volume, dose entry to the DVH.

        :param volume: The volume value for the new entry.
        :param dose: The dose value for the new entry.
        :return: None
        """
        self._sorted = False
        self.data.loc[self.data.shape[0]] = [volume, dose]

    @property
    def is_sorted(self):
        """
        Returns if the data is sorted by volume.

        :return: True if the object is sorted, False otherwise.
        :rtype: bool
        """
        return self._sorted

    def sort(self, ascending: bool = True):
        """
        Sorts the DVH data by volume.

        :param ascending: Specifies whether the data should be sorted in ascending order (default is True).
        :return: None
        """
        self.data.sort_values(by="Volume", ascending=ascending, inplace=True)
        self._sorted = True

    def get(self, index: int) -> [float, float]:
        """
        Returns the data at the given index.

        :param index: The index of the data.
        :type index: int
        :return: A list representing the data (volume, dose)  at the given index.
        :rtype: list[float, float]
        """
        return self.data.iloc[index].tolist()

    def get_volume(self, index: int) -> float:
        """
        Get the volume value for a given index.

        :param index: The index of the data row.
        :type index: int
        :return: The volume value associated with the given index.
        :rtype: float
        """
        return self.data.iloc[index]['Volume']

    def get_dose(self, index: int) -> float:
        """Get the dose value for a given index.

        :param index: The index of the data element.
        :type index: int
        :return: The dose value for the given index.
        :rtype: float

        """
        return self.data.iloc[index]['Dose']

    def size(self):
        return self.data.shape[0]

    def dx(self, volume: float, is_volume_absolute: bool = False) -> float | None:
        """
        :param volume: The volume of interest.
        :param is_volume_absolute: Optional. Specifies whether the volume is absolute
                                   (in the same unit as the volume data in the dataset)
                                   or relative (as a percentage of the total volume in the dataset). Default is False.
        :return: The corresponding dose value for the given volume.
                 Returns None if the dataset has fewer than 2 rows and the volume is not found in the dataset.
        """
        if not self.is_sorted:
            self.sort()
        if not is_volume_absolute:
            if volume in self.data["Volume"].values:
                return self.data.loc[self.data["Volume"] == volume, "Dose"].values[0]
            else:
                if self.data.shape[0] < 2:
                    return None
                for i in range(self.data.shape[0] - 1):
                    r0 = self.data.iloc[i]
                    r1 = self.data.iloc[i + 1]
                    if r0["Volume"] <= volume <= r1["Volume"]:
                        dose_diff = r1["Dose"] - r0["Dose"]
                        volume_diff = r1["Volume"] - r0["Volume"]
                        dose_per_volume = dose_diff / volume_diff
                        dose = r0["Dose"] + dose_per_volume * (volume - r0["Volume"])
                        return dose
                return None
        else:
            rel_volume = volume / self.volume * 100.0
            return self.dx(rel_volume, is_volume_absolute=False)

    def vx(self, dose: float) -> float | None:
        """
        Find the volume corresponding to a given dose.

        :param dose: The dose value for which to find the corresponding volume.
        :return: The volume corresponding to the given dose, or None if no matching dose is found.
        """
        if not self.is_sorted:
            self.sort()
        if dose in self.data["Dose"].values:
            return self.data.loc[self.data["Dose"] == dose, "Volume"].values[0]
        else:
            if self.data.shape[0] < 2:
                return None
            for i in range(self.size() - 1):
                r0 = self.data.iloc[i]
                r1 = self.data.iloc[i + 1]
                if r1["Dose"] <= dose <= r0["Dose"]:
                    dose_diff = r1["Dose"] - r0["Dose"]
                    volume_diff = r1["Volume"] - r0["Volume"]
                    volume_per_dose = volume_diff / dose_diff
                    volume = r0["Volume"] + volume_per_dose * (dose - r0["Dose"])
                    return volume
            return None

    @classmethod
    def from_dict(cls, data: Dict) -> 'Dvh':
        try:
            dvh = cls()
            dvh.name = data["name"]
            dvh.volume = data["volume"]
            for entry in data["data"]:
                dvh.add(entry["volume"], entry["dose"])
            return dvh
        except KeyError as e:
            raise Exception(f"Invalid key in dictionary: {e}")

    def __str__(self):
        return (f"Name: {self.name},\n"
                f"Volume: {self.volume},\n"
                f"Sorted: {self._sorted},\n"
                f"Data:\n{self.data}\n"
                )


def read_json(filename: str) -> List[Dvh]:
    """
    Reads a JSON file and converts it into a list of Dvh objects.

    :param filename: The name of the JSON file to be read.
    :return: A list of Dvh objects populated with data from the JSON file.
    :rtype: List[Dvh]
    """
    with open(filename, 'r') as f:
        data = json.load(f)
        return parse_json_str(data)


def parse_json_str(list_dvh_dicts: List[Dict]) -> List[Dvh]:
    """
    Parse a JSON string and convert it into a list of Dvh objects.

    :param list_dvh_dicts: A list of dictionaries representing the JSON data.
    :type list_dvh_dicts: List[Dict]
    :return: A list of Dvh objects.
    :rtype: List[Dvh]
    """
    # ld = None
    dvhs = []
    if isinstance(list_dvh_dicts, dict):
        ld = [list_dvh_dicts]
    elif isinstance(list_dvh_dicts, list):
        ld = list_dvh_dicts
    else:
        raise ValueError("Function argument must be of type: Dict or List. Got type {}".format(type(list_dvh_dicts)))
    for dvh_data in ld:
        dvh = Dvh.from_dict(dvh_data)
        dvhs.append(dvh)
    return dvhs
