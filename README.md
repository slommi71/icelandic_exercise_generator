# Generator - Exercise Excel Sheets

Based on a yaml orðabók (vocabulary) in /etc folder this simple app generates an excel file with sheets of words taken from `etc/ordabok.yaml`.

First columns contains 40 words.
The student has to fill following:

- gender of the word in second column
- third column: singular with article
- fourth column: plural without artcle
- fifth with artcle
  
the first sheet is to train nominativ, the second sheet to train accusativ.

Your own word list can be entered in `etc/ordabok.yaml` and thus adapted to your own learning progress. 

## Prerequisites

python 3.6 or higher
python modules as listed in requirements.tyt

## How to execute

``` powershell
pip install -r requirements.txt
python .\src\createnafnordsheet\app.py
```
