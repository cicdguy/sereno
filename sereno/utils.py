"""
Utils
"""


def _get_unique_values_for_given_key(_list_of_dicts, _value):
    j = []
    for i in _list_of_dicts:
        for k, val in i.items():
            if k == _value:
                j.append(val)
    return list(set(j))


def _get_items_for_given_values_list(_list_of_dicts, _list_of_values, _key, _desired_key):  # noqa: E501  # pylint: disable=C0301
    i = {}
    for lval in _list_of_values:
        k = []
        for j in _list_of_dicts:
            if j[_key] == lval:
                k.append(j[_desired_key])
        i[lval] = {
            _desired_key: list(set(k)),
            "count": len(list(set(k)))
        }
    return i
