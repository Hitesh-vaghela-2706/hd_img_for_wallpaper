from pypdf import PdfReader, PdfWriter
import os

# --- Part 1: Split PDF ---
def split_pdf(input_pdf, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    reader = PdfReader(input_pdf)
    parts = []
    
    for i, page in enumerate(reader.pages):
        writer = PdfWriter()
        writer.add_page(page)
        
        output_filename = os.path.join(output_dir, f'page_{i + 1}.pdf')
        with open(output_filename, 'wb') as out_file:
            writer.write(out_file)
        print(f'Created: {output_filename}')
        parts.append(output_filename)
    return parts

# --- Part 2: Merge PDF ---
def merge_pdfs(file_list, output_path):
    writer = PdfWriter()
    
    for pdf in file_list:
        writer.append(pdf)
        
    with open(output_path, 'wb') as out_file:
        writer.write(out_file)
    print(f'Merged PDF created: {output_path}')

# --- Execution ---
source_file = 'test.pdf' # Replace with your PDF
split_folder = 'split_pdf'
merged_file = 'merged.pdf'

# Run split
page_files = split_pdf(source_file, split_folder)

# Run merge
merge_pdfs(page_files, merged_file)
