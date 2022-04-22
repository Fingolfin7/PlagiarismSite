import docx2txt
import PyPDF2
import os


def read_doc(filename, file_dir=r"C:\Users\Kuda\Documents\Programming\Django\PlagiarismSite\media"):
    path = os.path.join(file_dir, filename)
    print(path)

    if not os.path.exists(path):
        return

    if path.endswith(".docx") or path.endswith(".doc"):
        file_contents = docx2txt.process(path)
    elif path.endswith(".pdf"):
        with open(path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            file_contents = pdf_reader.getPage(0).extractText()
    else:
        file_contents = None

    return file_contents


if __name__ == "__main__":
    print(read_doc(r"C:\Users\Kuda\Documents\The Work of Wolves Asimov.docx", ""))
