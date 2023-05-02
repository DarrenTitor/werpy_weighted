"""
This module provides a function for calculating a list of the Word Error Rates for each of the reference and
hypothesis texts.

This module defines the following function:
    - wers(reference, hypothesis)
"""


import numpy as np
from .metrics import metrics


def wers(reference, hypothesis):
    """
    This function calculates a list of the Word Error Rates for each of the reference and hypothesis texts.

    Parameters
    ----------
    reference : str, list or numpy array
        The ground truth transcription of a recorded speech or the expected output of a live speech.
    hypothesis : str, list or numpy array
        The text generated by a speech-to-text algorithm/system which will be compared to the reference text.

    Raises
    ------
    ValueError
        if the two input parameters do not contain the same amount of elements.
    AttributeError
        if input text is not a string, list or np.ndarray data type.

    Returns
    -------
    float or list
        This function will return either a single Word Error Rate (if the input is a pair of strings) or a list of Word
        Error Rates (if the input is a pair of lists) for each of the reference and hypothesis texts.

    Example
    --------
    >>> ref = ['no one else could claim that','she cited multiple reasons why']
    >>> hyp = ['no one else could claim that','she sighted multiple reasons why']
    >>> wers_example_1 = wers(ref, hyp)
    >>> print(wers_example_1)
    [0.0, 0.2]
    """

    try:
        word_error_rate_breakdown = metrics(reference, hypothesis)
    except ValueError:
        print("ValueError: The Reference and Hypothesis input parameters must have the same number of elements.")
    except AttributeError:
        print("AttributeError: All text should be in a string format. Please check your input does not include any "
              "Numeric data types.")
    else:
        if isinstance(word_error_rate_breakdown[0], np.ndarray):
            transform_word_error_rate_breakdown = np.transpose(word_error_rate_breakdown.tolist())
            wers_result = transform_word_error_rate_breakdown[0].tolist()
        else:
            wers_result = word_error_rate_breakdown[0].tolist()
        return wers_result
