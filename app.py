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
        
        # Inicializando uma lista para armazenar dados extraídos
        extracted_data = []
        
        # Percorrendo as páginas do PDF
        for page in pdf_reader.pages:
            text = page.extract_text()
            if text:
                # Aqui você deve processar o texto para extrair dados relevantes
                # Exemplo de como dividir o texto em linhas e colunas (ajuste conforme necessário)
                lines = text.split('\n')  # Divida o texto em linhas
                for line in lines:
                    # Divida cada linha em colunas (ajuste o delimitador conforme necessário)
                    columns = line.split()  # Aqui você pode usar um delimitador específico
                    extracted_data.append(columns)  # Adicione a linha extraída à lista
        
        # Crie um DataFrame a partir da lista extraída
        df = pd.DataFrame(extracted_data)
        
        # Retorne o DataFrame como JSON
        return jsonify(df.to_dict(orient='records'))  # Convertendo o DataFrame para um formato JSON

    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
