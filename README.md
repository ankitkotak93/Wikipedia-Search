I used SAX parse for parsing xml input file that was given.
After extracting data am categorizing it into 6 major fields : Title, Infobox, Body, Reference Links, External Links, Categories. 
Used my own list of stop words.
For tokenizing, regular experessions are used.
For stemming, PyStemmer is used.
Indexing is done in 6 files ( for 6 major fields as described above ):
Avg run time for indexing = 1min30secs.
Total Indexing size = 37mb.
For indexing, first I create a file in which for each 1000 documents that i extract are stored in sorted way. sample.xml generated 13 such files so total number of documents in sample.xml is 12k-13k. After creating intermediate files, i apply 2 way external merge sort to create one single indexing file for each of the fields described above. Benifits : i dont have to sort a large file in a single go, enables me to weigh my queries according to indexes created, computationally less costly. Cons : Creating intermediate files takes up extra space so its a trade off between space and speed.
My input folder would contain input xml file ( just created for my own convenience, u can give path to your own input ).
Did secondary indexing to search for a word in my created indexing.
Used heuristics to give weight to words according to their occurences in various documents.
Also applied selectivity in optimizing query response time.
