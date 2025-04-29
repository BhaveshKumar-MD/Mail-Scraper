import requests
import os
import time

def download_program_pages(id_file_path, output_folder="Diagnostic Radiology Nuclear Medicine program_pages"):
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

    print(f"\nSummary:")
    print(f"Successfully downloaded: {success_count}/{len(program_ids)}")
    print(f"Failed IDs: {failed_ids}")

# Usage - replace with your actual file path
input_file = r'C:\Users\dell\Desktop\code\Diagnostic_Radiology_Nuclear_Medicine_program_ids.txt'
download_program_pages(input_file)