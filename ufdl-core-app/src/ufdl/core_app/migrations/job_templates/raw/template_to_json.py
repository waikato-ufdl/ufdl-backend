# Simple script to convert a template file into a JSON structure
# to allow copy/pasting into the actual JSON template.
# JSON doesn't support multi-line strings unfortunately.
# First argument to script is the file to turn into JSON.

import json
import sys

if len(sys.argv) == 1:
    print("No template file provided!")
    exit(1)

with open(sys.argv[1], "r") as tf:
    lines = tf.readlines()
data = dict()
data['body'] = "".join(lines)
print(json.dumps(data, indent=2))
