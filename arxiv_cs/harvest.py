import requests
import xml.etree.ElementTree as ET
import time
import json
import gzip
import os
from pathlib import Path
import argparse

OAI_URL = 'https://export.arxiv.org/oai2'

OAI_NAMESPACES = {
    'OAI': 'http://www.openarchives.org/OAI/2.0/',
    'arXiv': 'http://arxiv.org/OAI/arXivRaw/'
}

ARXIV_SETS = ["cs", "econ", "eess", "math", "physics", "physics:astro-ph", "physics:cond-mat", "physics:gr-qc", "physics:hep-ex",
              "physics:hep-lat", "physics:hep-ph", "physics:hep-th", "physics:math-ph", "physics:nlin", "physics:nucl-ex", "physics:nucl-th",
              "physics:physics", "physics:quant-ph", "q-bio", "q-fin", "stat"]


def _extract_resumption_token(elem):
    """ Extract resumption token from given OAI element."""
    resumption_token = elem.find(
        'OAI:ListRecords/OAI:resumptionToken',
        OAI_NAMESPACES
    )

    return resumption_token.text if resumption_token is not None else ''


def _extract_arxiv_records(elem):
    """ Extract all records from given OAI element."""
    records = elem.findall(
        'OAI:ListRecords/OAI:record/OAI:metadata/arXiv:arXivRaw',
        OAI_NAMESPACES
    )
    return records


def _check_errors(elem):
    """ Check if there are errors in OAI response."""
    error = elem.find('OAI:error', OAI_NAMESPACES)
    if error is not None:
        raise RuntimeError(
            'OAI error: {}'.format(error.text)
        )
    else:
        print("No errors in chunk")


def _find(elem, key):
    """ Find in element an item given a key."""
    item = elem.find('arXiv:{}'.format(key), OAI_NAMESPACES)
    return item.text if item is not None else None


def _findall(elem, key):
    """ Find in element all items given a key"""
    return elem.findall('arXiv:{}'.format(key), OAI_NAMESPACES)


def parse_arxiv_record(elem):
    """ Parse an OAI xml element and transform it into a dictionary."""
    # Date encoded in id
    keys = ['id', 'authors', 'title', 'abstract']

    record = {key: _find(elem, key) for key in keys}
    record['categories'] = _find(elem, 'categories')

    return record


def parse_chunk(chunk):
    """ Parse an OAI chunk obtained by get_oai_chunk. Return a list of parsed records and the resumption token."""
    root = ET.fromstring(chunk)
    _check_errors(root)
    resumption_token = _extract_resumption_token(root)
    records = _extract_arxiv_records(root)
    records_parsed = [parse_arxiv_record(r) for r in records]
    return records_parsed, resumption_token


def get_oai_chunk(params, url=OAI_URL, resumption_token=None):
    """ Get from OAI arxiv a chunk of 1000 records given the OAI parameters."""

    # resumptionToken is exclusive, the argument may be included with request, but must be the only argument
    # (in addition to the verb argument).
    if resumption_token:
        params = {'verb': 'ListRecords', 'resumptionToken': resumption_token}

    print("params: ", params)

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.text

    if response.status_code == 503:
        # by default wait 20 seconds
        seconds = int(response.headers.get('Retry-After', 20)) * 1.5
        print(
            f"Retry-After from OAI-PMH request, waiting {seconds} seconds until retry ...")

        time.sleep(seconds)
        return get_oai_chunk(params, resumption_token=resumption_token)
    else:
        raise Exception(
            "Unknown response status {}".format(response.status_code))


def dump(records_parsed, output_file):
    """ Save chunk into a compressed text file. Successive chunks will be appended."""
    with gzip.open(output_file, 'at', encoding='utf-8') as f:
        for record in records_parsed:
            f.write(json.dumps(record) + '\n')


def harvest(params, output_folder, sleep=20):
    """

    :param params: OAI parameters.
    :param output_file: file name where the OAI chunks will be saved.
    :param sleep: seconds to wait between OAI requests (min. 15 secs).
    :return: None
    """

    if not os.path.exists(output_folder):
        os.mkdir(output_folder)

    name_file = f"arxiv-{params['set']}.txt.gz"
    output_file = os.path.join(output_folder, name_file)

    print("output_file: ", output_file)

    if sleep < 15:
        raise Exception("Be nice, sleep must be > 15 seconds.")

    resumption_token = params['resumptionToken']

    num_chunks = 0
    num_records = 0
    # records = []  # dev: temporal

    while True:

        print("-" * 60)

        chunk = get_oai_chunk(params, resumption_token=resumption_token)
        records_parsed, resumption_token = parse_chunk(chunk)

        # save to file
        dump(records_parsed, output_file)

        # records.append(records_parsed)  # dev: temporal

        num_chunks += 1
        num_records += len(records_parsed)

        print(f"num_chunks: {num_chunks}  num_records: {num_records}")

        if resumption_token is None:
            print(
                f"Download finished, with {num_chunks} chunks and {num_records} records.")
            print(f"Raw dataset stored in: {output_file}")
            return  # records   # dev: temporal

        print(f"sleeping {sleep} seconds")
        time.sleep(sleep)


def main():

    parser = argparse.ArgumentParser(description='ArXiv harvest')
    parser.add_argument("output_folder", type=str, help="mandatory arg. ")
    parser.add_argument("-s", "--set", nargs='?', default="cs", type=str, choices=ARXIV_SETS)
    parser.add_argument("-f", "--from_date", nargs='?', default=None, type=str, help="YYYY-MM-DD")
    parser.add_argument("-u", "--until_date", nargs='?', default=None, type=str, help="YYYY-MM-DD")
    parser.add_argument("-t", "--sleep", nargs='?', default=15, type=int,
                        help="Delay between requests in seconds. Min. 12.")

    parser.add_argument("-k", "--resumptionToken", nargs='?', default=None, type=str, help="Resumption token")
    # parameters = {'verb': 'ListRecords', 'metadataPrefix': 'arXivRaw', 'from': '2019-10-01',
    #               'until': '2019-10-04', 'set': 'cs'}
    # parameters = {'verb': 'ListRecords', 'metadataPrefix': 'arXivRaw', 'set': 'cs'}

    # output_folder = "../data/test2"

    args = parser.parse_args()

    arxiv_params = {'verb': 'ListRecords', 'metadataPrefix': 'arXivRaw', 'set': args.set}

    if args.from_date:
        arxiv_params['from'] = args.from_date
    if args.until_date:
        arxiv_params['until'] = args.until_date

    arxiv_params['resumptionToken'] = args.resumptionToken

    harvest(arxiv_params, args.output_folder, sleep=args.sleep)


if __name__ == "__main__":
    main()
