import pdf_mining_and_crop_only_questions
import os

t = pdf_mining_and_crop_only_questions.pdfPositionHandling()
file = "2019_국가직_9급_컴퓨터일반(나)_2019년.pdf"

def search(dirname):
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                tmp = filename[8]
                if tmp != "답" and ext == '.pdf' and not(tmp.isdigit()):
                    # print(full_filename)
                    t.parsepdf(full_filename,dirname,filename,0,0)
    except PermissionError:
        pass

search("C:/Users/LSY/OneDrive/Archive/전산공부/0_전산공무원문제정리/")
#t.parsepdf("C:/Users/LSY/OneDrive/Archive/전산공부/0_전산공무원문제정리/7급/7급_데이터베이스/2014_7급_데이터베이스론-A.pdf","C:/Users/LSY/OneDrive/Archive/전산공부/0_전산공무원문제정리/7급/7급_데이터베이스/","2014_7급_데이터베이스론-A.pdf",0,0)
