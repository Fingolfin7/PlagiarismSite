from django import forms


class DocumentForm(forms.Form):
    doc1 = forms.FileField(widget=forms.FileInput(attrs={'accept': '.doc, .docx, .pdf'}))
    doc2 = forms.FileField(widget=forms.FileInput(attrs={'accept': '.doc, .docx, .pdf'}))

    class Meta:
        fields = ['doc1', 'doc2']
