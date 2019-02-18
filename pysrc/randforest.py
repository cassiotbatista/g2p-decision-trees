import sys
import io
import os
import random
from termcolor import colored

from sklearn.ensemble import RandomForestClassifier

import graphviz

#from matplotlib.ticker import FuncFormatter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

DEGUB = 0

# https://stackoverflow.com/questions/9433240/python-matplotlib-3d-bar-plot-adjusting-tick-label-position-transparent-b
def hist3d(graphemes, phonemes, datamtx, color='b'):
	lx = len(graphemes)
	ly = len(phonemes)

	fig = plt.figure()
	ax = Axes3D(fig)
	
	xpos = np.arange(0,lx,1)    # Set up a mesh of positions
	ypos = np.arange(0,ly,1)
	xpos, ypos = np.meshgrid(xpos+0.25, ypos+0.25)
	
	xpos = xpos.flatten()   # Convert positions to 1D array
	ypos = ypos.flatten()
	zpos = np.zeros(lx*ly)
	
	dx = 0.5 * np.ones_like(zpos)
	dy = dx.copy()
	dz = datamtx.flatten()
	
	ax.bar3d(xpos, ypos, zpos, dx, dy, dz, color=color)
	
	#sh()
	ax.set_xlabel('Graphemes')
	ax.w_xaxis.set_ticks(range(lx))
	ax.w_xaxis.set_ticklabels(graphemes, rotation=90)

	ax.set_ylabel('Phonemes')
	ax.w_yaxis.set_ticks(range(ly))
	ax.w_yaxis.set_ticklabels(phonemes, rotation=90)
	
	ax.set_zlabel('Frequency')

	plt.ion()
	plt.show()
	plt.pause(0.001)

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

if __name__=='__main__':
	if len(sys.argv) < 5:
		print('tá errado moça')
		print('graph, phon, context, refdir')
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

	# check given dir
	refdir = sys.argv[4] + '/'
	if not os.path.isdir(refdir):
		print('error: %s is not a valid dir' % sys.argv[4])
		sys.exit(2)

	# load training samples
	with open('{0}/train.{1}.index'.format(refdir, context)) as f:
		train = f.read().split('\n')[:-1]

	# load test samples
	with open('{0}/test.{1}.index'.format(refdir, context)) as f:
		test = f.read().split('\n')[:-1]

	# for histogram
	match    = np.zeros((len(graphemes),len(phonemes)), dtype=np.uint64)
	mismatch = np.zeros((len(graphemes),len(phonemes)), dtype=np.uint64)

	X, Y, i = [], [], 0
	for inst in train:
		sample = list(map(int, inst.split()[:-1]))
		label  = int(inst.split()[-1])

		X.append(sample)
		Y.append(label)
		i += 1
		print('\r%d' % i, end='')
	print()

	# train decision tree 
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(X, Y)

	logfile = refdir + 'dectree_log.log'
	if os.path.isfile(logfile):
		os.remove(logfile)

	words = 0
	delim_count = 0
	delim_index = graphemes.index('#')
	s, n = 0, 0
	wer, per = 0, []
	subs, total = 0, 0
	graph, phon_orig, phon_pred = '', '', ''
	for inst in test:
		sample     = list(map(int, inst.split()[:-1]))
		label_orig = int(inst.split()[-1])
		label_pred = int(clf.predict(np.array([sample]))[0])

		graph     += '%s'  % graphemes[sample[context]]
		phon_orig += '%s ' % phonemes[label_orig]
		phon_pred += '%s ' % phonemes[label_pred]

		n += 1
		total += 1

		# mismatch else match
		if label_orig != label_pred:
			s += 1
			subs += 1
			mismatch[label_orig][label_pred] += 1
		else:
			match[label_orig][label_pred] += 1

		if DEGUB:
			print('(%02d) %-3s %-2s (%02d) -> ' % \
					(sample[context], graphemes[sample[context]],
					phonemes[label_orig], label_orig),
					end='')
			print(sample, label_pred)

		delim_count += sample.count(delim_index)
		#print(sample, delim_count, sample.count(delim_index), context)

		if delim_count == context * (context+1):
			words += 1
			per.append(100.0*s/n)
			if per[-1] > 0.0:
				wer += 1
				if DEGUB:
					print('[%s] per: %.3f%% (%d/%d)' % (graph, per[-1],s,n))
					for o, r in zip(phon_orig.split(), phon_pred.split()):
						print('%-4s' % o, end='') if o == r else print(colored('%-4s' % o, 'green', attrs=['bold']), end='')
					print()
					for o, r in zip(phon_orig.split(), phon_pred.split()):
						print('%-4s' % r, end='') if o == r else print(colored('%-4s' % r, 'red', attrs=['bold', 'blink']), end='')
					print()
				else:
					with io.open(logfile, 'a', encoding='utf-8') as f:
						f.write('[%s] per: %.3f%% (%d/%d)\n' % (graph,per[-1],s,n))
						f.write('o: ')
						for o, r in zip(phon_orig.split(), phon_pred.split()):
							f.write('%-4s' % o);
						f.write('\n')
						f.write('r: ')
						for o, r in zip(phon_orig.split(), phon_pred.split()):
							f.write('%-4s' % r);
						f.write('\n')
			s, n, delim_count = 0, 0, 0
			graph, phon_orig, phon_pred = '', '', ''
			if DEGUB:
				print('========================')
	if DEGUB:
		print('wer: %.4f%% (%d/%d)' % ((100.0*wer/words),wer,words))
		print('per: %.4f%% (%d/%d)' % ((100.0*subs/total),subs,total))
		hist3d(graphemes, phonemes, match)
		hist3d(graphemes, phonemes, mismatch, 'r')
		input('digita aí disgraaaaaça')
	else:
		with io.open(logfile, 'a', encoding='utf-8') as f:
			f.write('wer: %.4f%% (%d/%d)\n' % ((100.0*wer/words), wer, words))
			f.write('per: %.4f%% (%d/%d)\n' % ((100.0*subs/total), subs, total))

	print('desenhando esta disgraaaaaça')
	dot_data = tree.export_graphviz(clf, out_file=None,
			leaves_parallel=True,
			filled=True, rounded=True, special_characters=True,
			class_names=np.array(phonemes))
	graph = graphviz.Source(dot_data) 
	graph.render("/tmp/iris")
	#graph.view()
