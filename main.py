import sys, os
import docx2pdf
import shutil
#user defined functions
import images, word_doc, template_creation
from uuid import uuid4


def process_image_and_generate_report():
    # Get image details
    uploads_dir = 'Uploaded Images'
    uploaded_images_dir = os.path.join(os.getcwd(), uploads_dir)
    # folder_path = "F:\\phAIdelta\\Img Processing and Report Creation\\images"
    no_of_imgs, dict_image_names =  images.count_files(uploaded_images_dir)

    if no_of_imgs == 0:
        print("There are no images to process in the specified folder.")
        sys.exit()

    # Check if resize folder is available
    resized_folder_dir = 'Resized'
    resized_folder_path = os.path.join(uploaded_images_dir,resized_folder_dir)
    # resized_folder_path = "F:\\phAIdelta\\Img Processing and Report Creation\\images\\resized_images"   
    images.check_folder(resized_folder_path=resized_folder_path)

    # Resize images
    images.resize_image(dict_image_names, resized_folder_path=resized_folder_path, desired_height= 100)  

    # Get resized image details
    no_of_resized_imgs, dict_image_names_resized =  images.count_files(resized_folder_path)

    # Identify number of rows to be included in the table.
    number_of_rows = word_doc.calc_number_of_rows(no_of_resized_imgs) 

    # Create Report
    template_creation.ceate_reoprt(resized_img_dict = dict_image_names_resized ,no_of_imgs=no_of_resized_imgs,no_of_rows=number_of_rows)

    # Add headers and footers
    company_logo = 'logo.jpeg'
    doc_path = 'report.docx'
    doc_title = 'Adjudication Report'
    word_doc.add_headers_footers(doc_path=doc_path, doc_title=doc_title, logo_path=company_logo)

    # Add second para
    template_creation.add_second_para(doc_path=doc_path)

    rand_name = uuid4().hex
    # Save Report in PDF
    print("Process Start")
    # os.system("docx2pdf report.docx assets/report.pdf")
    os.system(f"docx2pdf report.docx assets/report_{rand_name}.pdf")
    # source_path = os.path.join(os.getcwd(),'report.pdf')
    # print(source_path)
    # destination_path = os.path.join(os.getcwd(),'assets','report.pdf')
    # shutil.move(source_path,destination_path)
    print("Process end")
    return f"assets/report_{rand_name}.pdf"

if __name__ == "__main__":
    process_image_and_generate_report()