#!/bin/bash
#
# author: 2018
# cassio batista - cassio.batista.13@gmail.com
# edited on feb 2019

DT_CONTEXT=4
DT_DATADIR="data"
DICT_BASEFILENAME="dict_50k"

# TODO: path to m2m aligner
# get it from https://github.com/letter-to-phoneme/m2m-aligner
M2M_ALIGNER_GITDIR="${HOME}/git-all/m2m-aligner/" 

# fb_00: align graphemes and phonemes
mkdir -p output
rm -f output/${DICT_BASEFILENAME}.old.ali
${M2M_ALIGNER_GITDIR}/m2m-aligner \
	--delX \
	-i input/${DICT_BASEFILENAME}.news \
	-o output/${DICT_BASEFILENAME}.old.ali \
	--alignerOut /tmp/nada

rm -f output/${DICT_BASEFILENAME}.old.ali.err
bash scripts/fix_align.sh output/${DICT_BASEFILENAME}.old.ali output/${DICT_BASEFILENAME}.new.ali
#bash ./scripts/check.sh output/${DICT_BASEFILENAME}.new.ali

bash scripts/ali2instance.sh output/${DICT_BASEFILENAME}.new.ali

# fb_01: split train and test
python3 scripts/split_train_test.py \
		res/graphemes.list \
		res/phonemes.list \
		$DT_CONTEXT \
		output/dict_50k.new.ali \
		$DT_DATADIR > /dev/null

# fb_02: decision tree
python3 dt_src/dectree.py \
	res/graphemes.list \
	res/phonemes.list \
	$DT_CONTEXT \
	$DT_DATADIR > /dev/null
