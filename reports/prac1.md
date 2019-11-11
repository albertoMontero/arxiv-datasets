# Arxiv-cs dataset Report.

1. Context.

    ArXiv.org is widely known to be one of the first initiatives towards open access for scientific publishing. Although it is not a peer reviewed system, a group of moderators for each area review the submissions and may re-categorize any considered off-topic or reject not scientific papers. This garanties a certain quality in both, content and categorization. 
    
    ArXiv began in 1991 as a physics archive (accessible via FTP) called LANL (Los Alamos National Laboratory) and soon expanded to include other fields like astronomy, mathematics, computer science, quantitative biology and, most recently, statistics. In 1993 was opened to the World Wide Web and in 2001 was hosted by Cornell University and changed the name to arXiv.org.

    The repository contains several subject specific repositories including the Computer Research Repository (CoRR) with more that 240K papers submitted (November 2019). The full repository contains 
    nowadays about 1,600,000 papers. It shares articles metadata and e-prints and offers some APIs possibilities to gather data.

2. Title of dataset. 
   
   Arxiv-cs dataset, a complete computer science ArXiv articles metadata dataset.

3. Description of dataset.

    Arxiv-cs contains about 240k records of articles metadata from ArXiv [Computing Research Repository (CoRR)](https://arxiv.org/corr). It contains a few relevant fields extracted from computer science papers, including identifier, title, abstract and categories.

4. Picture. 
   
    The picture is presented in the project's main page and has been implemented in notebook [image.ipynb](../notebooks/image/image.ipynb). It uses wordcloud ans Scrapy python packages to generate a word cloud style image with last year papers text from title and abstracts, filtering by stop-words and verbs (but keeping "learning" verb) and using the 100 most frequent words.

5. Content.

    Arxiv-cs is presented as a json file containing the following attributes (all of them as a string):
    * **id**: ArXiv internal article identifier.
    * **title**: title of article.
    * **abstract**: abstract of article.
    * **categories**: list of category tags the article was submitted. White space separated, with primary category in first position. Notice that we have tags coming from other subjects like physics, statistics, math, etc.

    The collecting date interval of records includes from the beginning of CoRR repository creation (1993-01) to the end of October 2019 (2019-10). Date is not present in the dataset but it can be easily parsed from identifier. We provide a method to extract date and show an example in notebooks/eda folder.

    ArXiv provides several APIs services enabling developers the creation of valuable services to scientists and general public. When harvesting large amounts of data, the ArXiv Bulk Data Access services are recommended. In this project we use the [OAI protocol for metadata harvesting](https://arxiv.org/help/oa) (OAI-PMH). ArXiv is a registered OAI-PMH data-provider, providing access to metadata for all articles, updated daily with new articles. This is the preferred way to bulk-download or keep an up-to-date copy of ArXiv metadata. ArXiv suports [OAI_PMH v2.0 protocol](http://www.openarchives.org/OAI/2.0/openarchivesprotocol.htm).

    The harvest was performed with the python script [arxiv_cs/harvest.py](../arxiv_cs/harvest.py), which implements all protocols and requests needed to harvest the ArXiv Computer Science repository. Some examples of use can also be found in notebooks [03_harvest_01.ipynb](../notebooks/experimental/03_harvest_01.ipynb) and [03_harvest_02.ipynb](../notebooks/experimental/03_harvest_02.ipynb) which were implemented as helpers in developing process.

    Briefly, harvest.py specifies the OAI ListRecords request protocol which returns chunks of 1000 records and a resumption token. This token is used in the next request to resume the download. Finally an empty resumption token is returned meaning that the complete bulk download is finished. The script define a delay of 15 seconds (at least 10 seconds is required) between requests and the complete bulk for CoRR is downloaded in about 90 minutes (about 240K articles metadata).
    Another specification required is ArXiv metadata format. Here we use arXivRaw which is very similar to internal format stored ar ArXiv ([see Open Archives Initiative (OAI) help](https://arxiv.org/help/oa)). This format includes several article attributes and we selected a few of them, but relevant for our purposes. Finally, a set can be defined for selective harvesting a particular subject, "cs" in our case. Additionally, a datestamp can be used for a period of time selection.

    With respect to data storage, the 1K-size chunks of records are saved in a text file, a record per line. The XML response from OAI is parsed and transformed into python dictionaries. When the harvest is completed, a data process transformation is performed, converting the text file into a json file ([arxiv_cs/utils.py/raw2json](../arxiv_cs/utils.py#raw2json)). After that, a minimal cleaning for abstract and title fields is done [arxiv_cs/utils.py/process_raw_ds](../arxiv_cs/utils.py#process_raw_ds).

    More details in wiki.
    
6. Acknowledgments.

    This dataset was possible thanks to [arxiv.org](https://arxiv.org/) and its owner, Cornell University which maintains likely the most important open access platform to articles metadata and e-prints. Also, we have to mention the [Open Archives Initiatives](http://www.openarchives.org/) which was very helpful when harvesting the bulk, providing friendly protocols.

7. Inspiration.

    Text classification and topic modeling are two very prominent machine learning tasks nowadays. In recent years, new deep learning based approaches have shown state of the art for such kind of tasks, with language modeling and knowledge transfer methods as cornerstones for current methodologies. Still, text classification is a hard task, specially in multi-class and multi-label problems.

    We shared arxiv-cs dataset with the hope to help researches and practitioners to develop text classifications models under a challenge dataset with about 160 different categories or labels. Although classifiying a papers into a category might be to some extend somewhat subjective, arXiv categories have been annotated by paper authors and reviewed by arXiv moderators, so we expect a high quality of labels.

    Tackling the complete multi-class and multi-label task is quite challenge, specially the multi-label problem seems hard. We suggest to use the complete dataset to define incrementally difficulty kind of tasks. For instance, starting by binary single label classification tasks using primary category as labels. A quick exploratory data analysis of categories distributions shows that some categories or subjects might be harder to classify than others when tackling binary tasks, by observing co-occurrence of categories in records, which supports our intuition. For instance, we can see that classifying between Computer Vision and Machine Learning is harder than between Computer Vision and Computation and Language. 

    Notice that we can also use the arxiv-cs dataset to evaluate text clustering or topic modeling models.

    We hope this dataset helps to define interesting sub-sets and tasks to obtain deeper insights in text classifications problems. 

    The code provided in this project also allows to extend easily the dataset to other subjects or fields contained in arXiv.org.


8.  License.

    We distribute this repository (but data folder) under MIT license, which is the one most recognized open source licenses. It is short and easy to read and quite permissive. 
    The data folder containing the datasets is under CC0 1.0 license, which is the arXive license for archive metadata.

9.  Code

    See [arxiv-cs project](../arxiv_cs/)


10. Dataset

    See [arxiv-cs dataset]()

