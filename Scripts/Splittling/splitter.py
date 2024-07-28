import fitz
import nltk
import json
import PyPDF2
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text()
    doc.close()
    return text

def identify_cities(text):
    with open('pak_city_names.json', 'r') as file:
        cities = json.load(file)
    
    city_names = set(city['name'].lower() for city in cities)
    cities_mentioned = set()
    tokens = nltk.word_tokenize(text.lower())
    text = ' '.join(tokens)
    for city in city_names:
        if city in text:
            cities_mentioned.add(city.title())
    return list(cities_mentioned)

def save_pdf_in_chunks(pdf_writer, file_name, city_dir):
    total_pages = pdf_writer.page_count
    if total_pages == 0:
        print(f"No pages to save for {file_name}, skipping...")
        return 

    if total_pages > 2:
        for start_page in range(0, total_pages, 2):
            end_page = start_page + 1
            if end_page >= total_pages:
                end_page = total_pages - 1
            
            sub_doc = fitz.open()
            for i in range(start_page, end_page + 1):
                sub_doc.insert_pdf(pdf_writer, from_page=i, to_page=i)
            chunk_name = f"{file_name}_pages_{start_page + 1}_to_{end_page + 1}.pdf"
            sub_doc.save(os.path.join(city_dir, chunk_name))
            sub_doc.close()
    else:
        pdf_writer.save(os.path.join(city_dir, file_name))

def classify_and_split_by_extension(doc, output_dir, city):
    city_lower = city.lower()
    if " to " in city_lower:
        sub_folder = "roads"
    else:
        sub_folder = "cities"
    
    city_dir = os.path.join(output_dir, sub_folder, city_lower)
    if not os.path.exists(city_dir):
        os.makedirs(city_dir)

    pdf_writer_bar_graphs = fitz.open()
    pdf_writer_maps = fitz.open()
    pdf_writer_tables = fitz.open()

    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        page_text = page.get_text().lower()

        if city_lower in page_text:
            images = page.get_images(full=True)
            has_png = any(doc.extract_image(img[0])['ext'] == 'png' for img in images)
            has_jpeg = any(doc.extract_image(img[0])['ext'] == 'jpeg' for img in images)
            
            if has_png:
                pdf_writer_bar_graphs.insert_pdf(doc, from_page=page_number, to_page=page_number)
            if has_jpeg:
                pdf_writer_maps.insert_pdf(doc, from_page=page_number, to_page=page_number)
            else:
                pdf_writer_tables.insert_pdf(doc, from_page=page_number, to_page=page_number)

    save_pdf_in_chunks(pdf_writer_bar_graphs, f"{city_lower}_bar_graphs.pdf", city_dir)
    save_pdf_in_chunks(pdf_writer_maps, f"{city_lower}_maps.pdf", city_dir)
    save_pdf_in_chunks(pdf_writer_tables, f"{city_lower}_tables.pdf", city_dir)

    pdf_writer_bar_graphs.close()
    pdf_writer_maps.close()
    pdf_writer_tables.close()

def split_pdf_by_cities(input_pdf, city_list, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    doc = fitz.open(input_pdf)
    for city in city_list:
        classify_and_split_by_extension(doc, output_dir, city)
    doc.close()

def process_files_in_directory(main_folder):
    base_output_dir = r'C:\Users\Dell\Desktop\A_Project\Flooding\OpenCelliD data\Flooding\output'
    os.makedirs(base_output_dir, exist_ok=True)
    
    for year in os.listdir(main_folder):
        year_path = os.path.join(main_folder, year)
        if os.path.isdir(year_path):
            year_output_dir = os.path.join(base_output_dir, year)
            os.makedirs(year_output_dir, exist_ok=True)
            
            for file_name in os.listdir(year_path):
                if file_name.lower().endswith('.pdf'):
                    pdf_path = os.path.join(year_path, file_name)
                    text = extract_text_from_pdf(pdf_path)
                    cities = identify_cities(text)
                    split_pdf_by_cities(pdf_path, cities, year_output_dir)
                    print(f"Processed {pdf_path}: Cities mentioned in the PDF:", cities)

# Directory containing the PDFs to be split
main_folder = r'C:\Users\Dell\Desktop\A_Project\Flooding\OpenCelliD data\Flooding\PTA-dataset'
process_files_in_directory(main_folder)
