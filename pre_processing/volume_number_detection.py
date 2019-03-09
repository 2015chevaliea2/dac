import pandas as pd
import re
from pre_processing import cleaning


def extract_volume_info(title):
    """
    Function that identifies if a title contains a volume information and returns the volume number where appropriate,
    else it returns None.

    In practice, it uses regular expression to identify each pattern which could be a volume information.

    :param title: a string
    :return: None, or the volume number (int) where appropriate
    """
    # ETAPE 0: Initialisation
    key_words_list = [' tome ', ' t ', ' volume ', ' vol ', ' t']  # Pour séparer les n°  revues, ajouter ' n '.
    arabic_volume_nbr = int()
    roman_volume_nbr = int()
    multi_volumes = False
    # A. (multi-vol) Vérifier la présence de mots clé spécifiques aux multi-volumes, associés à au moins un chiffre
    if re.findall('(?i)( tomes | tomes$| volumes | volumes$| lot |^lot )', title):
            multi_volumes = True
    else:
        # B. (vol) Chercher les mots-clé introduisant un numéro de volume
        for key_word in key_words_list:
            if arabic_volume_nbr or roman_volume_nbr:
                break
            # C. (multi-vol) Vérifier l'occurence du mot clé
            elif len(re.findall('(?i)'+key_word, title)) > 1 and key_word != ' t' and key_word != ' t ':
                multi_volumes = True
            # D. (vol) Si mono occurence d'un mot clé, chercher le numéro de volume (s'il existe)
            elif len(re.findall('(?i)'+key_word, title)) == 1:
                # scinder la chaîne en deux selon le séparateur 'tome', ' t ', 'volume' etc
                split_title = re.split('(?i)'+key_word, title)
                # Recherche du n° de volume uniquement dans le mot suivant immédiatement le mot clé ('tome', 'vol'...)
                separate_words = re.split(' ', split_title[1])
                arabic_volume_nbr = extract_arabic_numerals(separate_words[0])
                roman_volume_nbr = extract_roman_numerals(separate_words[0])
                # On vérifie si le mot suivant le n° de volume est 'et', ce qui implique un multi-tome
                if arabic_volume_nbr or roman_volume_nbr:
                    if len(separate_words) > 1 and re.match('(?i)^et$', separate_words[1]):
                        multi_volumes = True

    if multi_volumes:
        return -2
    elif not arabic_volume_nbr and roman_volume_nbr:
        return decode_roman_numeral(roman_volume_nbr)
    elif arabic_volume_nbr and not roman_volume_nbr:
        return arabic_volume_nbr
    else:
        return -1


def extract_roman_numerals(string):
    """Trouver un chiffre romain dans une chaîne de caractère d'un seul mot non entouré d'espaces"""
    if re.findall('(?i)^(M{0,4})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$', string):
        return ''.join(re.findall('(?i)^(M{0,4})(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$', string)[0])
    else:
        return None


def decode_roman_numeral(roman):
    """Calculate the numeric value of a Roman numeral (in lowercase)"""
    trans = {'i': 1, 'v': 5, 'x': 10, 'l': 50, 'c': 100, 'd': 500, 'm': 1000}
    values = [trans[r] for r in roman]
    return sum(
        val if val >= next_val else -val
        for val, next_val in zip(values[:-1], values[1:])
    ) + values[-1]


def extract_arabic_numerals(string):
    """Idem"""
    if re.findall('[0-9]+', string):
        return re.findall('[0-9]+', string)[0]
    else:
        return None


def add_volume_column(df):
    # todo : tester cette fonction dans le main !
    df['title'] = cleaning.clean_df_column(df['title'])
    df['VOLUME'] = df['title'].apply(extract_volume_info)
    return df


if __name__ == '__main__':

    def test_csv():
        df = pd.read_csv('../post_processing/test_clustered_25000.csv', sep=',', usecols=[0, 9], index_col=0)
        df['title'] = cleaning.clean_df_column(df['title'])
        df['VOLUME'] = df['title'].apply(extract_volume_info)
        df.to_csv('test_volume_17.csv', encoding='utf-8')

    test_csv()
