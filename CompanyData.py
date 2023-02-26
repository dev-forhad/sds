import re


def extract_company_details(text):
    company_name = re.findall(
        r'(?:Company|Company\s*:)[:\s]*(.*?)\n', text, re.IGNORECASE)
    telephone = re.findall(
        r'(?:T\.|Telephone)[:\s]*(.*?)\n', text, re.IGNORECASE)
    email = re.findall(
        r'(?:E-mail address|Email)[:\s]*(\S+@\S+)', text, re.IGNORECASE)

    return {
        "company_name": company_name[0].strip() if company_name else None,
        "telephone": telephone[0].strip() if telephone else None,
        "email": email[0].strip() if email else None,
    }


text1 = '''Company: MAPEI MALAYSIA Sdn Bhd
Lot 754, Lengkok Emas 1,
Kawasan Perindustrian Nilai,
71800 Negeri Sembilan,
MALAYSIA
T. +606 799 8028 (Mon-Fri 8.30am to 5.30pm)
F. +606 799 8191
sicurezza@mapei.it
www.mapei.com.mx'''

text2 = '''Company : Sika Kimia Sdn. Bhd. 
Lot 689 Nilai Industrial Estate 
71800 Nilai
Telephone : +60 6799 1762
Telefax : +60 6799 1980
E-mail address : EHS@my.sika.com 
Emergency telephone 
number 
: - 
Contact point :'''

print(extract_company_details(text1))
print(extract_company_details(text2))
