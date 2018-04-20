#Rule Based POS Tagging

https://en.wikipedia.org/wiki/Part-of-speech_tagging
<br/>
https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
<br/>

A POS-tagged training file POSTaggedTrainingSet.txt, that has been tagged with POS tags
from the Penn Treebank POS tagset. Using this POS tagged file to compute for each word w the tag t that maximizes P(t|w).<br/>

Task:
	Retag the training file with POS tags that are most probable for a given word. Compute the error rate by comparing the retagged file against the original tagged file.<br/>
<br/>
	Now perform error analysis to find the top-5 erroneously tagged words. Write at least five rules to do a better job of tagging these top-5 erroneously tagged words, and show the difference in error rates.<br/>

python main.py<br/>
Output:<br/>
file1.txt  --> text file with only words.<br/>
file2.txt  --> text file contains words tagged with most probable tag.(without applying rules)<br/>
file3.txt  --> text file contains words tagged with all the rules applied.<br/>


