from flask import Flask, request, jsonify
import pdfplumber
import pandas as pd

app = Flask(__name__)

@app.route('/extract-tables', methods=['POST'])
def extract_tables():
    file = request.files['pdf']
    pdf = pdfplumber.open(file)

    dataframes = []
    for page in pdf.pages:
        tables = page.extract_tables()
        for table in tables:
            df = pd.DataFrame(table[1:], columns=table[0])
            dataframes.append(df.to_json())

    pdf.close()
    return jsonify({'dataframes': dataframes})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)