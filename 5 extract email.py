# file names
info_file = 'program_info_output 3.txt'       # yahan pe program director aur contact person ka data hai
email_file = 'emails_with_source 3.txt'    # yahan pe program_id:email lines hain
output_file = 'info_updated 4.txt'
import ast
from collections import defaultdict

# 1) load emails into a dict: program_id → [emails]
email_data = defaultdict(list)
with open(email_file, encoding='utf-8') as ef:
    for line in ef:
        line = line.strip()
        if not line or ':' not in line:
            continue
        prog, mail = line.split(':', 1)
        email_data[prog].append(mail.strip())

# 2) process info_file
output_lines = []
current_prog = None
# to keep track: 0→director, 1→contact
email_idx = 0

with open(info_file, encoding='utf-8') as inf:
    for raw in inf:
        line = raw.rstrip('\n')
        # detect program id header
        if line.startswith('program_') and '.html' in line:
            current_prog = line.split(':',1)[0]
            email_idx = 0
            output_lines.append(line + '\n')
            continue

        # only touch lines containing a Python-style dict after "program director:" or "contact person:"
        if (line.lstrip().startswith('program director:') or
            line.lstrip().startswith('contact person:')) and '{' in line and '}' in line:
            
            # split prefix and dict text
            prefix, dict_txt = line.split(':', 1)
            d = ast.literal_eval(dict_txt.strip())
            
            mails = email_data.get(current_prog, [])
            # decide which mail goes here
            new_email = ''
            if len(mails) >= 2:
                # first mail → director, second → contact
                if email_idx < 2:
                    if email_idx < len(mails):
                        new_email = mails[email_idx]
            elif len(mails) == 1:
                # single mail → always contact
                if email_idx == 1:
                    new_email = mails[0]
            
            # update only the 'email' key
            d['email'] = new_email
            
            # reconstruct dict text, preserving order of existing keys
            items = []
            for k, v in d.items():
                # ensure proper quoting
                items.append(f"'{k}': {repr(v)}")
            new_dict_txt = '{' + ', '.join(items) + '}'
            
            output_lines.append(f"{prefix}: {new_dict_txt}\n")
            email_idx += 1
            continue

        # all other lines stay the same
        output_lines.append(raw)

# 3) write output
with open(output_file, 'w', encoding='utf-8') as outf:
    outf.writelines(output_lines)

print("✅ done! see", output_file)
