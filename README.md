# MatchPhrases
RESTful microservice to parse a sentence looking for words from a list

# The task

Create a REST micro-service that takes as input a string 
parameter and returns a list of matched phrases from a dictionary list.

## Requirements and running

All the code is written using Python 3.6.
The server runs using **CherryPy** framework, which is the main dependency for this code.
An extra version of the server which experiments with noun chunks also uses **spaCy 2.0**. 
The scripts config_Linux.sh and config_OSX.sh configure a working Conda environment for the project and take care of installing all the relevant libraries. 
The two scripts also install and configure the latest version of Conda for the appropriate OS.
The server can be also configured manually and run on any environment which has Python 3.6, CherryPy and (for the noun chunk server) spaCy 2.0 installed.
After configuring everything, the command
```
    python run.py
```
will launch an instance of the server on port 8080. GET requests can then be made at the URI 
```
    localhost:8080/find_matches?text=input_text
```
where "input_text" is the text to parse. 
The server responds with a JSON representation of the list of matched phrases. 


## Code structure

The file **run.py** launches the server on port 8080. It is a very simple script and contains a *config* dictionary which can be used to customize some of the parameters of the server (number of threads, listening port and whether the autorun option should be enabled). Autorun is currently disabled for two reasons:

* It makes the server run slightly slower
* It doesn't work with the spaCy library due to a bug in the latter in handling the *hasattr* method. 

The main class of the project is the MatchPhrases class contained in the file **MatchPhrases.py**. 
The class loads the list of phrases to detect and exposes the *find_matches* method, which takes as input the text parameter and returns a list of phrases contained in the input text.
A simple check is done to verify that the list of matches returned doesn't contain overlapping phrases (i.e. "sore" and "sore throat"), but just the most specific one (i.e. ["sore throat"]). 
Some unit tests for the class are located in the **test_match_phrases.py** file. These tests verify whether common cases work properly and also do some very simple stress test to verify whether the approach scales to a bigger wordlist / is able to parse a very long sentence in a reasonable amount of time.

## Extra 

The class **MatchNounChunks.py** implements a slightly more sophisticated version of the matching: noun chunks are extracted from the input text using the spaCy library and then each noun chunk is checked against the list of phrases. To make the research more efficient, the phrase list is sorted during the server setup and the search is implemented through a binary search algorithm. 

## Performance and behaviour considerations

The following table shows performances for the two classes (in terms of avg. response time in seconds) with various scenarios. (the file **speed_test.py** contains a very simple code snippet used to run these tests):

|                         | Baseline   Class  | Noun Chunk Class  |
| -------------           | ----------------- | ----------------- |
| Simple request          | 0.009s            | 0.009s            |
| 1000 words input text   | 0.03              | 0.14s             |
| 10x larger phrase list  | 0.08              | 0.009s            |

As the table highlights, the simple implementation works quite wekk even with large input texts, but has a lower average response time when the phrases list gets larger (in facts, the matching algorithm is linear wrt the number of phrases).
The noun chunk based algorithm, on the other hand, has a major slowdown for a very large input text (in facts, its complexity is O(log p) * O(w), where p and w are the size of the phrase list and the input words respectively.), but works very well with large phrase lists.
In terms of scalability, the second algorithm is probably more reliable, since the word list is more likely to grow larger, while very large input texts are less likely.
One last consideration can be done about the behaviour of the two classes: while the baseline one will always extract phrases correctly if it detects them, the second one relies on spaCy's noun chunk extraction, which sometimes will cause false negatives (e.g. "I have a bad coff" will be extracted as "a bad coff" and will not consider "bad coff"). This behaviour could be fixed by considering a more fine-grained noun chunk extraction, possibly exploring the dependency tree.
