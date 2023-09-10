# pdfapp/views.py
import PyPDF2
from django.shortcuts import render, redirect

from drive.forms import PDFUploadForm
from drive.models import PDFDocument


def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            pdf_file = form.cleaned_data['pdf_file']
            pdf_text = extract_text_from_pdf(pdf_file)
            pdf_doc = PDFDocument(title=title, text_content=pdf_text)
            pdf_doc.save()
            return redirect('pdf_list')
    else:
        form = PDFUploadForm()
    return render(request, 'upload_pdf.html', {'form': form})


def pdf_list(request):
    pdf_documents = PDFDocument.objects.all()
    return render(request, 'pdf_list.html', {'pdf_documents': pdf_documents})


def extract_text_from_pdf(pdf_file):
    pdf_text = ""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        pdf_text += page.extract_text()
    return pdf_text
