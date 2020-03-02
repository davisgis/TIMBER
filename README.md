# TIMBER
Tensor Induced Multilingual knowledge Base Entity Resolution (TIMBER)

TIMBER is a tool created by Anthony D. Davis, Assistant Professor of Computer Science at Lyon College.
TIMBER is designed for scholars in Digital Humanities to create a simple knowledge base and tag large corpora of domain specific texts.

Details of its creation, use, etc can be found in the following dissertation: https://github.com/davisgis/TIMBER/blob/master/20191115DavisDissertationFinalSubmittedCopy.pdf

Reference:
A. D. Davis, “Combing Texts: A Quest to Increase the Timeliness and Accuracy of Geotagging Multilingual Toponyms and Tagging Persons in Large Corpora Using Tensors for Disambiguation,” Ph.D. Dissertation, Engineering and Information Technology, University of Arkansas at Little Rock, 2019.

Installation Notes

INSTALL:
pip install pypdf2
pip install hickle
pip install cltk
pip install nltk

NOTE 1 (Windows):
Make sure to place lemmata file in c:\\username\cltk_data\greek\model\greek_models_cltk\lemmata\greek_lemmata_cltk.py

NOTE 2 (Windows):
Add the following paths
C:\Texts\AuthorityFile
C:\Texts\DataFiles
C:\Texts\Results\Candidates

Note 3: 
Flags: English/Greek needs to be set
