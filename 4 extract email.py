import re
import os

# regex to capture the email address
pattern = re.compile(r'"field_email":"([a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,})"', re.IGNORECASE)

root_dir = r'C:\Users\dell\Desktop\code\Allergy and Immunology program_pages'
output_file = 'emails_with_source 3.txt'

with open(output_file, 'w', encoding='utf-8') as out:
    for subdir, _, files in os.walk(root_dir):
        for fname in files:
            if fname.lower().endswith('.html'):
                path = os.path.join(subdir, fname)
                with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                    text = f.read()
                for email in pattern.findall(text):
                    # write in format: filename:email
                    out.write(f'{fname}:{email}\n')

print(f'done! emails written to {output_file}')
