#!/bin/bash

csl_ids=(acc ae ap90 ben bhs bop bor bur cae ccs gra gst ieg inm krm mci md mw mw72 mwe pe pgn pui pw pwg sch shs skd snp stc vcp vei wil yat)

# pd, ap not to be find in csl-origin

#$1 abs_path_to csl-orig (e.g. '/opt/cdsd/csl-orig/v02/')
#$2 abs_path_to csl-pywork bash files (in csl-pywork e.g. '/opt/cdsd/csl-pywork/v02/'
#$3 abs_path_to csl-pywork_output e.g. '/opt/cdsd/csl-generated-pywork/'
#$4 abs_path_to_generated_kosh_files e.g. '/opt/cdsd/csl-generated-kosh/'
#$5 abs_path to conda.sh e.g. '/home/me/miniconda3/etc/profile.d/conda.sh'

source $5
conda activate csl-kosh


for dict_id in "${csl_ids[@]}"

do 
	cd ${2}

    echo "current dir $PWD" 

	# generate_orig.py	
	python generate.py "${dict_id}" inventory_orig.txt _ "${1}${dict_id}" ${3}${dict_id}

	echo "${3}${dict_id} has been generated" 

	# generate_pywork.py
	python generate.py "${dict_id}" inventory.txt  makotemplates distinctfiles/${dict_id} ${3}${dict_id}
			
	# go to the generated local instance
	cd ${3}${dict_id}/pywork

	echo "regenerate ${dict_id} headwords"
	sh redo_hw.sh

	echo "regenerate ${dict_id}.xml files"
	sh redo_xml.sh

	#mkdir if not available
	mkdir -p ${4}${dict_id}
	echo "${4}${dict_id} created"

	# copy xml file fo csl-kosh_generated
  cp  ${dict_id}.xml ${4}${dict_id}/${dict_id}.xml
  echo "${dict_id}.xml copied to ${4}${dict_id}"

done
