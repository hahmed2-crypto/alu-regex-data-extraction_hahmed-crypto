# My ALU regex data extraction and validation
# Overview
This is my project where i extracted real data and validated it from a sample of messy test that I created. In the input/raw-text.txt file is where the messy data is in. In there, u will find.
 Emails: 
    It has email adress with special categorazation for ALU emails, official alu eamil, alumni email, and SI alu email adress.
Phone numbers:
    categoraized into two parts. Rwandan and International phone numbers.
Credit card numbers: 
    I am validating between suspicious card vs real card.
currency amounts:
    I am checking wither the currency is labeled as in "USD" or "$" infront or at the back of the digits.
    Also, if it is RWF format. if it is labeled as RWF at the begining or not.

Results are printed on the console as they are found, and full categorized results are written to outp/sample-output.json file.

# How to Run
from the root folder.
using python src/main.py 

# Explanation on how it works
The main.py file reads the input/raw-text.txt which in the root so that is why we need to run the program from the root.
Then, it processes/stores the data, and writes summary of each extracted data into the output/sample-output.json file.

# Regex Design Notes

. Emails: It starts checking the general email pattern(local@domian.com) -> looks for emails ending with @si.alueducation.com -> checks for one ending with @alumni.alueducation.com -> checks if theres is one that ends with @alueducation.com wich is the officail student email -> if else, it will print non-alu emails.

. Phone numbers: It starts by checking if the cobination of strings start with '+' and is between 7-17 digits, also checks for space,dashes or parentheses. ->  focuses on cobinations that has starts with this "+250" to print is a Rwandan number else it is international number.


. Credit cards: It starts with group 4 by 4, 4 digits in four groups -> we remove or strip space,or dashes entirely so that digits become one string -> check if all of those digits identical-> if all identical print the card but only the last 4 digits because of security resoans and print suspisious text at the end -> if else print it normal card, also only yhe last 4 digits with a text telling us it normal card

. Currency amounts: I start by setting the pattern to catch the $ and RWF at the front of the number and with different string multiplied or attached to the first string, we also check the USD at the end of the cobination of the digits -> in the loop, we catch what prefix and suffix are -> follow with if it is prefex and it is the actual of the signs "$" or "RWF" or suffixes of "USD" then store it and print in the console. In that way, we get digits starting with prefix of "$" and "RWF" at the front and numbers contain "USD" at the end.

Negative amounts: I start by searching for a dash -> followed by digits, but only if ther isn't already a digit right before the dash, to stop it from grapping pieces of credit card or phone numbers that just happen to haave a dash in them, and only catches real negative amounts like -99999 in my data.

# Security Considerations
> Credit card numbers are masked in order to concile the whole card since we don't want people stealing those information
> Credit cards where every digit is identical (e.g. all zeros in my raw-text.txt file) are flagged as suspicious rather than accepted as valid since that can't be real credit card.
> Negative currency amounts are flagged rather than silently treated as valid disbursement amounts.
> I wrote in the raw-text.txt file some malford data in order to make sure that the my regex scans tags(HTML) and sql(SQL patterns like ; DROP Table or Delete table) injections and reports back as flagged injection.
> On top of that, the program actively scans the whole file to find anything that looks like it is an HTML tag or a SQL command, and flags it whatever it finds separately in the output instead of just hoping hte other patterns skip over it. 

# Known Limitations
> I am working on the duplicate credit card detection across multiple tickets
> The suspicious-card check only detects all-identical-digit patterns; it is not a full fraud-detection system.
