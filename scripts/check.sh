skip_graph=(
	"n:h" "c:h" "l:h" "r:r" "s:s" "q:u" "g:u" "s:c" "s:ç" "x:c" # digrafos
	"a:n" "e:n" "i:n" "o:n" "u:n" "â:n" "ê:n" "í:n" "ô:n"
	"a:m" "e:m" "i:m" "o:m" "u:m" "â:m" "ê:m" "í:m" "ô:m"
	"a:j" "k:s" "i:e"
)

skip_phon=(
	"k:s" "a:j" "e:j" "E:j" "i:j" "o:j" "O:j" "u:j"
)

sort -R $1 > tmp

while read line ; do
	grapheme=$(echo $line | cut -d ' ' -f 1)
	phoneme=$(echo $line | cut -d ' ' -f 2)

	token_count=0
	pair_count=0
	for token in $(echo $grapheme | sed 's/|/ /g') ; do
		if [[ "$token" == *":"* ]] ; then
			token_count=$((token_count+1))
			for pair in ${skip_graph[@]} ; do
				if [[ "$token" == "$pair" ]] ; then
					pair_count=$((pair_count+1))
					break
				else
					p=$token
				fi
			done
		fi
	done
	if [[ $pair_count -lt $token_count ]] ; then
		echo "$p $line" | sed 's/ /\t/g' | GREP_COLOR='1;32' grep ':' --color=always
	fi

	token_count=0
	pair_count=0
	for token in $(echo $phoneme | sed 's/|/ /g') ; do
		if [[ "$token" == *":"* ]] ; then
			token_count=$((token_count+1))
			for pair in ${skip_phon[@]} ; do
				if [[ "$token" == "$pair" ]] ; then
					pair_count=$((pair_count+1))
					break
				else
					p=$token
				fi
			done
		fi
	done
	if [[ $pair_count -lt $token_count ]] ; then
		echo "$p $line" | sed 's/ /\t/g' | grep ':' --color=auto
	fi
done < tmp

rm -f tmp
