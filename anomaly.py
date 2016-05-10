# -*- coding: utf-8 -*-

import argparse
import logging
import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer


def dataframe_processing(dataframe, logger, col_text, groupby='D', min_df=1, max_n_gram=1):
    logger.info("Initial number of rows: {}".format(dataframe.shape[0]))
    countVectorizer = CountVectorizer(analyzer='word', ngram_range=(1, max_n_gram), min_df=min_df)
    dataframe = dataframe.groupby(dataframe.index)[col_text].apply(lambda x: text_preprocessing('\n'.join(x)))
    logger.info("Number of rows after grouping by date: {} ({} - {})"
                .format(dataframe.shape[0], dataframe.first_valid_index(), dataframe.last_valid_index()))
    term_doc_matrix = countVectorizer.fit_transform(dataframe).toarray()
    vocab = countVectorizer.get_feature_names()
    logger.info("Vocabulary size: {}".format(len(vocab)))
    term_vec_data = pd.DataFrame(term_doc_matrix, index=dataframe.index, columns=vocab, dtype='uint64')
    term_vec_data = term_vec_data.resample(groupby).sum()
    logger.info("Number of rows after grouping by {}: {}".format(groupby, term_vec_data.shape[0]))
    return term_vec_data


def read_dataset(file_path, col_index, col_text):
    return pd.read_csv(file_path, sep=';', engine='python', quotechar='"', header=0, parse_dates=[col_index],
                       encoding='utf-8', usecols=[col_index, col_text], index_col=0)


def text_preprocessing(text):
    """Removes tags and author name from text.

        Args:
            text: input text.

        Returns:
            Text with removed tags and author name.

        Examples:

        >>> text_preprocessing("[TEMAT]Odmowa kredytu[/TEMAT] Witam czy odmowa kredytu jest notowana")
        'Odmowa kredytu Witam czy odmowa kredytu jest notowana'

        >>> text_preprocessing("[CYTAT MSG=5487205][AUTOR]ArturKredyty[/AUTOR]Jeśli te chwilówki były spłacane[/CYTAT] Tak, były spłacane.")
        'Jeśli te chwilówki były spłacane Tak, były spłacane.'

        >>> text_preprocessing("[Cytat Mag=9106][Autor]Leila[/AUTOR]Miałam ale zrezygnowałam z niego.[/CYTAT] o to ciekawe.")
        'Miałam ale zrezygnowałam z niego. o to ciekawe.'

    """

    text = re.sub(r"\[TEMAT\](.*)\[/TEMAT\]", r"\1", text)
    text = re.sub(r"\[CYTAT (MSG|Mag)=\d+\]\[AUTOR\](.*)\[/AUTOR\](.*)\[/CYTAT\]", r"\3", text, flags=re.I)
    return text


def create_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_arguments():
    parser = argparse.ArgumentParser(description='Anomaly detection in time series text data')
    parser.add_argument('-f', '--file_name', default="bank_data.csv", help="input file path")
    parser.add_argument('-g', '--group_by', default="D", choices=['D', 'W', 'M'],
                        help="group by: D - day (default), W - week, M - month")
    parser.add_argument('-d', '--min_df', default=2, help="min number of documents for a n-gram")
    parser.add_argument('-n', '--max_n_gram', default=2, help="max n-gram size")
    parser.add_argument('-i', '--col_index', default="start_dt", help="index column name")
    parser.add_argument('-t', '--col_text', default="body", help="text column name")
    args = parser.parse_args()
    return args


def print_data(data_frame, ind=0):
    signal = data_frame.as_matrix(columns=[data_frame.columns[ind]])
    mask = get_median_anomaly(signal)
    print(data_frame[mask].iloc[:,ind])


def get_median_anomaly(signal, threshold = 4):
    difference = np.abs(signal - np.median(signal))
    median_difference = np.median(difference)
    s = 0 if median_difference == 0 else difference / float(median_difference)
    mask = s > threshold
    return mask


if __name__ == "__main__":
    # import doctest
    # doctest.testmod()

    logger = create_logger()
    args = get_arguments()

    bank_data = read_dataset(args.file_name, args.col_index, args.col_text)
    bank_data = dataframe_processing(bank_data, logger=logger, col_text=args.col_text, groupby=args.group_by,
                                     min_df=args.min_df, max_n_gram=args.max_n_gram)
    print_data(bank_data)
