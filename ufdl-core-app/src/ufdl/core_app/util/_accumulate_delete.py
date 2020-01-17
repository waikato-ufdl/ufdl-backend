from typing import Dict, Tuple

# Types
DELETION_DICT_TYPE = Dict[str, int]
DELETION_RESULT_TYPE = Tuple[int, DELETION_DICT_TYPE]


def accumulate_delete(accumulator: DELETION_RESULT_TYPE,
                      deletion_result: DELETION_RESULT_TYPE) -> DELETION_RESULT_TYPE:
    """
    Takes the current deletion result accumulator and adds a new deletion
    result to it.

    :param accumulator:         The current value of the accumulator.
    :param deletion_result:     The new deletion result to add.
    :return:                    The new value of the accumulator.
    """
    # Update the total number of deleted objects
    total: int = accumulator[0] + deletion_result[0]

    # Update the deletion dictionary
    deletion_dict: DELETION_DICT_TYPE = accumulator[1].copy()
    for name, count in deletion_result[1].items():
        if name not in deletion_dict:
            deletion_dict[name] = 0
        deletion_dict[name] += count

    return total, deletion_dict
