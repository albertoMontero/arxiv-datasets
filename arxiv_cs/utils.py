import gzip
import json
import os
from pathlib import Path
import datetime
import re


def raw2json(textfile, outfolder=None, compressed=False):
    """ Convert arxiv_cs.txt.gz (raw data from harvest) file to arxiv_cs.json.gz if compressed is True in the given
    folder. If False, it is converted to arxiv_cs.json."""

    records = []
    with gzip.open(textfile, 'rt') as f:
        for line in f:
            records.append(json.loads(line))

    p = Path(textfile)

    if not outfolder:
        fname = p.parent / str(p.name.split('.')[0] + ".json")
    else:
        if not os.path.exists(outfolder):
            os.mkdir(outfolder)
        fname = Path(outfolder) / str(p.name.split('.')[0] + ".json")

    if compressed:
        with gzip.open(str(fname) + ".gz", 'wt') as fout:
            json.dump(records, fout)
    else:
        with open(fname, 'w') as fout:
            json.dump(records, fout)


def process_raw_df(df):
    """ Clean abstract and title fields from a pandas data frame."""

    df.abstract = df.abstract.str.strip()
    df.abstract = df.abstract.str.replace(
        '\n', ' ', regex=True).replace('\s+', ' ', regex=True)

    df.title = df.title.str.strip()
    df.title = df.title.str.replace(
        '\n', ' ', regex=True).replace('\s+', ' ', regex=True)

    return df


def extract_date(id_list):
    p = re.compile('\d')
    dates = []
    for id in id_list:
        if p.match(id):
            parts = id.split('.')[0]
            month = int(parts[2:])
        else:
            parts = id.split('/')[1]
            month = int(parts[2:4])

        year = int(parts[:2]) + 1900
        if year < 1993:
            year += 100

        dates.append(datetime.date(year, month, 1))

    return dates
