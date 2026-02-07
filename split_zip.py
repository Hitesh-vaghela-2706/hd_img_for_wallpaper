import os
import zipfile

def split_zip(source_zip_path, output_dir, max_size_mb):
    """Splits a zip file into smaller zip files."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    max_size_bytes = max_size_mb * 1024 * 1024
    current_size = 0
    file_count = 1
    
    # Create the first output zip
    current_zip_name = os.path.join(output_dir, f"split_part_{file_count}.zip")
    current_zip = zipfile.ZipFile(current_zip_name, 'w', zipfile.ZIP_DEFLATED)
    
    with zipfile.ZipFile(source_zip_path, 'r') as zf:
        for file_info in zf.infolist():
            file_data = zf.read(file_info.filename)
            file_size = file_info.file_size
            
            # If adding this file exceeds the limit, create a new zip
            if current_size + file_size > max_size_bytes and current_size > 0:
                current_zip.close()
                file_count += 1
                current_zip_name = os.path.join(output_dir, f"split_part_{file_count}.zip")
                current_zip = zipfile.ZipFile(current_zip_name, 'w', zipfile.ZIP_DEFLATED)
                current_size = 0
            
            # Write file to current split zip
            current_zip.writestr(file_info, file_data)
            current_size += file_size
            print(f"Added {file_info.filename} to {current_zip_name}")
            
    current_zip.close()
    print("Splitting complete.")

# --- Example Usage ---
split_zip('test.zip', 'split_zip', 20) # Splits into 10MB parts


def merge_zips(input_dir, output_zip_path):
    """Merges all zip files from input_dir into a single zip file."""
    
    # Get list of all zip files, sorted to maintain order
    zip_files = sorted([os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.zip')])
    
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as main_zip:
        for zf_path in zip_files:
            print(f"Merging {zf_path}...")
            with zipfile.ZipFile(zf_path, 'r') as zf:
                for file_info in zf.infolist():
                    # Read and write each file
                    main_zip.writestr(file_info, zf.read(file_info.filename))
                    
    print(f"Merged {len(zip_files)} files into {output_zip_path}")

# --- Example Usage ---
merge_zips('split_zip', 'merged.zip')
