import json
import sys
from pathlib import Path

# ap, pd not available in csl-orig
csl_ids = ["acc", "ae", "ap90", "ben", "bhs", "bop", "bor", "bur", "cae", "ccs", "gra", "gst", "ieg", "inm", "krm",
           "mci", "md", "mw", "mw72", "mwe", "pe", "pgn", "pui", "pw", "pwg", "sch", "shs", "skd", "snp", "stc", "vcp",
           "vei", "wil", "yat"]


def generate_kosh_files(csl_ids, abs_path_to_gen_xml_files):
    for dict in csl_ids:
        # create sub_Dir for each if not there
        Path('{}/{}'.format(abs_path_to_gen_xml_files, dict)).mkdir(parents=True, exist_ok=True)

        # we create a .kosh file for each dict
        filename = "{}/{}/.kosh".format(abs_path_to_gen_xml_files, dict)
        with open(filename, mode="w") as writer:
            # [acc]
            writer.write('[{}]'.format(dict))
            writer.write('\n')
            # files: ["acc.xml"]
            #abs_path_to_gen_dict_xml_files = '{}/{}/pywork/{}'.format(abs_path_to_gen_xml_files, dict, dict)
            writer.write('files: ["{}.xml"]'.format(dict))
            writer.write('\n')
            # schema: kosh_dict_mapping.json
            # abs_path_to_gen_dict_kosh_files = '{}/{}/'.format(abs_path_to_gen_kosh_files, dict)
            writer.write('schema: kosh_{}_mapping.json'.format(dict))
            writer.write("\n")


def generate_mapping_files(csl_ids, abs_path_to_gen_kosh_files):
    for dict in csl_ids:
        # create sub_Dir for each if not there
        Path('{}/{}/'.format(abs_path_to_gen_kosh_files, dict)).mkdir(parents=True, exist_ok=True)
        mappings = {}
        mappings['mappings'] = {}

        xpaths = {}
        xpaths['_xpaths'] = {}
        ## add objects to xpaths
        # xpath to get all entries. in CDSD CML dicts is the <H1> node
        xpaths['_xpaths']['root'] = '//H1'
        # ids are required. To be found in tail><L>XXX</L>...
        xpaths['_xpaths']['id'] = './tail/L'
        # fields to be indexed. Here we do only index the <H1><h><key1>XXX</key1>... headword. This can be tailored for each dict later.
        # Kosh per default indexes the whole xml entry. NOTE: xml tags and attrs are not indexed.
        fields = {}
        fields['headword'] = './h/key1'
        xpaths['_xpaths']['fields'] = fields

        mappings['mappings']['_meta'] = xpaths

        properties = {}
        properties['headword'] = {}
        properties['headword']['type'] = 'keyword'

        mappings['mappings']['properties'] = properties

        ## The 'properties' object provides elastic search with info for manipulating the index
        # strings classified as 'keyword' will not be analyzed i.e. they will not be tokenized or lowercased.
        # strings classified as 'text' will be analyzed

        with open('{}/{}/kosh_{}_mapping.json'.format(abs_path_to_gen_kosh_files, dict, dict), 'w') as outfile:
            json.dump(mappings, outfile, indent=4)


def main():
    # print command line arguments
    # sript's name sys.argv[0]='generate_kosh_files.py'


    # sys.argv[2] = abs_path_to_gen_xml_files e.g. '/home/me/repositories/csl-generated_xml/'
    abs_path_to_gen_xml_files = sys.argv[1]

    # remove trailing slashes is present
    abs_path_to_gen_xml_files = abs_path_to_gen_xml_files.rstrip('/')
    print('path_to_gen_xml', abs_path_to_gen_xml_files)

    # create kosh files
    generate_kosh_files(csl_ids, abs_path_to_gen_xml_files)
    # create mapping files
    generate_mapping_files(csl_ids, abs_path_to_gen_xml_files)


if __name__ == "__main__":
    main()
