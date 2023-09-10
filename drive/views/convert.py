import os

import PyPDF2
from django.http import JsonResponse
from django.shortcuts import render, redirect

from drive.forms import PDFUploadForm
from drive.models import PDFDocument
from drive.utils import speech_to_text_pipeline


def upload_pdf(request):
    if request.method == 'POST':
        form = PDFUploadForm(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf_file']
            # Extract the original file name without the extension
            pdf_file_name = os.path.splitext(pdf_file.name)[0]
            pdf_text = extract_text_from_pdf(pdf_file)
            pdf_doc = PDFDocument(title=pdf_file_name, text_content=pdf_text)
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


# Charts but lamda not installed
# def Chart(request):
#     file = Files.objects.all()
#     folder = Folder.objects.all()
#     fig = px.line(
#         x=[c.upload_date for c in file],
#         y=[c.upload_date for c in folder]
#     )
#     chart = fig.to_html()
#     context = {'chart': chart}
#     return render(request, 'chart.html', context)

# appname/views.py


def speech_to_text(request):
    if request.method == 'POST':
        try:
            text = speech_to_text_pipeline(request.FILES['audio'])
            return JsonResponse({'text': text})
        except Exception as e:
            return JsonResponse({'error': str(e)})

    return render(request, 'speech_to_text.html')
