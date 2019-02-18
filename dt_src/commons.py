import io
import os
import graphviz

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def draw_tree(clf, name='iris', depth=3):
	print('desenhando esta disgraaaaaça')
	dot_data = tree.export_graphviz(clf, out_file=None,
			leaves_parallel=True, max_depth=depth,
			filled=True, rounded=True, special_characters=True,
			class_names=np.array(phonemes))
	graph = graphviz.Source(dot_data) 
	graph.render("/tmp/" + name)

def mishist(phonemes, datamtx, color='b'):
	lut = {}
	for i in range(datamtx.shape[0]):
		for j in range(datamtx.shape[1]):
			if datamtx[i][j] > 0:
				key = (i,j)
				if key in lut:
					lut[key] += datamtx[i][j]
				else:
					lut[key]  = datamtx[i][j]

	newphonemes = []
	datavec = []
	predicted = []
	for key in sorted(lut, key=lut.get, reverse=True):
		newphonemes.append(phonemes[key[0]])
		predicted.append(phonemes[key[1]])
		datavec.append(lut[key])

	rotation = 0
	newphonemes = newphonemes[:len(newphonemes)//2]
	datavec = datavec[:len(datavec)//2]
	predicted = predicted[:len(predicted)//2]

	x = np.arange(len(newphonemes))
	fig, ax = plt.subplots()

	plt.bar(x, datavec, color=color)
	plt.xlabel('Original Phonemes', fontsize=28)
	plt.ylabel('Predicted Phonemes', fontsize=28)
	
	ax.set_xticks(x+0.4)
	ax.set_xticklabels(newphonemes, fontsize=20, rotation=rotation)
	ax.set_xlim(-0.25, len(x))

	ax2 = ax.twiny()
	ax2.set_xlim(ax.get_xlim())
	ax2.set_xticks(x+0.4)
	ax2.set_xticklabels(x+1)

	print(len(x),len(datavec),len(predicted))
	for i, value, phone in zip(x, datavec, predicted):
		if value < 8:
			offset = value*0.4
		elif value < 20:
			offset = value*0.2
		elif value < 50:
			offset = value*0.08
		else:
			offset = value*0.02
		ax.text(i+0.3, value+offset, phone, fontsize=20)

	mng = plt.get_current_fig_manager()
	mng.full_screen_toggle()

	ax.grid()
	plt.ion()
	plt.show()
	plt.pause(0.001)

def hist2d(phonemes, datavec, color='b'):
	lut = {}
	for key, value in zip(phonemes, datavec):
		lut[key] = value

	newphonemes = []
	datavec = []
	for key in sorted(lut, key=lut.get, reverse=True):
		newphonemes.append(key)
		datavec.append(lut[key])

	rotation = 0
	newphonemes = newphonemes[:len(newphonemes)//2]
	datavec = datavec[:len(datavec)//2]

	x = np.arange(len(newphonemes))
	fig, ax = plt.subplots()

	plt.bar(x, datavec, color=color)
	plt.xlabel('Phonemes', fontsize=28)
	plt.ylabel('Frequency', fontsize=28)
	
	ax.set_xticks(x+0.4)
	ax.set_xticklabels(newphonemes, fontsize=20, rotation=rotation)
	ax.set_xlim(-0.25, len(x))
	
	ax2 = ax.twiny()
	ax2.set_xlim(ax.get_xlim())
	ax2.set_xticks(x+0.4)
	ax2.set_xticklabels(x+1)
	
	mng = plt.get_current_fig_manager()
	mng.full_screen_toggle()
	
	ax.grid()
	plt.ion()
	plt.show()
	plt.pause(0.001)

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
	ax.set_xlabel('Phonemes (original)')
	ax.w_xaxis.set_ticks(range(lx))
	ax.w_xaxis.set_ticklabels(phonemes, rotation=90)

	ax.set_ylabel('Phonemes (predicted)')
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
