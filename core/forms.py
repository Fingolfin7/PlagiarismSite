from django import forms


class DocumentForm(forms.Form):
    doc1 = forms.FileField(widget=forms.FileInput(attrs={'accept': '.doc, .docx, .pdf'}))
    doc2 = forms.FileField(widget=forms.FileInput(attrs={'accept': '.doc, .docx, .pdf'}))

    class Meta:
        fields = ['doc1', 'doc2']


class MultiDocumentForm(forms.Form):
    documents = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False)
