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
        # Aqui você pode extrair as tabelas do PDF e transformá-las em DataFrame
        # Isso é apenas um exemplo, você deve adaptar para a sua lógica de extração
        tables = []  # Aqui você deve armazenar suas tabelas
        for page in pdf_reader.pages:
            text = page.extract_text()
            tables.append(text)  # Processar para extrair tabelas
        
        return jsonify({'tables': tables})  # Retornar as tabelas como resposta

    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
