import os
from bs4 import BeautifulSoup

# function to extract info from html content
def extract_program_info(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text('\n').strip()
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    data = {
        'program_director': {},
        'contact_person': {}
    }
    
    pd_done = False
    for i, line in enumerate(lines):
        # extract program director
        if "Program Director:" in line and not pd_done:
            pd_done = True
            # name
            if i+1 < len(lines):
                data['program_director']['name'] = lines[i+1]
            # address
            address = []
            j = i + 2
            while j < len(lines) and not lines[j].startswith('Tel:'):
                address.append(lines[j])
                j += 1
            data['program_director']['address'] = ' '.join(address)
            # contact details
            for k in range(j, len(lines)):
                if lines[k].startswith('Tel:'):
                    data['program_director']['tel'] = lines[k].split(':', 1)[1].strip()
                elif lines[k].startswith('Fax:'):
                    data['program_director']['fax'] = lines[k].split(':', 1)[1].strip()
                elif lines[k].startswith('E-mail:'):
                    data['program_director']['email'] = lines[k].split(':', 1)[1].strip()
                elif "Person to contact" in lines[k]:
                    break
        # extract contact person
        if "Person to contact for more information about the program:" in line:
            # name
            if i+1 < len(lines):
                data['contact_person']['name'] = lines[i+1]
            # address
            address = []
            j = i + 2
            while j < len(lines) and not lines[j].startswith('Tel:'):
                address.append(lines[j])
                j += 1
            data['contact_person']['address'] = ' '.join(address)
            # contact details
            for k in range(j, len(lines)):
                if lines[k].startswith('Tel:'):
                    data['contact_person']['tel'] = lines[k].split(':', 1)[1].strip()
                elif lines[k].startswith('Fax:'):
                    data['contact_person']['fax'] = lines[k].split(':', 1)[1].strip()
                elif lines[k].startswith('E-mail:'):
                    data['contact_person']['email'] = lines[k].split(':', 1)[1].strip()
                elif k > i and ("Program Director:" in lines[k] or k == len(lines)-1):
                    break
    return data

# directory containing html files
input_dir = r'C:/Users/dell/Desktop/code/Allergy and Immunology program_pages'
# output txt file path
output_path = os.path.join(input_dir, 'program_info_output 3.txt')

results = []

# open the output file for writing
with open(output_path, 'w', encoding='utf-8') as out_file:
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.html'):
            file_path = os.path.join(input_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()
            info = extract_program_info(html)
            results.append(info)

            # write to txt
            out_file.write(f"processed {filename}:\n")
            out_file.write(f"program director: {info['program_director']}\n")
            out_file.write(f"contact person: {info['contact_person']}\n\n")

print(f"results saved to {output_path}")
