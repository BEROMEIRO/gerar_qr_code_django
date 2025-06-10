from django import forms

class QRCodeForm(forms.Form):
    texto = forms.CharField(widget=forms.Textarea(attrs={'rows': 8}), required=False, label="📜 Texto com serial")
    arquivo = forms.FileField(required=False, label="📁 Envie um arquivo Excel (.xlsx)")
    coluna = forms.CharField(max_length=100, required=False, initial='serial', label="Nome da coluna com os dados")
    separador = forms.ChoiceField(
        choices=[
            ("newline", "\\n (quebra de linha)"),
            ("comma", ", (vírgula)"),
            ("semicolon", "; (ponto e vírgula)")
        ],
        label="Separar os dados dentro do QR Code por",
        initial="newline",
        required=True
    )

