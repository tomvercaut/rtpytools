from typing import List


class LimitedList(List):
    """
    A list with a specified limit.

    :param limit: The maximum limit for the list.
    :type limit: int
    """
    def __init__(self, limit: int) -> None:
        """
        Initializes the List with a specified limit.

        :param limit: The maximum limit for the object.
        :type limit: int
        """
        super().__init__()
        self.limit = limit

    def append(self, value) -> None:
        """
        Append an object to the list if the number of items is less than the limit.

        :param value: The value to be appended to the list.
        :return: None
        """
        if len(self) >= self.limit:
            return
        super().append(value)

    def insert(self, index, value):
        """
        :param index: the index at which the value should be inserted
        :param value: the value to be inserted
        :return: None

        Inserts the given value at the specified index. If the list is limited, the insertion will be ignored.

        Example:
            >>> myList = LimitedList(5)
            >>> myList.insert(2, "test")
            """
        if self.is_limited():
            return
        super().insert(index, value)

    def extend(self, __iterable):
        """
        :param __iterable: An iterable object.
        :return: None.

        The `extend` method is used to add elements from an iterable object (__iterable)
        to the end of the current object.
        If the current object is a LimitedList and is already at its limit, no elements will be added.

        If the __iterable is an instance of List or LimitedList, the elements will be added up to the limit of the
        current object. If the combined length of the current object and the __iterable exceeds the limit,
        only a portion of the __iterable will be added, ensuring that the total length does not exceed the limit.

        If the __iterable is neither an instance of List nor LimitedList, each element from the __iterable will be
        individually appended to the current object.

        Example usage:
            my_list = LimitedList(3)
            my_list.append(5)
            my_list.extend([1, 2, 3])
            print(my_list)  # Output: [5, 1, 2]
        """
        if self.is_limited():
            return
        if isinstance(__iterable, List) or isinstance(__iterable, LimitedList):
            n = len(__iterable)
            m = n + len(self)
            if m < self.limit:
                super().extend(__iterable)
            else:
                lim = self.limit - len(self)
                super().extend(__iterable[:lim])
        else:
            for item in __iterable:
                self.append(item)

    def is_limited(self) -> bool:
        """
        Checks if the length of the object is greater than or equal to the limit.

        :return: True if the length is greater than or equal to the limit, False otherwise.
        :rtype: bool
        """
        return self.__len__() >= self.limit
