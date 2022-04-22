import re

author = "(?:[A-Z][A-Za-z'`-]+)"
etal = "(?:et al.?)"
additional = "(?:,? (?:(?:and |& )?" + author + "|" + etal + "))"
year_num = "(?:19|20)[0-9][0-9]"
page_num = "(?:, p.? [0-9]+)?"  # Always optional
year = "(?:, *" + year_num + page_num + "| *\(" + year_num + page_num + "\))"
regex = "(" + author + additional + "*" + year + ")"
citations = re.compile(regex)


def get_citations(text):
    c_list = citations.findall(text)
    c_count = len(c_list)
    return c_count, c_list


def remove_citations(text):
    return citations.sub(text, "")


if __name__ == "__main__":
    from read_docx import read_doc
    doc = read_doc(r"C:\Users\Kuda\Downloads\SAD Assignments"
                   r"\Kudakwashe Henry Mushunje R191584H SAD Assignment.docx")
    print(get_citations(doc))
