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

def to_lower_case(string: str) -> str:
    return string.lower()

def remove_under_score(string: str) -> str:
    return ''.join(string.split('_'))

def to_flat_case(string: str) -> str:
    result: str = to_lower_case(string)
    result = remove_under_score(result)
    return result

def snake_to_camel(string: str) -> str:
    words: list = to_lower_case(string).split('_')
    words: list = [words[0]] + [word.capitalize() for word in words[1:]]
    return ''.join(words)