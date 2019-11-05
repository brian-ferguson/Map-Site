This program will request all a href html information of a specified website and save the output to a csv file named after the specified url in a folder named the same, in the directory the script was run from.

To run this program type:

$python run.py -url "base_url.xyz" -keyword "html" --save [true if included / false if ommited]
*(the "--flags are not needed") example call:

--url:

specify the website to extract information from, if not supplied the script will read the csv file "urls.csv"

--keyword:

specify the keyword that you, if not supplied default to return all a href text
	
--save:

specify if the output csv file should be saved, if not supplied default to false



