from pypdf import PdfReader, PdfWriter
import os

def split_pdf(input_pdf, output_dir, chunk_size=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    reader = PdfReader(input_pdf)
    total_pages = len(reader.pages) # Get total page count
    parts = []
    
    # Iterate through pages in steps of 10
    for i in range(0, total_pages, chunk_size):
        writer = PdfWriter()
        
        # Calculate the end page for this chunk
        end = min(i + chunk_size, total_pages)
        
        # Add pages in the current 10-page range
        for page_num in range(i, end):
            writer.add_page(reader.pages[page_num])
        
        output_filename = os.path.join(output_dir, f'pages_{i+1}_to_{end}.pdf')
        with open(output_filename, 'wb') as out_file:
            writer.write(out_file)
            
        print(f'Created: {output_filename}')
        parts.append(output_filename)
        
    return parts

def merge_pdfs(file_list, output_path):
    writer = PdfWriter()
    
    # Efficiently append each chunked PDF file
    for pdf in file_list:
        writer.append(pdf)
        
    with open(output_path, 'wb') as out_file:
        writer.write(out_file)
    print(f'Final Merged PDF created: {output_path}')


# Execution remains the same
source_file = 'test.pdf'
split_folder = 'split_pdf'
merged_file = 'final_10page_blocks.pdf'

# 1. Split into 10-page chunks
page_files = split_pdf(source_file, split_folder, chunk_size=10)

# 2. Merge those specific chunks into one final file
merge_pdfs(page_files, merged_file)