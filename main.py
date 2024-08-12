# main.py
import sys
import signal
import gradio as gr
from langchain_community.document_loaders import PyPDFLoader
from langchain_helper import generate_paper
import fitz

def process_csv(curriculum, past_papers):
    # loader = PyPDFLoader(curriculum)
    # pages = loader.load_and_split()
    # curriculum_text =  pages[0].page_content

    
    # loader = PyPDFLoader(past_papers)
    # pages = loader.load_and_split()
    # past_papers_text =  pages[0].page_content

    cr_doc = fitz.open(curriculum)
    pp_doc = fitz.open(past_papers)

    cr_page = cr_doc[0]
    pp_page = pp_doc[0]

    curriculum_text = cr_page.get_text()
    past_papers_text = pp_page.get_text()
    image_list = pp_page.get_images(full=True)

    # Iterate over each image
    for image_index, img in enumerate(image_list):
        xref = img[0]
        base_image = pp_doc.extract_image(xref)
        image_bytes = base_image["image"]
        image_ext = base_image["ext"]
        
        # Save the image
        with open(f"image_page_{image_index}.{image_ext}", "wb") as img_file:
            img_file.write(image_bytes)

    filePath =  generate_paper(curriculum_text, past_papers_text)

    return filePath

def main():
    try:
        iface = gr.Interface(
            fn=process_csv,
            inputs=[gr.File(file_count="single", type="filepath", label="Curriculum"), gr.File(file_count="single", type="filepath", label="PastPaper")],
            outputs="text", 
            title="Paper Generator",
            description="Upload Curriculum and Past Paper to Generate New Paper"
        )

        # Define a signal handler to close the interface
        def signal_handler(sig, frame):
            print("Closing Gradio interface...")
            iface.close()
            sys.exit(0)

        # Register the signal handler for SIGINT and SIGTERM
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Launch the Gradio interface
        iface.launch(share=True)
    except Exception as e:
        print(f'An error occurred: {e}')
        sys.exit(1)

if __name__ == "__main__":
    main()
