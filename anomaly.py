# -*- coding: utf-8 -*-

import argparse
import logging
import re

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


def data_frame_processing(data_frame, logger, col_text, group_by='D', min_df=1, max_n_gram=1):
    """Process given data frame:
    - clean text data
    - crate n-gram count vectors
    - group n-gram count vectors by given grouping key

    Args:
        data_frame: input data frame
        logger: stream_logger
        col_text: name of the column with text data to process
        group_by: group by key
        min_df: minimum number of documents for an n-gram
        max_n_gram: maximum n-gram

    Returns:
        Data frame with n-gram count vectors
    """

    logger.info("Initial number of rows: {}".format(data_frame.shape[0]))
    count_vectorizer = CountVectorizer(analyzer='word', ngram_range=(1, max_n_gram), min_df=min_df)
    data_frame = data_frame.groupby(data_frame.index)[col_text].apply(lambda x: text_processing('\n'.join(x)))
    logger.info("Number of rows after grouping by date: {} ({} - {})"
                .format(data_frame.shape[0], data_frame.first_valid_index(), data_frame.last_valid_index()))
    term_doc_matrix = count_vectorizer.fit_transform(data_frame).toarray()
    vocab = count_vectorizer.get_feature_names()
    logger.info("Vocabulary size: {}".format(len(vocab)))
    term_vec_data = pd.DataFrame(term_doc_matrix, index=data_frame.index, columns=vocab, dtype='uint64')
    term_vec_data = term_vec_data.resample(group_by).sum()
    logger.info("Number of rows after grouping by {}: {}".format(group_by, term_vec_data.shape[0]))
    return term_vec_data


def read_dataset(file_path, col_index, col_text):
    """Read data frame from given file path.

    Args:
        file_path: input file path
        col_index: name of the column with index data (dates)
        col_text: name of the column with text data

    Returns:
        Data frame with text data indexed by dates
    """
    return pd.read_csv(file_path, sep=';', engine='python', quotechar='"', header=0, parse_dates=[col_index],
                       encoding='utf-8', usecols=[col_index, col_text], index_col=0)


def text_processing(text):
    """Removes tags and author name from text.

        Args:
            text: input text.

        Returns:
            Text with removed tags and author name.

        Examples:

        >>> text_processing("[TEMAT]Odmowa kredytu[/TEMAT] Witam czy odmowa kredytu jest notowana")
        'Odmowa kredytu Witam czy odmowa kredytu jest notowana'

        >>> text_processing("[CYTAT MSG=5487205][AUTOR]ArturKredyty[/AUTOR]Jeśli te chwilówki były spłacane[/CYTAT] " \
         "Tak, były spłacane.")
        'Jeśli te chwilówki były spłacane Tak, były spłacane.'

        >>> text_processing("[Cytat Mag=9106][Autor]Leila[/AUTOR]Miałam ale zrezygnowałam z niego.[/CYTAT] o to " \
        "ciekawe.")
        'Miałam ale zrezygnowałam z niego. o to ciekawe.'
    """
    text = re.sub(r"\[TEMAT\](.*)\[/TEMAT\]", r"\1", text)
    text = re.sub(r"\[CYTAT (MSG|Mag)=\d+\]\[AUTOR\](.*)\[/AUTOR\](.*)\[/CYTAT\]", r"\3", text, flags=re.I)
    return text


def analyse_data(data_frame, threshold):
    """Detect anomalies in a given data frame.

    Args:
        data_frame: input data frame
        threshold: output threshold

    Returns:
        Generator yielding string representation of non-empty results of anomaly detection.
    """
    for ngram in data_frame.columns:
        result = analyse_single_ngram(data_frame, ngram, threshold)
        if not result.empty:
            yield result.to_string(header=False, name=True)


def analyse_single_ngram(data_frame, ngram, threshold):
    """Detect anomalies in a given time series data.

    Args:
        data_frame: input data frame
        ngram: n-gram (column name) to analyse
        threshold: output threshold (algorithm parameter)

    Returns:
        Outliers data found by the algorithm.
    """
    signal = data_frame.as_matrix(columns=[ngram])
    mask = get_median_anomaly(signal, threshold)
    return data_frame[mask].loc[:, ngram]


def write_result(data_generator, output_file_path):
    """Write data from a given data generator to a file.

    Args:
        data_generator: data generator
        output_file_path: output file path
    """
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        output_file.write("\n\n".join(list(data_generator)))


def get_median_anomaly(signal, threshold=4):
    """Find anomalies in a given signal using median filtering algorithm.

    Args:
        signal: signal data to analyse
        threshold: median filtering algorithm parameter

    Returns:
        An array with boolean values indicating whether a value in a given position is an outlier (True) or not (False).
    """
    difference = np.abs(signal - np.median(signal))
    median_difference = np.median(difference)
    s = np.zeros(len(signal)) if median_difference == 0 else difference / float(median_difference)
    mask = s > threshold
    return mask


def create_logger():
    """Create stream_logger.

    Returns:
        Logger instance.
    """
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_arguments():
    """Parse program arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Anomaly detection in time series text data')
    parser.add_argument('-i', '--input_file', default="bank_data.csv", help="input file path")
    parser.add_argument('-o', '--output_file', default="output.txt", help="output file path")
    parser.add_argument('-g', '--group_by', default="D", choices=['D', 'W', 'M'],
                        help="group by: D - day (default), W - week, M - month")
    parser.add_argument('-d', '--min_df', default=3, help="min number of documents for a n-gram")
    parser.add_argument('-n', '--max_n_gram', default=2, help="max n-gram size")
    parser.add_argument('-x', '--col_index', default="start_dt", help="index column name")
    parser.add_argument('-b', '--col_body', default="body", help="text column name")
    parser.add_argument('-t', '--threshold', default=6, help="output threshold")
    return parser.parse_args()


if __name__ == "__main__":
    import doctest
    doctest.testmod()

    stream_logger = create_logger()
    args = get_arguments()

    bank_data = read_dataset(args.input_file, args.col_index, args.col_body)
    bank_data = data_frame_processing(bank_data, logger=stream_logger, col_text=args.col_body, group_by=args.group_by,
                                      min_df=args.min_df, max_n_gram=args.max_n_gram)
    analysis_result = analyse_data(bank_data, args.threshold)
    write_result(analysis_result, args.output_file)
