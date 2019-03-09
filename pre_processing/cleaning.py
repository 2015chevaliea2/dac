import re


def clean_df_column(df_column):
    """
    :param df_column: a dataframe column to clean
    :return: a dataframe column with cleaned data
    """
    if type(df_column) == str:
        return clean_string(df_column)

    else:
        return df_column.apply(lambda x: clean_string(x))


def remove_words_from_df_columns(df_column, to_remove):
    """
    :param df_column:
    :return:
    """
    return df_column.apply(lambda x: remove_words_from_field(x, to_remove))


def clean_string(string):
    """
    Function to clean a string by suppressing any capital letters, special characters or double spaces
    :param string: string to clean
    :return: string cleaned
    """

    if not type(string) is str:
        raise TypeError("Expected type str")

    # Remove special chars
    str_punctuation = re.sub('\W+', ' ', string)
    # Lower case
    str_lowercase = str_punctuation.lower()
    # Remove double spaces
    str_double_spaces = re.sub('\s+', ' ', str_lowercase).strip()
    # Translates special chars
    dict1 = str.maketrans('0123456789abcdefghijklmnopqrstuvwxyzªµºãàáâåäçèéêëìíîïñõòóôöøùúûüÿƒπω',
                          '0123456789abcdefghijklmnopqrstuvwxyzauoaaaaaaceeeeiiiinoooooouuuuyfpw')
    str_special_chars = str_double_spaces.translate(dict1)
    str_out = str_special_chars.replace("œ", "oe").replace("ﬁ", "fi").replace("ﬂ", "fl").replace("æ", "ae").replace("ß", "ss")
    return str_out


def remove_words_from_field(field, to_remove):
    """
    Removes words in to_remove list from field and return processed field
    :param field: field to be cleaned
    :param to_remove: a list of words to remove
    :return field: cleaned field
    """
    if not type(field) is str:
        raise TypeError("Expected type str")

    field = field.split()
    for word in to_remove:
        try:
            field.remove(word)
        except ValueError:
            pass
    field = ' '.join(field)
    return field


def sort(x):
    """
    Use to sort names in author fields
    :param x: string
    :return: sorted string
    """
    a = x.split()
    a.sort()
    a = ' '.join(a)
    return a


def add_dummy_author_column(common_names, data):
    data['authors_dummy'] = data.author.apply(lambda x: remove_dummy_names_from_author(common_names, x))
    return data


def add_dummy_title_column(common_names, data):
    data['title_dummy'] = data.title.apply(lambda x: remove_dummy_names_from_title(common_names, x))
    return data


def remove_dummy_names_from_author(dummy_names, authors):
    """

    :param dummy_names:
    :param authors:
    :return: a list of names
    """
    authors = str(authors).split()
    for name in dummy_names:
        if len(authors) <= 1:
            break
        else:
            if name in authors:
                authors.remove(name)
    return authors


def remove_dummy_names_from_title(dummy_names, authors):
    """

    :param dummy_names:
    :param authors:
    :return: a list of names
    """
    authors = str(authors).split()
    for name in dummy_names:
        if len(authors) <= 1:
            break
        else:
            if name in authors:
                authors.remove(name)
    return ' '.join(authors)

