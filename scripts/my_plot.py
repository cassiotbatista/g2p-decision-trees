import sys
import os
import re

import matplotlib.pyplot as plt
import numpy as np

np.set_printoptions(precision=3)

if __name__=='__main__':
	if len(sys.argv) != 2:
		print('tá errado moça. passe o refdir')
		sys.exit(1)

	refdir = sys.argv[1] + '/'
	if not os.path.isdir(refdir):
		print('tá errado moça. passe o refdir')
		sys.exit(1)

	wer = np.zeros((5,7))
	per = np.zeros((5,7))
	for context in range(1,8):
		for holdout in range(1,6):
			erfile = '{0}/holdout_{1}/dectree.{2}.er'.format(refdir,holdout,context)
			if not os.path.isfile(erfile):
				print('%s não existe' % erfile)
				sys.exit(1)
			with open(erfile, 'r') as f:
				file_content = f.readlines()
			for line in file_content:
				if '#' not in line:
					# look for WER
					er = re.findall(r'^wer: (.*?)%', line)
					if er != []:
						wer[holdout-1][context-1] = np.float64(er.pop())
						continue

					# look for PER
					er = re.findall(r'^per: (.*?)%', line)
					if er != []:
						per[holdout-1][context-1] = np.float64(er.pop())
						continue

	wer_mean = wer.mean(axis=0)
	per_mean = per.mean(axis=0)

	wer_std = wer.std(axis=0)
	per_std = per.std(axis=0)
	
	x = np.arange(len(wer_mean))

	plt.subplot(1,2,1)
	plt.errorbar(x, wer_mean, yerr=wer_std,
			linewidth=2,
			fmt='o--', color='b', ecolor='b',
			capsize=5, capthick=2)
	#plt.title('Minha tchola', fontsize=20)
	plt.ylabel('WER (%)', fontsize=40)
	plt.grid()
	plt.xlim([-0.25, 6.25])
	plt.xticks(x, x+1, fontsize=20)
	plt.yticks(fontsize=20)
	plt.xlabel('Context size', fontsize=30)

	plt.subplot(1,2,2)
	plt.errorbar(x, per_mean, yerr=per_std,
			linewidth=2,
			fmt='s--', color='r', ecolor='r',
			capsize=5, capthick=2)
	plt.ylabel('PER (%)', fontsize=40)
	plt.grid()
	plt.xlim([-0.25, 6.25])
	plt.yticks(fontsize=20)
	plt.xticks(x, x+1, fontsize=20)
	plt.xlabel('Context size', fontsize=30)

	plt.ion()
	plt.show()
	plt.pause(0.001)

	input('eita')
