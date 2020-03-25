# Deploy the [Cologne Digital Sanskrit Dictionaries](https://www.sanskrit-lexicon.uni-koeln.de) with [Kosh](https://cceh.github.io/kosh/)

## Required GitHub repos:

For generating CDSD-XML files:

[https://github.com/sanskrit-lexicon/csl-orig](https://github.com/sanskrit-lexicon/csl-orig)

[https://github.com/sanskrit-lexicon/csl-pywork](https://github.com/sanskrit-lexicon/csl-pywork)

For generating and regenerating XML files automatically:

https://github.com/vocabulista/csl-kosh

We recommend to place all the repos under the same path e.g. `/opt/cdsd/`

anaconda/[minicoda](https://docs.conda.io/en/latest/miniconda.html) is required. 

After cloning `csl-kosh`, inside this directory execute:  `conda env create --file=environment.yml`

## **Generate XML files**

`csl-pywork` contains different scripts that generate XML versions of the CDSD dicts.

The script `csl-kosh/generate_csl_xml.sh` contains most of the logic implemented in csl-pyworks scripts. The resulting files are to be found in `csl-pywork_output`. In order to make the sync function of Kosh work properly, after each dict is generated in `generate_csl_xml.sh`, a copy of the related XML file is copied into `csl-kosh_generated`.

Running `csl-kosh/generate_csl_xml.sh`:

* $1 abs_path_to csl-orig (e.g. '/opt/cdsd/csl-orig/v02/'
* $2 abs_path_to csl-pywork bash files (in csl-pywork e.g. '/opt/cdsd/csl-pywork/v02/''
* $3 abs_path_to csl-pywork-output e.g. '/opt/cdsd/csl-generated-pywork/'
* $4 abs_path_to_generated_kosh_files e.g. '/opt/cdsd/csl-generated-kosh/'
* $5 abs_path to conda.sh e.g. '/home/me/miniconda3/etc/profile.d/conda.sh'

`bash generate_csl_xml.sh /opt/cdsd/csl-orig/v02/ /opt/cdsd/csl-pywork/v02/ /opt/cdsd/csl-generated-pywork/ /opt/cdsd/csl-generated-kosh/ /home/me/miniconda3/etc/profile.d/conda.sh`

## Generate Kosh files

The script generate_kosh_files.py generates all files required by Kosh.

Usage:

- sys.argv[1] = abs_path_to_gen_xml_files e.g. 'opt/cdsd/csl-generated-kosh/'

 `python csl-kosh/generate_kosh_files.py  /opt/cdsd/csl-generated-kosh/`


## **Deploying Kosh**

[Kosh](https://cceh.github.io/kosh/) requires Docker and Docker Compose. 

Clone Kosh: [https://github.com/cceh/kosh](https://github.com/cceh/kosh)

Use the `feat-elem_id` branch

Kosh must know where the XML and Kosh-related files are located. For this purpose you need to provide the path in  `docker-compose.local.yml`:
```
    version: '2.3'
    services:
    	kosh:
    		volumes: ['/opt/cdsd/csl-generated-kosh:/var/lib/kosh:ro']
```

Deploy Kosh:

    docker-compose -p cdsd -f docker-compose.yml -f docker-compose.local.yml up -d

## Sync csl-orig

The master TXT files located in `csl-orig` are regularly updated. 
You can create a cron job for pulling regularly this repo from GitHub into your local instance:

`crontab -e`

Add the following entries:
```
# m h  dom mon dow   command
55 23 * * * cd /opt/cdsd/csl-orig/ && git pull
55 07 * * * cd /opt/cdsd/csl-orig/ && git pull
```



## Regenerating XML files with watch_csl-orig.sh

This script requires the package `inotify-tools`. This script is a slightly modified version of `generate_csl_xml.sh`

It is recommended to run this script with `screen`.

Example:

`screen -S watch_csl-orig`

* $1 abs_path_to csl-orig e.g. '/opt/cdsd/csl-orig/v02/'
* $2 abs_path_to csl-pywork bash files e.g. '/opt/cdsd/csl-pywork/v02/'
* $3 abs_path_to csl-pywork_output e.g. '/opt/cdsd/csl-generated-pywork/'
* $4 abs_path_to_generated_kosh_files e.g. '/opt/cdsd/csl-generated-kosh/'
* $5 abs_path to conda.sh e.g. '/home/me/miniconda3/etc/profile.d/conda.sh'
* $6 abs_path_to_logfile e.g. '/opt/cdsd/csl-logs/logs.txt'

 `bash watch_csl-orig.sh /opt/cdsd/csl-orig/v02/ /opt/cdsd/csl-pywork/v02/ /opt/cdsd/csl-generated-pywork/ /opt/cdsd/csl-generated-kosh/ /home/me/miniconda3/etc/profile.d/conda.sh /opt/cdsd/csl-logs/logs.txt`
