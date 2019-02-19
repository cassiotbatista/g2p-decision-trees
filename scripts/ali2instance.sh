#!/bin/bash
#
# author: 2018
# cassio batista - cassio.batista.13@gmail.com
# edited on feb 2019

i=1
n=$(wc -l $1 | awk '{print $1}')
while read line
do
	grapheme=$(echo $line | awk '{print $1}' | sed 's/|/ /g')
	phonemes=$(echo $line | awk '{print $2}' | sed 's/|/ /g')
	for letter in $grapheme ; do echo $letter >> g.tmp ; done
	for phone  in $phonemes ; do echo $phone  >> p.tmp ; done
	echo -ne "\r$i / $n"
	i=$((i+1))
done < $1
echo

echo "sorting and uniquing graphemes... "
sort g.tmp | uniq > res/graphemes.list
echo "sorting and uniquing phonemes... "
sort p.tmp | uniq > res/phonemes.list

echo "done! check 'res/graphemes.list' and 'res/phonemes.list' files"

rm *.tmp
