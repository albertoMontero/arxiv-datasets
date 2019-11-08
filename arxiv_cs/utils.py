import gzip
import json
import os
from pathlib import Path


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


def clean_df(df):
    """ Clean abstract and title fields from a pandas data frame."""

    df.abstract = df.abstract.str.strip()
    df.abstract = df.abstract.str.replace('\n', ' ').replace('\s+', ' ')

    df.title = df.title.str.strip()
    df.title = df.title.str.replace('\n', ' ').replace('\s+', ' ')

    return df


# TODO: normalize authors.
# TODO: parse date from id.

def clean_raw_ds(jsonfile, outfolder, compressed=False):
    """ Clean abstract and title fields directly from json file."""

    if compressed:
        with gzip.open(jsonfile, 'rt') as f:
            data = json.load(f)
    else:
        with open(jsonfile, 'r') as f:
            data = json.load(f)

    for record in data:
        record['title'] = record['title'].strip().replace('\n', ' ').replace('\s+', ' ')
        record['abstract'] = record['abstract'].strip().replace('\n', ' ').replace('\s+', ' ')

    if not os.path.exists(outfolder):
        os.mkdir(outfolder)

    if compressed:
        with gzip.open(Path(outfolder) / Path(jsonfile).name, 'wt') as f:
            json.dump(data, f)
    else:
        with open(Path(outfolder) / Path(jsonfile).name, 'w') as f:
            json.dump(data, f)