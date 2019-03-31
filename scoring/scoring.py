import numpy as np


def to_matrix(df, c):
    """
    Creates the matrix M representing the clustering: M[i,j] = 1 if the books i and j are clustered together, else 0.
    :param df: a dataframe containing books and their cluster ids.
    :param c: the name of the column of df which contains the id_cluster
    :return: matrix M
    """
    n = len(df)
    M = np.identity(n, dtype=int)
    C = df[c]
    for i in range(1, n):
        for j in range(i):  # only the columns under the diagonal because symetric matrix
            if C.iloc[i] == C.iloc[j]:  # if the books i and j are considered as comparable, ie same cluster
                M[i, j] = 1
                M[j, i] = 1
    return M


def matrix_comparison(M_algo, M_ref):
    """
    Compares the matrix M_algo and M_ref, and returns performance scores
    :param M_algo: matrix representing the clustering made by the algorithm
    :param M_ref: matrix representing the true clustering of reference
    :return: precision, recall, F_score
    """
    if not isinstance(M_algo, np.ndarray) or not isinstance(M_ref, np.ndarray):
        raise TypeError("The matrix should be a numpy array")
    if M_algo.shape != M_ref.shape:
        raise ValueError("Both matrix should have the same shape.")

    n = len(M_algo[0])
    TP, TN, FP, FN = 0, 0, 0, 0
    for i in range(1, n):  # throughout the lines
        for j in range(i):  # throughout the columns under the diagonal
            if M_algo[i][j] == 1 and M_ref[i][j] == 1:
                TP += 1
            elif M_algo[i][j] == 0 and M_ref[i][j] == 1:
                FN += 1
            elif M_algo[i][j] == 1 and M_ref[i][j] == 0:
                FP += 1
            else:
                TN += 1
    
    precision = TP/(TP+FP)
    recall = TP/(TP+FN)
    F_score = 2*(precision*recall)/(precision+recall)
    
    return precision, recall, F_score


def performance(df_algo, df_ref):
    """
    Calls the functions to_matrix and matrix_comparison to get the scores out of dataframes df_algo and df_ref
    :param df_algo: dataframe containing books and their cluster ids computed by the algorithm
    :param df_ref: dataframe containing books and their true cluster ids of reference
    :return: precision, recall and F_score
    """
    df_algo = df_algo[['id', 'id_cluster']]  # keeps only the 2 columns that matter
    df_algo = df_algo.sort_values('id')  # sort df by index, to be sure to compare the books in the same order
    df_ref = df_ref[['id', 'id_cluster']]
    df_ref = df_ref.sort_values('id')

    M_to_compare = to_matrix(df_algo, 'id_cluster')
    M_ref = to_matrix(df_ref, 'id_cluster')

    return matrix_comparison(M_to_compare, M_ref)
