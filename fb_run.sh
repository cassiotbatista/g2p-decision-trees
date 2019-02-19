#!/bin/bash
#
# author: 2018
# cassio batista - cassio.batista.13@gmail.com
# edited on feb 2019

COLOR_FG_BOLD="\033[1m"
COLOR_RESET="\033[0m"

TAG='FB_RUN'
DT_CONTEXT=4
DT_DATADIR="dt_data"
DICT_BASEFILENAME="dict_50k"

# TODO: path to m2m aligner
# get it from https://github.com/letter-to-phoneme/m2m-aligner
M2M_ALIGNER_GITDIR="${HOME}/git-all/m2m-aligner/" 

# fb_00: align graphemes and phonemes
echo -e "${COLOR_FG_BOLD}[${TAG}] running M2M aligner ...${COLOR_RESET}"
mkdir -p output
rm -vf output/${DICT_BASEFILENAME}.old.ali
${M2M_ALIGNER_GITDIR}/m2m-aligner \
	--delX \
	-i input/${DICT_BASEFILENAME}.news \
	-o output/${DICT_BASEFILENAME}.old.ali \
	--alignerOut /tmp/nada
rm -vf output/${DICT_BASEFILENAME}.old.ali.err

echo -e "${COLOR_FG_BOLD}[${TAG}] Fixing alignment for Brazilian Portuguese ...${COLOR_RESET}"
bash scripts/fix_align.sh output/${DICT_BASEFILENAME}.old.ali output/${DICT_BASEFILENAME}.new.ali
#bash ./scripts/check.sh output/${DICT_BASEFILENAME}.new.ali

echo -e "${COLOR_FG_BOLD}[${TAG}] Creating list of features (graphemes) and labels/classes (phonemes) ...${COLOR_RESET}"
bash scripts/ali2instance.sh output/${DICT_BASEFILENAME}.new.ali

# fb_01: split train and test
echo -e "${COLOR_FG_BOLD}[${TAG}] Splitting data intro train and test sets...${COLOR_RESET}"
mkdir -p res
python3 scripts/split_train_test.py \
		res/graphemes.list \
		res/phonemes.list \
		$DT_CONTEXT \
		output/dict_50k.new.ali \
		$DT_DATADIR 

# fb_02: decision tree
echo -e "${COLOR_FG_BOLD}[${TAG}] Running decision tree...${COLOR_RESET}"
python3 dt_src/dectree.py \
	res/graphemes.list \
	res/phonemes.list \
	$DT_CONTEXT \
	$DT_DATADIR 
echo -e "${COLOR_FG_BOLD}[${TAG}] Obrigado meu consagrado!${COLOR_RESET}"
echo -e "${COLOR_FG_BOLD}[${TAG}] Check '${DT_DATADIR}' folder to check result files${COLOR_RESET}"
