import os
import sys
import csv
import json


# specify input and output file paths
input_file = os.path.join(sys.path[0], "../laion/laion_synthetic_filtered_large.json")
output_file = os.path.join(sys.path[0], "laion_synthetic_filtered_large_30k.tsv")

# load JSON data from input file
with open(input_file, 'r') as f:
    data = json.load(f)

# extract header and data from JSON
header = data[0].keys()
rows = [x.values() for x in data[:30000]]

# write data to TSV file
with open(output_file, 'w') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(header)
    writer.writerows(rows)
