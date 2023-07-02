"""
This module contains two functions: calculations and metrics. The calculations function takes two input sequences (
reference and hypothesis) and returns a ragged array containing the word error rate (WER), Levenshtein distance (LD), 
number of words in the reference sequence, counts of insertions, deletions and substitutions, as well as lists of 
inserted, deleted and substituted words. The metrics function applies vectorization to the calculations function, 
enabling it to take in multiple values for reference and hypothesis in the form of lists or numpy arrays.

Functions:
- calculations(reference, hypothesis) -> np.ndarray: Calculates WER and related metrics for two input sequences and 
returns a ragged array containing the metrics.
- metrics(reference, hypothesis) -> np.ndarray: Applies vectorization to the calculations function to calculate WER 
and related metrics for multiple pairs of input sequences.
"""

import numpy as np


def calculations(reference, hypothesis) -> np.ndarray:
    """
    This function calculates the word error rate and provides a breakdown of the word edits (inserts, deletions and
    substitutions) required to minimally transform one text sequence into another.

    Parameters
    ----------
    reference : str, list or numpy array
        The ground truth transcription of a recorded speech or the expected output of a live speech.
    hypothesis : str, list or numpy array
        The text generated by a speech-to-text algorithm/system which will be compared to the reference text.

    Returns
    -------
    np.ndarray
        This function will return a ragged array containing the following nine variables:
            1. wer - The Word Error Rate
            2. ld - The Levenshtein distance
            3. m - The number of words in the reference sequence
            4. insertions - count of words that are present in the hypothesis sequence but not in the reference
            5. deletions - count of words that are present in the reference sequence but not in the hypothesis
            6. substitutions - count of words needing to be transformed so the hypothesis matches the reference
            7. inserted_words - list of inserted words
            8. deleted_words - list of deleted words
            9. substituted_words - list of substitutions. Each substitution will be shown as a tuple with the
            reference word and the hypothesis word. For example: [(cited, sighted), (abnormally, normally)]
    """
    reference_word = reference.split()
    hypothesis_word = hypothesis.split()

    m, n = len(reference_word), len(hypothesis_word)
    i, j = 0, 0
    ldm = np.zeros((m + 1, n + 1), dtype=int)
    for i in range(m + 1):
        ldm[i, 0] = i
    for j in range(n + 1):
        ldm[0, j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if reference_word[i - 1] == hypothesis_word[j - 1]:
                ldm[i, j] = ldm[i - 1, j - 1]
            else:
                # https://github.com/usnistgov/SCTK/blob/f48376a203ab17f0d479995d87275db6772dcb4a/doc/sclite.htm#L173
                # cost of correct words, insertions, deletions and substitutions as 0, 3, 3 and 4 respectively
                substitution = ldm[i - 1, j - 1] + 4
                insertion = ldm[i, j - 1] + 3
                deletion = ldm[i - 1, j] + 3
                ldm[i, j] = min(substitution, insertion, deletion)

    ld = ldm[i, j]
    wer = ld / m

    insertions, deletions, substitutions = 0, 0, 0
    inserted_words, deleted_words, substituted_words = [], [], []
    i, j = m, n
    while i > 0 or j > 0:
        if i > 0 and j > 0 and reference_word[i - 1] == hypothesis_word[j - 1]:
            i -= 1
            j -= 1
        else:
            if i > 0 and j > 0 and ldm[i, j] == ldm[i - 1, j - 1] + 1:
                substitutions += 1
                substituted_words.append((reference_word[i - 1], hypothesis_word[j - 1]))
                i -= 1
                j -= 1
            elif j > 0 and ldm[i, j] == ldm[i, j - 1] + 1:
                insertions += 1
                inserted_words.append(hypothesis_word[j - 1])
                j -= 1
            elif i > 0 and ldm[i, j] == ldm[i - 1, j] + 1:
                deletions += 1
                deleted_words.append(reference_word[i - 1])
                i -= 1

    inserted_words.reverse(), deleted_words.reverse(), substituted_words.reverse()

    return np.array(
        [wer, ld, m, insertions, deletions, substitutions, inserted_words, deleted_words, substituted_words],
        dtype=object)


def metrics(reference, hypothesis) -> np.ndarray:
    """
    This function applies vectorization to the calculations function. It enables the reference and hypothesis input
    to contain multiple values in the form of lists or numpy arrays, in addition to single strings.

    Parameters
    ----------
    reference : str, list or numpy array
        The ground truth transcription of a recorded speech or the expected output of a live speech.
    hypothesis : str, list or numpy array
        The text generated by a speech-to-text algorithm/system which will be compared to the reference text.

    Returns
    -------
    np.ndarray
        This function will return a ragged array containing the Word Error Rate, Levenshtein distance, the number of
        words in the reference sequence, insertions count, deletions count, substitutions count, a list of inserted
        words, a list of deleted words and a list of substituted words.
    """
    vectorize_calculations = np.vectorize(calculations)
    result = vectorize_calculations(reference, hypothesis)
    return result
