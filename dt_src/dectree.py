import sys
sys.path.insert(0, 'pysrc')

import io
import os
import random
from termcolor import colored

from sklearn import tree
import graphviz

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

from commons import *

DEGUB = 0

def dt_print_diffs(graph, orig, pred, per, s, n):
	print('[%s] per: %.3f%% (%d/%d)' % (graph, per, s, n))
	for o, r in zip(orig.split(), pred.split()):
		if o == r:
			print('%-4s' % o, end='')
		else:
			print(colored('%-4s' % o, 'green', attrs=['bold']), end='')
	print()
	for o, r in zip(orig.split(), pred.split()):
		if o == r:
			print('%-4s' % r, end='')
		else:
			print(colored('%-4s' % r, 'red', attrs=['bold', 'blink']), end='')
	print()

def dt_save_diffs(filename, graph, orig, pred, per, s, n):
	with io.open(filename, 'a', encoding='utf-8') as f:
		f.write('[%s] per: %.3f%% (%d/%d)\n' % (graph, per, s, n))
		f.write('o: ')
		for o, r in zip(orig.split(), pred.split()):
			f.write('%-4s' % o);
		f.write('\n')
		f.write('r: ')
		for o, r in zip(orig.split(), pred.split()):
			f.write('%-4s' % r);
		f.write('\n')

def dt_train(refdir, context):
	# load training samples
	with open('{0}/train.{1}.index'.format(refdir, context)) as f:
		train = f.read().split('\n')[:-1]

	X = []
	Y = [] 
	i = 0
	for inst in train:
		sample = list(map(int, inst.split()[:-1]))
		label  = int(inst.split()[-1])

		X.append(sample)
		Y.append(label)
		i += 1
		print('\r%d' % i, end='')
	print()

	# create and train decision tree 
	clf = tree.DecisionTreeClassifier()
	clf = clf.fit(X, Y)

	return clf

def dt_test(clf, graphemes, phonemes, context, refdir):
	# for histogram
	pmatch    = np.zeros((len(phonemes),len(phonemes)), dtype=np.uint64)
	pmismatch = np.zeros((len(phonemes),len(phonemes)), dtype=np.uint64)

	gmatch    = np.zeros((len(graphemes),len(phonemes)), dtype=np.uint64)
	gmismatch = np.zeros((len(graphemes),len(phonemes)), dtype=np.uint64)

	# load test samples
	with open('{0}/test.{1}.index'.format(refdir, context)) as f:
		test = f.read().split('\n')[:-1]

	erfile  = '{0}/dectree.{1}.er'.format(refdir, context)
	misfile = '{0}/dectree.{1}.mis'.format(refdir, context)

	words = 0
	delimiter = graphemes.index('#')
	s, n = 0, 0
	wer, per = 0, 0
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
			pmismatch[label_orig][label_pred] += 1
		else:
			pmatch[label_orig][label_pred] += 1

		#if DEGUB:
		#	print('(%02d) %-3s %-2s (%02d) -> ' % \
		#			(sample[context], graphemes[sample[context]],
		#			phonemes[label_orig], label_orig),
		#			end='')
		#	print(sample, label_pred)

		if sample[context:].count(delimiter) == context:
			words += 1
			per = 100.0*s/n
			if per > 0.0:
				wer += 1
				if DEGUB:
					dt_print_diffs(graph, phon_orig, phon_pred, per, s, n)
				else:
					dt_save_diffs(misfile, graph, phon_orig, phon_pred, per, s, n)
			s, n = 0, 0
			graph, phon_orig, phon_pred = '', '', ''
			#if DEGUB:
			#	print('========================')
	if DEGUB:
		print('wer: %.4f%% (%d/%d)' % ((100.0*wer/words),wer,words))
		print('per: %.4f%% (%d/%d)' % ((100.0*subs/total),subs,total))
		#hist3d(phonemes, phonemes, pmatch)
		#hist3d(phonemes, phonemes, pmismatch, 'r')
		hist2d(phonemes, pmatch.diagonal(), 'g')
		mishist(phonemes, pmismatch, 'r')
		input('digita aí disgraaaaaça')
	else:
		with io.open(misfile, 'a', encoding='utf-8') as f:
			f.write('###########################################################\n');
		with io.open(erfile, 'a', encoding='utf-8') as f:
			f.write('wer: %.4f%% (%d/%d)\n' % ((100.0*wer/words), wer, words))
			f.write('per: %.4f%% (%d/%d)\n' % ((100.0*subs/total), subs, total))
			f.write('###\n');

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

	if not DEGUB:
		print('[%s] set DEBUG flag "True" to enable verbose mode.' % sys.argv[0])

	# train routine
	print('training DT...')
	clf = dt_train(refdir, context)

	## draw the fucking tree
	#print('drawing DT...')
	#draw_tree(clf, depth=None)

	# test tree
	print('testing DT...')
	dt_test(clf, graphemes, phonemes, context, refdir)
