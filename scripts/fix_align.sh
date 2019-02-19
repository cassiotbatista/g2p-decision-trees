rm -f $2
echo "sorting"
sort -R $1 > tmp 
mv tmp $1
n=$(cat $1 | wc -l)
i=1
while read line
do
	new=$(echo $line |\
		sed 's/:n|h/|n:h/g' |\
		sed 's/o~:j~|_/o~|j~/g' |\
		sed 's/q|u:/q:u|/g' |\
		sed 's/|j:s/:j|s/g' |\
		sed 's/|m:/:m|/g' |\
		sed 's/k:z/k:s/g' |\
		sed 's/j:j/i/g' |\
		sed 's/_:j/e/g' |\
		sed 's/s|s:/s:s|/g' | sed 's/:s|s/|s:s/g')

	# treat gu
	if [[ "$new" == *"g|u:"[aeiouáéíóúãõâêô]* ]]
	then
		new=$(echo $new | sed 's/g|u:/g:u|/g')
	fi

	# treat h
	if [[ "$new" == "h:"* ]]
	then
		grapheme=$(echo $new | cut -d ' ' -f 1 | sed 's/h:/h|/g')
		phoneme="_|$(echo $new | cut -d ' ' -f 2)"
		new="$grapheme $phoneme"
	fi

	# treat |n:CONS
	if [[ "$new" == *"n:"[cdftgqsj]* ]]
	then
		new=$(echo $new |\
			sed 's/|n:c/:n|c/g' |\
			sed 's/|n:d/:n|d/g' |\
			sed 's/|n:f/:n|f/g' |\
			sed 's/|n:t/:n|t/g' |\
			sed 's/|n:g/:n|g/g' |\
			sed 's/|n:q/:n|q/g' |\
			sed 's/|n:s/:n|s/g' |\
			sed 's/|n:j/:n|j/g')
	fi

	echo $new | sed 's/ /\t/g' >> $2
	echo -ne "\r$i/$n"
	i=$((i+1))
done < $1
echo
