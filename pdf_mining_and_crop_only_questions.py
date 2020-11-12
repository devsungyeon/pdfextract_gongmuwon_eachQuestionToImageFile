from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import PyPDF2
# import PyPDF2


li = []
# questions location list

def extract_tree(in_file, locli, pagenum):
    with open(in_file, 'rb') as infp:
        # Read the document that contains the tree (in its first page)
        reader = PyPDF2.PdfFileReader(infp)
        page = reader.getPage(pagenum)
        
        for q in range(len(locli)-1): #595, 841
            if locli[q][1]  > locli[q+1][1]:
                # Crop the tree. Coordinates below are only referential
                page.cropBox.lowerLeft =  [  locli[q][0],     locli[q+1][1] +15  ]#[100,200]
                # print(locli[q][0],     locli[q+1][1] +15)
                page.cropBox.upperRight = [  locli[q][0]+280, locli[q][1]   +15  ]#[250,300]
                # print(locli[q][0]+280, locli[q][1]   +15)
                # Create an empty document and add a single page containing only the cropped page
            else:
                page.cropBox.lowerLeft =  [  locli[q][0],     0  ]
                page.cropBox.upperRight = [  locli[q][0]+280, locli[q][1]   +15  ]

            writer = PyPDF2.PdfFileWriter()
            writer.addPage(page)
            out_file = infp.name[0:5] + str(locli[q][2]) + ".pdf"
            with open(out_file, 'wb') as outfp:
                writer.write(outfp)

class pdfPositionHandling:
    
    def parse_obj(self, lt_objs):

        # loop over the object list
        for obj in lt_objs:

            if isinstance(obj, pdfminer.layout.LTTextLine):
                # print("%6d, %6d, %s" % (obj.bbox[0], obj.bbox[1], obj.get_text().replace('\n', '_'))) 
                temp_txt = obj.get_text().replace('\n', '_')
                if temp_txt[0:2] == "문 ":
                    temp = []
                    temp.append(obj.bbox[0])
                    temp.append(obj.bbox[1])
                    temp.append( (obj.get_text().replace('\n', '_')).split('.')[0] )
                    temp[2] = int(temp[2].split(' ')[1])
                    li.append(temp)

            # if it's a textbox, also recurse
            if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
                self.parse_obj(obj._objs)

            # if it's a container, recurse
            elif isinstance(obj, pdfminer.layout.LTFigure):
                self.parse_obj(obj._objs)

    def parsepdf(self, filename, startpage, endpage):

        # Open a PDF file.
        fp = open(filename, 'rb')

        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)

        # Create a PDF document object that stores the document structure.
        # Password for initialization as 2nd parameter
        document = PDFDocument(parser)

        # Check if the document allows text extraction. If not, abort.
        if not document.is_extractable:
            raise PDFTextExtractionNotAllowed

        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()

        # Create a PDF device object.
        device = PDFDevice(rsrcmgr)

        # BEGIN LAYOUT ANALYSIS
        # Set parameters for analysis.
        laparams = LAParams()

        # Create a PDF page aggregator object.
        device = PDFPageAggregator(rsrcmgr, laparams=laparams)

            # Create a PDF interpreter object.
        interpreter = PDFPageInterpreter(rsrcmgr, device)


        i = 0
        # loop over all pages in the document
        for page in PDFPage.create_pages(document):
            if i >= startpage and i <= endpage:
                # read the page into a layout object
                interpreter.process_page(page)
                layout = device.get_result()

                # extract text from this object
                self.parse_obj(layout._objs)
                
                li.sort(key=lambda x:x[2])
                if len(li) != 0:
                    extract_tree(filename, li, i)

                print(li)
                del li[:]


            i += 1
