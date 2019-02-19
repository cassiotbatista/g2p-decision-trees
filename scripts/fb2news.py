import sys
import os
import io
import re

def usage():
	print('ta errado moça')
	print('dict.fb dict.news')

if __name__=='__main__':
	if len(sys.argv) != 3:
		usage()
		sys.exit(1)

	if os.path.isfile(sys.argv[1]):
		with io.open(sys.argv[1], 'r', encoding='utf-8') as f:
			dictionary = f.read().split('\n')[:-1]
	else:
		usage()
		print('\'%s\' is not a valid file.' % sys.argv[1])
		sys.exit(1)

	with io.open(sys.argv[2], 'w', encoding='utf-8') as f:
		for entry in dictionary:
			word, transcription = entry.split('\t')
			word = ' '.join(letter for letter in word)
			transcription = re.sub('^ ','', transcription)
			f.write('%s\t%s\n' % (word, transcription))
