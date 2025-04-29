import requests
import os
import time

def download_program_pages(id_file_path, output_folder=None):
    # Determine output folder if not provided
    if output_folder is None:
        input_dir = os.path.dirname(id_file_path)
        base_name = os.path.splitext(os.path.basename(id_file_path))[0]
        output_folder = os.path.join(input_dir, f"{base_name}_program_pages")

    # Read IDs from text file
    with open(id_file_path, 'r') as f:
        program_ids = [line.strip() for line in f.readlines() if line.strip()]

    # Create output directory if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    success_count = 0
    failed_ids = []

    for idx, program_id in enumerate(program_ids, 1):
        url = f'https://freida.ama-assn.org/program/{program_id}'
        filename = os.path.join(output_folder, f'program_{program_id}.html')

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            print(f"Downloaded ({idx}/{len(program_ids)}) {program_id}")
            success_count += 1
            time.sleep(1)  # Respectful delay

        except Exception as e:
            print(f"Failed to download {program_id}: {str(e)}")
            failed_ids.append(program_id)

    print(f"\nSummary for {os.path.basename(id_file_path)}:")
    print(f"Successfully downloaded: {success_count}/{len(program_ids)}")
    print(f"Failed IDs: {failed_ids}\n")
    print("-" * 50 + "\n")

# Usage - add your input file paths here
input_files = [
    r'C:\Users\dell\Desktop\code\Emergency Medicine_ids.txt',
    r'C:\Users\dell\Desktop\code\Emergency_Medicine_Anesthesiology_program_ids.txt',
    r'C:\Users\dell\Desktop\code\Emergency_Medicine_Family_Medicine_program_ids.txt',
    r'C:\Users\dell\Desktop\code\Family Medicine_ids.txt',
       # Add more file paths as needed
]

for input_file in input_files:
    download_program_pages(input_file)
    time.sleep(2)  # Additional delay between different program types

#     Summary for Family Medicine_ids.txt:
# Successfully downloaded: 803/804
# Failed IDs: ['1204500671']