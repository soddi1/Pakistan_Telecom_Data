import fitz  
import os

def extract_images_from_pdf(pdf_path, output_folder):
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    doc = fitz.open(pdf_path)
    
    # Iterate through each page of the PDF
    for page_number in range(len(doc)):
        page = doc[page_number]
        
        image_list = page.get_images(full=True)
        
        # Go through the image references found on the current page
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_filename = f"image_Page{page_number + 1}_{img_index + 1}.{image_ext}"
            image_filepath = os.path.join(output_folder, image_filename)
            
            # Save the image to the output folder
            with open(image_filepath, "wb") as img_file:
                img_file.write(image_bytes)
    
 
    doc.close()
    print("Image extraction completed.")

# Example usage
pdf_path =   r'E:\Desktop\LUMS\summer2024\Literature Review\data\pdf split\qos_survey_1st_qtr_2020_10072020.pdf'
output_folder = r'E:\Desktop\LUMS\summer2024\Literature Review\data\pdf split\extracted_images2'


extract_images_from_pdf(pdf_path, output_folder)
