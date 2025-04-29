import pandas as pd  # ✅ Keep this import at the top

input_txt = r"C:\Users\dell\Desktop\code\info_updated 4.txt"
output_excel = r"C:\Users\dell\Desktop\code\program_data 3.xlsx"

data = []
current_entry = {}

with open(input_txt, 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line.startswith('program_'):
            current_entry['Program ID'] = line.split('_')[1].split('.')[0]
        elif 'program director:' in line:
            # Rename variable from `pd` to `pd_data`
            pd_data = eval(line.split('program director: ')[1])
            current_entry.update({
                'Director Name': pd_data.get('name', ''),
                'Director Address': pd_data.get('address', ''),
                'Director Tel': pd_data.get('tel', ''),
                'Director Fax': pd_data.get('fax', ''),
                'Director Email': pd_data.get('email', '')
            })
        elif 'contact person:' in line:
            # Rename variable from `cp` to `cp_data`
            cp_data = eval(line.split('contact person: ')[1])
            current_entry.update({
                'Contact Name': cp_data.get('name', ''),
                'Contact Address': cp_data.get('address', ''),
                'Contact Tel': cp_data.get('tel', ''),
                'Contact Fax': cp_data.get('fax', ''),
                'Contact Email': cp_data.get('email', '')
            })
            data.append(current_entry)
            current_entry = {}

# Now `pd` refers to pandas, not your variable
df = pd.DataFrame(data)
df.to_excel(output_excel, index=False)