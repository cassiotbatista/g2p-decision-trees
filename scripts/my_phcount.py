import sys

DEGUB = False

monophones = {
	"a" :0, "a~":0, "b" :0, "d" :0,
	"dZ":0, "e" :0, "e~":0, "E" :0, 
	"f" :0, "g" :0, "i" :0, "i~":0,
	"j" :0, "j~":0, "J" :0, "k" :0, 
	"l" :0, "L" :0, "m" :0, "n" :0, 
	"o" :0, "o~":0, "O" :0, "p" :0,
	"r" :0, "R" :0, "s" :0, "S" :0, #"sp":0,
	"t" :0, "tS":0, "u" :0, "u~":0, 
	"v" :0, "w" :0, "w~":0, "X" :0, 
	"z" :0, "Z" :0
}

if DEGUB:
	for p in monophones:
		print '%3s -> %6d' % (p, monophones[p])

i=0
n=640390
with open('res/phons', 'r') as f:
	for line in f:
		for phone in line.split():
			for mono in monophones:
				if mono == phone:
					monophones[mono] += 1
					break
		i += 1
		sys.stdout.write('\r%d/%d' % (i,n))
		sys.stdout.flush()
print

with open('res/stats.txt', 'w') as f:
	for key, val in sorted(monophones.iteritems(), key=lambda (k,v): (v,k), reverse=True):
		f.write('%-2s %6d\n' % (key,val))
