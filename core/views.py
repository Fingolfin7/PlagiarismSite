from datetime import date
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from core.forms import DocumentForm
from core.models import History
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .similarity_checker.check_plagiarism import compare_docs
from .similarity_checker.citations import get_citations
from .similarity_checker.read_docx import read_doc


@login_required
def upload_docs(request):
    # getting the history of the user's scans
    filtered = History.objects.filter(user=request.user).order_by('-id')
    if len(filtered) >= 5:
        hist = filtered[:5]
    elif len(filtered) < 5:
        hist = filtered
    else:
        hist = []

    # processing uploaded docs
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            # clean uploaded docs
            doc1 = form.cleaned_data.get('doc1')
            doc2 = form.cleaned_data.get('doc2')

            # saves uploaded documents to "media"
            fs = FileSystemStorage()
            doc1_name = fs.save(doc1.name, doc1)
            doc2_name = fs.save(doc2.name, doc2)

            try:
                # get similarity and citation count
                sim = compare_docs(doc1_name, doc2_name)
                doc1_citations = get_citations(read_doc(doc1_name))
                doc2_citations = get_citations(read_doc(doc2_name))

                # save to history in database
                log_to_history = History(doc1=doc1_name, doc2=doc2_name, similarity=sim, user=request.user)
                log_to_history.save()

                # delete documents from "media"
                fs.delete(doc1_name)
                fs.delete(doc2_name)

                scan_results = {
                    "doc1": doc1_name,
                    "doc2": doc2_name,
                    "citations1": doc1_citations,
                    "citations2": doc2_citations,
                    "similarity": sim
                }

                return render(request, 'core/PlagiarismChecker.html', {
                    'form': DocumentForm(),
                    'title': "Scan Results",
                    'results': scan_results,
                    'history': hist
                })
            # if scan failed, print error message
            except Exception as e:
                form = DocumentForm()
                fs.delete(doc1_name)
                fs.delete(doc2_name)
                messages.error(request, f"{str(e).capitalize()}. Scan Failed. Please try again")

    else:
        form = DocumentForm()

    return render(request, 'core/PlagiarismChecker.html', {
        'form': form,
        'history': hist
    })
