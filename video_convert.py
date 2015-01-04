#!/bin/bash

###############################################################################
#execute using bash mkvconv.sh

# Script to recursively search a directory and batch convert all files of a given
# file type into another file type via HandBrake conversion.
#
# To run in your environment set the variables:
#   hbcli - Path to your HandBrakeCLI
#
#   source_dir - Starting directory for recursive search
#
#   input_file_types - Input file types to search for
#
#   output_file_type  - Output file type to convert into
#
#
# Change log:
# 2014-01-27: Initial release.  Tested on ubuntu 13.10.
#http://stackoverflow.com/questions/21404059/bash-script-to-select-multiple-file-formats-at-once-for-encode-process/21404530#21404530
###############################################################################

hbcli=HandBrakeCLI
source_dir="/media/rt/1tera_ext/1_Video_Stuff/1 Nova and bbc/Carbon diamonds"


input_file_types=(avi wmv flv mp4 webm mov mpg)
output_file_type="mkv"

echo "# Using HandBrakeCLI at "$hbcli
echo "# Using source directory " "$source_dir"
echo "# Converting "$input_file_types" to "$output_file_type

# Convert from one file to another
convert() {
	# The beginning part, echo "" | , is really important.  Without that, HandBrake exits the while loop.
	#echo "" | $hbcli -i "$1" -o "$2" --preset="Universal"; # dont use with preses things are left out
	echo "" | $hbcli -i "$1" -t 1 --angle 1 -c 1 -o "$2"  -f mkv  --decomb --loose-anamorphic  --modulus 2 -e x264 -q 20 --cfr -a 1,1 -E faac,copy:ac3 -6 dpl2,auto -R Auto,Auto -B 160,0 -D 0,0 --gain 0,0 --audio-fallback ffac3 --x264-profile=high  --h264-level="4.1"  --verbose=1

}
# loop over the types and convert
for input_file_types in "${input_file_types[@]}"
do

	# Find the files and pipe the results into the read command.  The read command properly handles spaces in directories and files names.
	#find "$source_dir" -name *.$input_file_type | while read in_file
	find "$source_dir" -name "*.$input_file_types" -print0 | while IFS= read -r -d $'\0' in_file
	#In order to correctly handle filenames containing whitespace and newline characters, you should use null delimited output. That's what the -print0 and read -d $'\0' is for.
	do
	        echo "Processing…"
		echo ">Input  "$in_file
	
		# Replace the file type
		out_file=$(echo $in_file|sed "s/\(.*\.\)$input_file_types/\1$output_file_type/g")
		echo ">Output "$out_file
	
		# Convert the file
		convert "$in_file" "$out_file"
	
		if [ $? != 0 ]
	        then
	            echo "$in_file had problems" >> handbrake-errors.log
	        fi
	
		echo ">Finished "$out_file "\n\n"
	done
done
echo "DONE CONVERTING FILES"