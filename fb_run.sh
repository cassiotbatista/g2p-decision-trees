#!/bin/bash
#
# author: 2018
# cassio batista - cassio.batista.13@gmail.com

DT_CONTEXT=4
DT_DATADIR="data"
DICT_BASEFILENAME="dict_50k"

# TODO: path to m2m aligner
# get it from https://github.com/letter-to-phoneme/m2m-aligner
M2M_ALIGNER_GITDIR="${HOME}/git-all/m2m-aligner/" 

# fb_00: align
rm -f output/${DICT_BASEFILENAME}.old.ali
${M2M_ALIGNER_GITDIR}/m2m-aligner \
	--delX \
	-i input/${DICT_BASEFILENAME}.news \
	-o output/${DICT_BASEFILENAME}.old.ali \
	--alignerOut /tmp/nada

rm -f output/${DICT_BASEFILENAME}.ali.err
bash scripts/fix_align.sh output/${DICT_BASEFILENAME}.old.ali output/${DICT_BASEFILENAME}.new.ali
#bash ./scripts/check.sh output/${DICT_BASEFILENAME}.new.ali

# fb_01: split
python3 scripts/split_train_test.py \
		output/graphemes.list \
		output/phonemes.list \
		$DT_CONTEXT \
		output/dict_50k.new.ali \
		$DT_DATADIR > /dev/null

# fb_02: dectree
python3 dt_src/dectree.py \
	output/graphemes.list \
	output/phonemes.list \
	$DT_CONTEXT \
	$DT_DATADIR > /dev/null
