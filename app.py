from flask import Flask, request, jsonify
import pandas as pd
from io import BytesIO
import PyPDF2  # Certifique-se de ter esta biblioteca instalada

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and file.filename.endswith('.pdf'):
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Inicializando variáveis
        content_between_keywords = []
        capturing = False

        # Extrair texto e capturar entre as palavras-chave
        for page in pdf_reader.pages:
            text = page.extract_text()
            if "DAs classificados por pontuação geral, em ordem decrescente..." in text:
                capturing = True
            elif "Definição das Métricas" in text:
                capturing = False

            if capturing:
                content_between_keywords.append(text)

        # Processar e formatar o conteúdo capturado
        df = process_extracted_content(content_between_keywords)

        return jsonify(df.to_dict(orient='records'))  # Retornar como JSON

    return jsonify({'error': 'Invalid file type'})

def process_extracted_content(content):
    # Aqui você deve implementar a lógica para formatar o conteúdo extraído em um DataFrame
    # Exemplo básico para transformar em um DataFrame
    data = []
    for entry in content:
        lines = entry.splitlines()
        for line in lines:
            if line.strip():  # Ignora linhas vazias
                data.append(line.split(','))  # Supondo que os dados estão separados por vírgula
    
    # Ajuste conforme necessário para formar o DataFrame corretamente
    columns = ["#", "Transporter ID", "Desempenho Score", "Pacotes Entregues", "DCR", "DNR DPMO", "Contact Compliance", "Swipe to Finish Compliance", "100% WHC", "Desempenho"]
    return pd.DataFrame(data, columns=columns)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
