import os

from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from reportlab.lib.styles import getSampleStyleSheet

from core.forms import DocumentForm, MultiDocumentForm
from core.models import History
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .similarity_checker.check_plagiarism import compare_docs
from .similarity_checker.citations import get_citations
from .similarity_checker.read_docx import read_doc
from django.shortcuts import render
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph


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


@login_required
def compare_multiple(request):
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
        # clean uploaded docs
        print(request.FILES)
        uploaded_docs = request.FILES.getlist('documents')

        num_docs = len(uploaded_docs)

        try:
            scan_results = []

            for i in range(num_docs):
                # create document objects from the uploaded file path (to get rid of the document not subscriptable error)
                for j in range(i + 1, num_docs):
                    doc1 = uploaded_docs[i]
                    doc2 = uploaded_docs[j]

                    # saves uploaded documents to "media"
                    fs = FileSystemStorage()
                    doc1_name = fs.save(doc1.name, doc1)
                    doc2_name = fs.save(doc2.name, doc2)

                    # get similarity and citation count
                    sim = compare_docs(doc1_name, doc2_name)
                    doc1_citations = get_citations(read_doc(doc1_name))
                    doc2_citations = get_citations(read_doc(doc2_name))

                    # save to history in database
                    log_to_history = History(doc1=doc1_name[:doc1_name.rfind("_")], doc2=doc2_name[:doc2_name.rfind("_")], similarity=sim, user=request.user)
                    log_to_history.save()

                    # delete documents from "media"
                    fs.delete(doc1_name)
                    fs.delete(doc2_name)

                    scan_results.append({
                        "doc1": doc1_name[:doc1_name.rfind("_")],
                        "doc2": doc2_name[:doc2_name.rfind("_")],
                        "citations1": doc1_citations,
                        "citations2": doc2_citations,
                        "similarity": sim
                    })


            return render(request, 'core/multi_doc_comparison.html', {
                'form': MultiDocumentForm(),
                'title': "Multiple Documents Comparison Results",
                'results': scan_results,
                'history': hist
            })
        # if scan failed, print error message
        except Exception as e:
            messages.error(request, f"{str(e).capitalize()}. Scan Failed. Please try again")


    return render(request, 'core/multi_doc_comparison.html', {
        'history': hist
    })


@login_required
def generate_report(request):
    # Fetch the scan history from the database
    scan_history = History.objects.filter(user=request.user).order_by('-id')

    # Create a response object with appropriate headers for PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="scan_report.pdf"'

    # Create a PDF document using ReportLab
    doc = SimpleDocTemplate(response, pagesize=landscape(letter),
                            title=f"{request.user.username.capitalize()} Scan History")

    # Create a list of data for the PDF table
    data = [['Document 1', 'Document 2', 'Similarity', 'Date']]
    for entry in scan_history:
        data.append([entry.doc1, entry.doc2, round(entry.similarity, 3), entry.date.date()])

    # Create a PDF table and set its style
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    # Build the PDF document
    styles = getSampleStyleSheet()
    title = Paragraph(f"<title>{request.user.username.capitalize()} Scan History</title>", styles["Title"])
    elements = [title, table]
    doc.build(elements)

    return response

