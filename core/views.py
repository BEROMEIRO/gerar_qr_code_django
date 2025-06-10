from django.shortcuts import render
from .forms import QRCodeForm
import pandas as pd
import qrcode
from io import BytesIO
from django.http import HttpResponse
from base64 import b64encode

def gerar_qrcode_unico(texto_total):
    qr = qrcode.QRCode(
        version=2,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )
    qr.add_data(texto_total)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def home(request):
    img_data = None
    msg = None

    if request.method == 'POST':
        form = QRCodeForm(request.POST, request.FILES)
        if form.is_valid():
            texto = form.cleaned_data.get('texto') or ''
            arquivo = form.cleaned_data.get('arquivo')
            coluna = form.cleaned_data.get('coluna') or 'serial'
            separador = form.cleaned_data['separador']

            if separador == "newline":
                separador = "\n"
            elif separador == "comma":
                separador = ","
            elif separador == "semicolon":
                separador = ";"

            dados_texto = [linha.strip() for linha in texto.splitlines() if linha.strip()]
            dados_excel = []

            if arquivo:
                try:
                    df = pd.read_excel(arquivo)
                    if coluna in df.columns:
                        dados_excel = df[coluna].dropna().astype(str).tolist()
                        msg = f"✅ {len(dados_excel)} registros carregados do Excel."
                    else:
                        msg = "⚠️ Coluna não encontrada na planilha."
                except Exception as e:
                    msg = f"❌ Erro ao ler o arquivo: {e}"

            dados_combinados = list(dict.fromkeys(dados_texto + dados_excel))

            if dados_combinados:
                texto_final = separador.join(dados_combinados)
                buffer = gerar_qrcode_unico(texto_final)
                img_base64 = b64encode(buffer.getvalue()).decode()
                img_data = f"data:image/png;base64,{img_base64}"
            else:
                msg = "ℹ️ Insira dados no campo de texto ou envie um arquivo Excel."
    else:
        form = QRCodeForm(initial={'separador': 'newline'})

    return render(request, "core/home.html", {"form": form, "img_data": img_data, "msg": msg})
