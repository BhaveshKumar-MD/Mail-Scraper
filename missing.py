import os

TEXT_FILE_PATH = r'C:\Users\dell\Desktop\code\program_ids.txt'
FOLDER_PATH = r'C:\Users\dell\Desktop\code\Program_pages'  # 👈 UPDATE THIS

# Read text file IDs
with open(TEXT_FILE_PATH, 'r') as f:
    text_ids = [line.strip() for line in f]  # Keep as LIST to check duplicates
    text_ids_set = set(text_ids)  # For comparison

# Read folder IDs
folder_ids = []
for filename in os.listdir(FOLDER_PATH):
    if filename.startswith('program_') and filename.endswith('.html'):
        id_part = filename.split('_')[1].split('.')[0]
        folder_ids.append(id_part)
folder_ids_set = set(folder_ids)

# Check for duplicates in TEXT FILE
text_duplicates = set([x for x in text_ids if text_ids.count(x) > 1])
if text_duplicates:
    print(f"⚠️ Duplicate IDs in text file: {text_duplicates}")

# Check for duplicates in FOLDER
folder_duplicates = set([x for x in folder_ids if folder_ids.count(x) > 1])
if folder_duplicates:
    print(f"⚠️ Duplicate files in folder: {folder_duplicates}")

# Compare counts
print(f"\nText file IDs: {len(text_ids)} (Unique: {len(text_ids_set)})")
print(f"Folder files: {len(folder_ids)} (Unique: {len(folder_ids_set)})")

# Find discrepancies
missing_in_folder = text_ids_set - folder_ids_set
extra_in_folder = folder_ids_set - text_ids_set

if missing_in_folder:
    print(f"\n🔍 Missing in folder: {missing_in_folder}")
if extra_in_folder:
    print(f"\n🔍 Extra files in folder: {extra_in_folder}")