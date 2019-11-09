# Arxiv-cs dataset Report.

1. Context.

    TODO: Arxiv / Open Archive Initiative.

2. Title of dataset. 
   
   Arxiv-cs dataset, a complete computer science arxiv articles metadata dataset.
3. Description of dataset.

    Arxiv-cs contains about 240k records of articles metadata from arxiv [Computing Research Repository (CoRR)](https://arxiv.org/corr). It contains a few relevant fields extracted from computer science papers, including authors, title, abstract and categories.
4. Picture --> TODO, add link.
5. Content.

    Arxiv-cs is presented as a json file containing the following attributes (all of them as a string):
    * **id**: arxiv internal article identifier.
    * **authors**: articles authors, comma-separated.
    * **title**: title of article.
    * **abstract**: abstract of article.
    * **categories**: list of category tags the article was submitted. White space separated, with primary category in first position. Notice that we have tags coming from other subjects like physics, statistics, math, etc.

    The collecting date interval of records includes from the beginning of CoRR repository creation (1993-01) to the end of October 2019 (2019-10). Day of the month is not presented. --> TODO: remove first week of November.

    Arxiv provides several APIs services enabling developers the creation of valuable services to scientists and general public. When harvesting large amounts of data, the arxiv Bulk Data Access services are recommended. In this project we use the [OAI protocol for metadata harvesting](https://arxiv.org/help/oa) (OAI-PMH). Arxiv is a registered OAI-PMH data-provider, providing access to metadata for all articles, updated daily with new articles. This is the preferred way to bulk-download or keep an up-to-date copy of arXiv metadata. Arxiv suports [OAI_PMH v2.0 protocol](http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm).

    The harvest was performed with the python script [arxiv_cs/harvest.py](../arxiv_cs/harvest.py), which implements all protocols and requests needed to harvest the arxiv Computer Science repository. Some examples of use can also be found in notebooks [03_harvest_01.ipynb](../notebooks/experimental/03_harvest_01.ipynb) and [03_harvest_02.ipynb](../notebooks/experimental/03_harvest_02.ipynb) which were implemented as helpers in developing process.

    Briefly, harvest.py specifies the OAI ListRecords request protocol which returns chunks of 1000 records and a resumption token. This token is used in the next request to resume the download. Finally an empty resumption token is returned meaning that the complete bulk download is finished. The script define a delay of 15 seconds (at least 10 seconds is asked) between requests and the complete bulk for CoRR is downloaded in about 90 minutes (about 240K articles metadata).
    Another specification required is arxiv metadata format. Here we use arXivRaw which is very similar to internal format stored ar arxiv ([see Open Archives Initiative (OAI) help](https://arxiv.org/help/oa)). This format includes several article attributes and we selected a few of them, but relevant for our purposes. Finally, a set can be defined for selective harvesting a particular subject, "cs" in our case. Additionally, a datestamp can be used for a period of time selection.

    With respect to data storage, the 1K-size chunks of records are saved in a text file, a record per line. The XML response from OAI is parsed and transformed into python dictionaries. When the harvest is completed, a data process transformation is performed, converting the text file into a json file ([arxiv_cs/utils.py/raw2json](../arxiv_cs/utils.py#raw2json)). After that, a minimal cleaning for abstract and title fields is done [arxiv_cs/utils.py/process_raw_ds](../arxiv_cs/utils.py#process_raw_ds).

    More details in wiki (si tic temps!)
    
6. Acknowledgments.

    This dataset was possible thanks to [arxiv.org](https://arxiv.org/) and Cornell University which maintains likely the most important open access platform to articles metadata and e-prints. Also, we have to mention the [Open Archives Initiatives](http://www.openarchives.org/) which was very helpful when harvesting the bulk, providing friendly protocols.

7. Motivation.


8. License.

    CC0 1.0 Universal (CC0 1.0) Public Domain Dedication.