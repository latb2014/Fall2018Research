# Fall2018Research

The NLPWebsite folder contains all of the website files for Mattia's NLP website which can also be found at this url as a codepen project under my username blattimer https://codepen.io/blattimer/project/editor/ALNRxL#

The WebScraping folder contains all of the files used for my web scraping project. These are written in Python 3. The scraper is run from WebCrawler.py which outputs three files using the pickle library, occurance, connnections, and levels. graphTests.py will generate interactive graphs from the three output files when run using the bokeh python library. Further details of the algorithms used can be found in my final paper.

WebCrawler.py starts by taking in all of the urls from conspiracy_submissions.txt which was too big to upload to github but can be aquired from Mattia or I.

Initial results can be found in WebScraping/Graphs folder which contains all of the interactive graphs referenced in my final paper. The extra python files are the ones that I used to get some extra data from the pickled files outputted by WebCrawler.py. 
