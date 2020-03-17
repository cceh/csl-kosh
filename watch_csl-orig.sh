#!/bin/bash

#$1 abs_path_to csl-orig (e.g. '/opt/cdsd/csl-orig/v02/')
#$2 abs_path_to csl-pywork bash files (in csl-pywork e.g. '/opt/cdsd/csl-pywork/v02/'
#$3 abs_path_to csl-pywork_output e.g. '/opt/cdsd/csl-generated-pywork/'
#$4 abs_path_to_generated_kosh_files e.g. '/opt/cdsd/csl-generated-kosh/'


inotifywait -m -r ${1} -e close_write|
    while read path action file; do
        dict_id=`basename "$path"`
        echo "$dict_id has been modified"
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

		# mkdir if not available
	  mkdir -p ${4}${dict_id}
	  echo "${4}${dict_id}"

	  # copy xml file fo csl-kosh_generated
    cp  ${dict_id}.xml ${4}${dict_id}/${dict_id}.xml
    echo "${dict_id}.xml copied to ${4}${dict_id}"

    done