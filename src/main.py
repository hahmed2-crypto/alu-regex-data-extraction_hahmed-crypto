import json
import re



# I want to validate the user input for email, credit card number, currency amount, and phone number using regex patterns for specifically ALU students who are international so that our financial aid team know how will the students be paying their tuition or recieving money for financial aid from ALU.
with open("input/raw-text.txt", "r", encoding="utf-8") as file:
    raw_data = file.read()


#storing emails in their formats
si_emails = []
alumni_emails = []
alu_emails = []
non_alu_emails = []

regex_email = r"[a-zA-Z0-9_\.]+@[a-zA-Z0-9_\.]+\.com" # #Validatinng email addres by categoraizing what the alu emails are by reading the raw data file.


matches = re.findall(regex_email, raw_data, re.IGNORECASE) 

for email in matches:                                               #finding all the matches of alu emails regarding their domain format
    if  email .endswith("@si.alueducation.com"):
        si_emails.append(email)
        print(f"{email} -> SI ALU email")
    elif email .endswith("@alumni.alueducation.com"):
        alumni_emails.append(email)
        print(f"{email} -> Alumni ALU email")
    elif email .endswith("@alueducation.com"):
        alu_emails.append(email)
        print(f"{email} -> ALU email")
    else:
        non_alu_emails.append(email)
        print(f"{email} -> Not an ALU email")

# done wth the email.

#storing and Validating rwandan phone number vs international phone numbers in my data.

rwandan_phones = []
international_phones = []

regex_phone_number = r'\+[\d\ \-\(\)]{7,17}'      # for this i am looking through all set of numbers that starts with literal + sign and contain 0-9, literal - and are in range of 7 to 17 digits

phone_matches = re.findall(regex_phone_number, raw_data)

for phone in phone_matches:
    if phone.startswith("+250"):              #here i am validating if the person is using rwandan phone number or not, if not then it will accept any other country phone number as well.
        rwandan_phones.append(phone)
        print(f"{phone} -> Rwandan phone number")
    else:
        international_phones.append(phone)
        print(f"{phone} -> Not a Rwandan phone number")

#done with phone number validation.

# Here i am building regex patterns for validating user input for email, credit card number, currency amount, and phone number for ALU international students.

normal_cards = []
suspicious_cards = []

regex_credit_card = r'\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}'  


pattern = re.findall(regex_credit_card, raw_data)
for card in pattern:
    normalized_card = card.replace(" ", "").replace("-", "")# removing spaces and dashes from the credit card number to normalize it for further validation.
    if len(set(normalized_card)) == 1:
        suspicious_cards.append(card)
        print(f"****-****-****-{normalized_card[-4:]} -> This is a suspicious credit card number") # the reason I am only printing the last 4 digits is for security reasons, i don't print out the full card. 
    else:
        normal_cards.append(card)
        print(f"****-****-****-{normalized_card[-4:]} -> This is a normal credit card number")

# not completely done with it because i need to do deletion of duplicates. 

# Hree is my currency checking/validation.

usd_amounts = []
rwf_amounts = []
unlabaled_format = []
negative_alerts = []


regex_currency_amount = r'(\$|RWF\s?)?(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)(?:\s?(USD))?' # I set this in groups of three matching different criteria( )


for match in re.finditer(regex_currency_amount, raw_data, re.IGNORECASE): # I use re.finditer to easily access group
    full_match = match.group(0).strip()
    prefix = match.group(1)
    suffix = match.group(3)
    
    
    if not prefix and not suffix and ("," not in full_match) and ("." not in full_match):     # Here is a logic where i am trying to skip the , and . if they are not in full_match.
        continue

                                                                                              # i am identifying the currency type
    if prefix and "$" in prefix:
        usd_amounts.append(full_match)
        print(f"{full_match} -> It is in USD ($ prefix)")
    elif prefix and "RWF" in prefix.upper():
        rwf_amounts.append(full_match)
        print(f"{full_match} -> It is in RWF")
    elif suffix and "USD" in suffix.upper():
        usd_amounts.append(full_match)
        print(f"{full_match} -> It is in USD (suffix)")
    else:
        unlabaled_format.append(full_match)
        print(f"{full_match}-> Unlabaled financial format")



#Finally, a way to know the negative numbers in the my data
negative_amounts = re.findall(r'(?<!\d)-\d+', raw_data)   # I am scanning for any numbers or sets of numbers with - at the start so t
for amount in negative_amounts:
    negative_alerts.append(amount)
    print(f"{amount}-> Negative amount detected")


# Recording html_javascript and sql injections 

html_injections = []
sql_injections = []



regex_html_tag = r'<[^>]+>'   # Looking for any tags that could be either html/js


regex_sql_cmd = r'(?:\bDROP\b|\bDELETE\b|--|;)\s*(?:\bTABLE\b|\bFROM\b)?' # SQL command patterns that match ; DROP Table, delete from, or inline comments like '--'

 
html_matches = re.findall(regex_html_tag, raw_data, re.IGNORECASE) # Here, i looping to search or scan for anything that matchs those tags and then store it.
for match in html_matches:
    html_injections.append(match)
    print(f" HTML Injection detected-> {match}")


sql_matches = re.findall(regex_sql_cmd, raw_data, re.IGNORECASE) # Here is also another for loop that i am using to scan for any SQL pattern that matches that i defined in regex_sql_command in order to catch them and store them so that I store it separately from the clean data.
for match in sql_matches:
    cleaned_match = match.strip()          #    # Double check to ensure we only capture actual risky syntax from the match
    if cleaned_match:
        sql_injections.append(cleaned_match)
        print(f"SQL Injection detected -> {cleaned_match}")


# companing everything and writing it in the .json file so it stores there cleanly.
parsed_financial_profile = {
    "emails": {
        "si": si_emails,
        "alumni": alumni_emails,
        "official": alu_emails,
        "non_alu": non_alu_emails
    },
    "phone_numbers": {
        "rwandan": rwandan_phones,
        "international": international_phones
    },
    "credit_cards": {
        "normal": normal_cards,
        "suspicious": suspicious_cards
    },
    "currency_records": {
        "usd": usd_amounts,
        "rwf": rwf_amounts,
        "unlabeled_formats": unlabaled_format,
        "negatives_detected": negative_alerts
    },

    "security_flags": {
        "html_javascript_injection": html_injections,
        "sql_injection_attempts": sql_injections
    }
}
# done with printing or writing it on the sample-output.json file, it will order the file or store it in this way that i structureed it.


# I want to write it in the .json file so that we can see what is happening in my sample-output.json file.

with open ("output/sample-output.json", "w", encoding="utf-8") as outfile:
    json.dump(parsed_financial_profile, outfile, indent=2)
