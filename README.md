To get running:

First install a virualenv and all the python requirements:
# Setup
`pip install virtualenv` 
`virtualenv venv` 
`source venv/bin/activate` 
`pip install -r requirements.txt` 

Note: Must use python2 - if you get a print error:
  File "Driver.py", line 55
    print "Pickle found at: " + PICKLE_DIR + picklename
virtualenv has installed python3


Required 3rd party downloads:
    -L2 Syntactic Complexity Analyzer from dropbox link (email vadmas@gmail.com for permission). It's been modified to be turned into a python package but user can also download from web here: http://www.personal.psu.edu/xxl13/downloads/l2sca.html
    -Stanford parser: http://nlp.stanford.edu/software/stanford-parser-full-2015-12-09.zip


-Also download the nltk packages "stopwords", "punkt", "averaged_perceptron_tagger",  using the NLTK Downloader 



