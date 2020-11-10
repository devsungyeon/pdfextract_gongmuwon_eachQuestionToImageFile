import PyPDF2
import PyPdf
def extract_tree(in_file, out_file):
    with open(in_file, 'rb') as infp:
        # Read the document that contains the tree (in its first page)
        reader = PyPdf.PdfFileReader(infp)
        page = reader.getPage(0)
        # Crop the tree. Coordinates below are only referential
        page.cropBox.lowerLeft = [100,200]
        page.cropBox.upperRight = [250,300]
        # Create an empty document and add a single page containing only the cropped page
        writer = PyPdf.PdfFileWriter()
        writer.addPage(page)
        with open(out_file, 'wb') as outfp:
            writer.write(outfp)
def insert_tree_into_page(tree_document, text_document):
    # Load the first page of the document containing 'text text text text...'
    text_page = PyPDF2.PdfFileReader(open(text_document,'rb')).getPage(0)
    # Load the previously cropped tree (cropped using 'extract_tree')
    tree_page = PyPDF2.PdfFileReader(open(tree_document,'rb')).getPage(0)
    # Overlay the text-page and the tree-crop   
    text_page.mergeScaledTranslatedPage(page2=tree_page,scale='1.0',tx='100',ty='200')
    # Save the result into a new empty document
    output = PyPDF2.PdfFileWriter()
    output.addPage(text_page)
    outputStream = open('merged_document.pdf','wb')
    output.write(outputStream)
# First, crop the tree and save it into cropped_document.pdf
extract_tree('document1.pdf', 'cropped_document.pdf')
# Now merge document2.pdf with cropped_document.pdf
insert_tree_into_page('cropped_document.pdf', 'document2.pdf')
 