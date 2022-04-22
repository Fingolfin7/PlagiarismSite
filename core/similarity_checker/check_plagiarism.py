import os
# extract the text from word documents and pdfs
from .read_docx import read_doc
# cosine_similarity  is a technique used in language processing to find the similarity of two bodies of text
from .cosine_similarity import cosine_similarity
# python AI, module that allows us to 'vectorize' text (i.e turn text to numbers) to be used in
# the cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def vectorize(Text):
    return TfidfVectorizer().fit_transform(Text).toarray()


def compare_docs(fileOne, fileTwo):
    file_one = read_doc(fileOne)
    file_two = read_doc(fileTwo)

    s_vectors = list(zip([fileOne, fileTwo], vectorize([file_one, file_two])))
    sim_score = 0

    for file_a, text_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((file_a, text_a))
        del new_vectors[current_index]
        for file_b, text_b in new_vectors:
            sim_score = cosine_similarity(text_a, text_b)
    print(sim_score)
    return sim_score


def multiple_doc_check(dir_path):
    filenames = [file for file in os.listdir(dir_path)]
    file_texts = [read_doc(_file, dir_path) for _file in filenames]

    vectors = vectorize(file_texts)
    s_vectors = list(zip(filenames, vectors))

    plagiarism_results = set()

    for file_a, text_a in s_vectors:
        new_vectors = s_vectors.copy()
        current_index = new_vectors.index((file_a, text_a))
        del new_vectors[current_index]
        for file_b, text_b in new_vectors:
            sim_score = cosine_similarity(text_a, text_b)
            student_pair = sorted((file_a, file_b))
            plagiarism_results.add((student_pair[0], student_pair[1], sim_score))

    return plagiarism_results
