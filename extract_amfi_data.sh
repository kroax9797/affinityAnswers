#!/bin/bash

# Download the data
curl -s https://www.amfiindia.com/spages/NAVAll.txt -o nav_data.txt

# Output file
OUTPUT_FILE="scheme_asset_value.tsv"

# Extract Scheme Name and Net Asset Value
# Fields in the file are pipe-separated | ; Scheme Name is 4th field, NAV is 6th
# Remove headers and blank lines

awk -F';' '
BEGIN {
    OFS="\t";
    print "Scheme Name", "Asset Value"
}
NF && $4 ~ /.+/ && $6 ~ /^[0-9.]+$/ {
    gsub(/^[ \t]+|[ \t]+$/, "", $4);
    gsub(/^[ \t]+|[ \t]+$/, "", $6);
    print $4, $6
}
' nav_data.txt > "$OUTPUT_FILE"

echo "✅ Extracted data saved to $OUTPUT_FILE"
