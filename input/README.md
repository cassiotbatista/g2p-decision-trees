## Input Resources for G2P for PT\_BR using Decision Trees
 - `wordlist_50k.txt`: list of 50 thousands words (grahemes) extracted from Natura do Minho's huge list     
 - `seed_lexicon.dict`: phonetic dictionary generated with [FalaBrasil Group's G2P software](https://gitlab.com/fb-nlp/nlp)     
 - `dict_50k.news`: phonetic dictionary in news format generated from FalaBrasil's dict        

To convert FalaBrasil's seed lexicon to a phonetic dictionary inthe news format,
you can use the script `fb2news.py` which is located inside the `scripts/`
folder. To create your own seed lexicon, however, you need to follow the
instructions on FalaBrasil Group's official GitLab page as indicated in the URL
link in the list above.

__Copyright (2005-2019) Grupo FalaBrasil__    
__Universidade Federal do Pará__     
Cassio Batista - cassio.batista.13@gmail.com
