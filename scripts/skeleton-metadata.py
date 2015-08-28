import registre.metadata
import sys

datafilename = sys.argv[1]
#with open(datafilename, 'rU') as datafile:
#    metadata = registre.metadata.generate_metadata(datafile)
#    registre.metadata.output_metadata(metadata, datafilename + ".json")

typesfilename = sys.argv[2]
with open(datafilename, 'rU') as datafile, open(typesfilename) as typesfile:
    metadata = registre.metadata.generate_metadata(datafile, typesfile=typesfile, inferdomain=True)
    registre.metadata.output_metadata(metadata, datafilename + ".json")

