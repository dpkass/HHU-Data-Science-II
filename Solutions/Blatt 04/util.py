import glob
import os.path
import email
import pandas as pd


def rent_in_rome(n=None, file='data/dataset_rent_rome_kijiji.tsv',
    cols=('Title', 'Short Description')):
    return pd.read_csv(file, sep='\t', header=0, nrows=n, usecols=cols)


def enron_email(n=None, dir_glob_pattern=f'data/maildir/**/*'):
    def read_file(path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            raw_email = file.read()
            msg = email.message_from_string(raw_email)
            return {
                'file': path,
                'subject': msg['subject'],
                'from': msg['from'],
                'to': msg['to'],
                'body': msg.get_payload(decode=True).decode(errors='ignore')
            }

    def get_n_files(n, paths):
        i = 0
        for path in paths:
            if i == n: break
            if os.path.isfile(path):
                i += 1
                yield path

    paths = glob.glob(dir_glob_pattern, recursive=True)
    return pd.DataFrame(read_file(file) for file in get_n_files(n, paths))
