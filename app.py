from flask import Flask, request, jsonify
import pandas as pd
import pdfplumber  # Use pdfplumber para melhor extração de texto

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    
    if file and file.filename.endswith('.pdf'):
        # Armazena as informações extraídas
        extracted_data = []

        with pdfplumber.open(file) as pdf:
            capturing = False
            for page in pdf.pages:
                text = page.extract_text()
                lines = text.split('\n')  # Divide o texto em linhas
                
                # Verifica se está entre as palavras-chave
                for line in lines:
                    if "DAs classificados por pontuação geral, em ordem decrescente" in line:
                        capturing = True
                        continue
                    elif "Definição das Métricas" in line:
                        capturing = False
                        break

                    if capturing:
                        # Processa cada linha capturada
                        # Pode ser necessário ajustar a lógica de como você extrai os dados
                        parts = line.split()  # Ajuste conforme necessário
                        if len(parts) >= 9:  # Certifique-se de que tem dados suficientes
                            data = {
                                "#": parts[0],
                                "Transporter ID": parts[1],
                                "Desempenho Score": parts[2],
                                "Pacotes Entregues": parts[3],
                                "DCR": parts[4],
                                "DNR DPMO": parts[5],
                                "Contact Compliance": parts[6],
                                "Swipe to Finish Compliance": parts[7],
                                "100% WHC": parts[8],
                                "Desempenho": ' '.join(parts[9:])  # Pega o restante como "Desempenho"
                            }
                            extracted_data.append(data)

        return jsonify(extracted_data)  # Retorna os dados como JSON

    return jsonify({'error': 'Invalid file type'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
