import sys
import os
import io
import random

DEGUB = 0

def load_graph(filename):
	if os.path.isfile(filename):
		with io.open(filename, 'r', encoding='utf-8') as f:
			graphemes = f.read().split('\n')[:-1]
			graphemes.append(u'#') # delimiter to avoid out-of-bounds
		return graphemes
	return -1

def load_phons(filename):
	if os.path.isfile(filename):
		with io.open(filename, 'r', encoding='utf-8') as f:
			phonemes = f.read().split('\n')[:-1]
		return phonemes
	return -1

def load_data(filename):
	if os.path.isfile(filename):
		with io.open(filename, 'r', encoding='utf-8') as f:
			dictionary = f.read().split('\n')[:-1]
		return dictionary
	return -1

def split_train_test(data, graphemes, phonemes, context, outdir, train_percent=80):
	n = len(data)
	n_train = n*train_percent/100
	n_test  = n-n_train

	# delete any previous files
	prefixes, suffixes = ['train', 'test'], ['char', 'index']
	for pref in prefixes:
		for suff in suffixes:
			filename = '{0}/{1}.{2}.{3}'.format(outdir, pref, context, suff)
			if os.path.isfile(filename):
				os.remove(filename)

	i = 0
	for entry in data:
		i += 1
		word, trans = entry.split('\t')
		
		delim=''
		for cont in range(context):
			delim += '#|'

		word = (delim + word + delim.rstrip('|')).split('|')
		trans = trans.rstrip('|').split('|')

		prefix = outdir
		if random.randrange(100) < train_percent:
			prefix += 'train.' + str(context)
		else:
			prefix += 'test.' + str(context)

		for pos in range(len(trans)):
			instance = word[pos:pos+2*context+1]
			label = trans[pos]

			instance_index = [graphemes.index(index) for index in instance]
			label_index = phonemes.index(label)

			print(prefix, instance, label) if DEGUB else print('\r%d/%d' % (i,n), end='')
			sys.stdout.flush()

			with io.open(prefix + '.char', 'a', encoding='utf-8' ) as f:
				for inst in instance:
					f.write('%-4s' % inst)
				f.write('%3s\n' % label)

			with open(prefix + '.index', 'a') as f:
				for inst in instance_index:
					f.write('%-3d' % inst)
				f.write('%2d\n' % label_index)
	print('')
	return n

if __name__ == '__main__':
	if len(sys.argv) < 6:
		print('tá errado moça')
		print('graph, phon, context, indata, outdir')
		sys.exit(1)

	# load list of modified graphemes 
	graphemes = load_graph(sys.argv[1])
	if graphemes == -1:
		print('error: %s is not a valid file' % sys.argv[1])
		sys.exit(2)

	# load list of modified phonemes
	phonemes = load_phons(sys.argv[2])
	if phonemes == -1:
		print('error: %s is not a valid file' % sys.argv[2])
		sys.exit(2)

	context = int(sys.argv[3])

	data = load_data(sys.argv[4])
	if data == -1:
		print('error: %s is not a valid file' % sys.argv[3])
		sys.exit(2)

	directory = sys.argv[5] + '/'
	if not os.path.isdir(directory):
		os.mkdir(directory)

	if not DEGUB:
		print('[%s] set DEBUG flag "True" to enable verbose mode.' % sys.argv[0])
	split_train_test(data, graphemes, phonemes, context, directory)

