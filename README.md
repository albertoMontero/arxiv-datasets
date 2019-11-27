# arxiv-cv dataset

![alt text](images/dataset_image.png)


## Repository for Arxiv-cs dataset, a complete computer science ArXiv articles metadata dataset.

## Description of dataset.

Arxiv-cs contains about 240k records of articles metadata from ArXiv [Computing Research Repository (CoRR)](https://arxiv.org/corr). It contains a few relevant fields extracted from computer science papers, including identifier, title, abstract and categories

## Dataset attributes.

Arxiv-cs is presented as a json file containing the following attributes (all of them as a string):

* **id**: ArXiv internal article identifier.
* **title**: title of article.
* **abstract**: abstract of article.
* **categories**: list of category tags the article was submitted. White space separated, with primary category in first position. Notice that we have tags coming from other subjects like physics, statistics, math, etc.

## Python scripts

This repository includes also basic a basic python script to harvest arXiv metadata [arxiv-cs project](archiv_cs/).

The requeriments for the script is requests package. Implemented with python 3.7, but theoretically should work with 3.6+. You can install requests from pip or better using an virtual environment like conda:

    pip install requests
    conda install requests

To download a arxiv metadata bulk run harvest.py. The only mandatory parameter is a folder where to save the dataset.

Example, to download the Computer Science bulk:

    python harvest output_folder

To customize to other sets (math, physics, etc), or to restrict the download to some dates:

    python harvest.py output_folder -s set -f from_date -u until_date -t sleep -k resumption_token
    
The parameter resumption_token allow to resume the download when the connection for whatever reason interrupts the download.

The parameter sleep is the delay between chunks of data. The minimum allowed is 12 seconds.

Example. Let's say we want to download the Quantitative Biology (q-bio) repository of October 2019 into folder ../data/qbio with 20 seconds of delay between requests (to be nice with API)

    python harvest.py ../data/q-bio -s q-bio -f 2019-10-01 -u 2019-10-31 -t 20  

This will save a file named arxiv-q-bio.txt.gz in folder ../data/q-bio. 

When running harvest.py you will get messages like

    params:  {'verb': 'ListRecords', 'resumptionToken': '4019533|1001'}
    No errors in chunk
    num_chunks: 2  num_records: 2000
    sleeping 15 seconds

If for any reason the connection is interrupted, you can always resume your download using the last resumption token given in the output, something like this

    python harvest.py ../data/q-bio '4019533|1001'

## License

MIT license, and CC0 1.0 license for data folder containing the dataset.
