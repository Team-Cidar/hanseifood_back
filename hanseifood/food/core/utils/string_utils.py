from typing import List


def parse_str_to_list(datas: str, sep: str = ',') -> List[str]:
    """returns a list of string

        Parameters
        ----------
        datas : str
            string data to split
        sep : str
            separator char

        Returns
        -------
        list[str]

        See Also
        --------
        If the length of string data is zero, It'll return empty list

        """
    if datas == '':
        return []
    return [data.strip() for data in datas.split(sep)]
