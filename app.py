from flask import Flask,render_template,url_for,request, jsonify
import re
import pandas as pd
import spacy
from spacy import displacy
import en_core_web_md
import json 

# @TASK : Load model bahasa 
nlp = en_core_web_md.load()
# END OF TASK 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process',methods=["POST"])
def process():
    if request.method == 'POST':
        choice = request.form['taskoption']
        rawtext = request.form['rawtext']
        doc = nlp(rawtext)
        d = []
        if len(doc.ents) > 0:
            for ent in doc.ents:
                d.append((ent.label_, ent.text))
                df = pd.DataFrame(d, columns=['category', 'value'])
                
                ORG_named_entity = df.query("category == 'ORG'")['value'] # Subset semua entitas dengan kategori 'ORG'
                PERSON_named_entity = df.query("category == 'PERSON'")['value'] # Subset semua entitas dengan kategori 'PERSON'
                GPE_named_entity = df.query("category == 'GPE'")['value'] # Subset semua entitas dengan kategori 'GPE'
                MONEY_named_entity = df.query("category == 'MONEY'")['value'] # Subset semua entitas dengan kategori 'MONEY'
                NORP_named_entity = df.query("category == 'NORP'")['value']
                CARDINAL_named_entity = df.query("category == 'CARDINAL'")['value']
                DATE_named_entity = df.query("category == 'DATE'")['value']
                EVENT_named_entity = df.query("category == 'EVENT'")['value']
                FAC_named_entity = df.query("category == 'FAC'")['value']
                LANGUAGE_named_entity = df.query("category == 'LANGUAGE'")['value']
                LAW_named_entity = df.query("category == 'LAW'")['value']
                LOC_named_entity = df.query("category == 'LOC'")['value']
                ORDINAL_named_entity = df.query("category == 'ORDINAL'")['value']
                PRODUCT_named_entity = df.query("category == 'PRODUCT'")['value']
                QTY_named_entity = df.query("category == 'QUANTITY'")['value']
                TIME_named_entity = df.query("category == 'TIME'")['value']
                # END OF TASK 

            if choice == 'organisation':
                results = ORG_named_entity
                num_of_results = len(results)
            elif choice == 'person':
                results = PERSON_named_entity
                num_of_results = len(results)
            elif choice == 'geopolitical':
                results = GPE_named_entity
                num_of_results = len(results)
            elif choice == 'money':
                results = MONEY_named_entity
                num_of_results = len(results)
            elif choice == 'nationalities_religious_political_groups':
                results = NORP_named_entity
                num_of_results = len(results)
            elif choice == 'cardinal':
                results = CARDINAL_named_entity
                num_of_results = len(results)
            elif choice == 'date':
                results = DATE_named_entity
                num_of_results = len(results)
            elif choice == 'event':
                results = EVENT_named_entity
                num_of_results = len(results)
            elif choice == 'facility':
                results = FAC_named_entity
                num_of_results = len(results)
            elif choice == 'language':
                results = LANGUAGE_named_entity
                num_of_results = len(results)
            elif choice == 'law':
                results = LAW_named_entity
                num_of_results = len(results)
            elif choice == 'location':
                results = LOC_named_entity
                num_of_results = len(results)
            elif choice == 'ordinal':
                results = ORDINAL_named_entity
                num_of_results = len(results)
            elif choice == 'product':
                results = PRODUCT_named_entity
                num_of_results = len(results)
            elif choice == 'quantity':
                results = QTY_named_entity
                num_of_results = len(results)
            elif choice == 'time':
                results = TIME_named_entity
                num_of_results = len(results)
            elif choice == 'Select Category':
                results = pd.DataFrame()
                num_of_results = len(results)
        else:
            results = pd.DataFrame()
            num_of_results = len(results)
   
    return render_template("index.html", results = results, num_of_results = num_of_results, original_text = rawtext)

@app.route('/endpoint_tertentu')
def nama_fungsi_tertentu():
    return ("Fungsi ini akan dijalankan saat endpoint tersebut diakses")

@app.route('/endpoint_get', methods=['GET'])
def contoh_get():
    return ("Contoh endpoint get")

@app.route('/endpoint_post', methods=['POST'])
def contoh_post():
    return ("Contoh endpoint post")

@app.route('/endpoint_multi', methods=['GET', 'POST'])
def multi_method():
    if request.method == 'POST':
        return ("Nilai ini akan dikembalikan jika endpoint ini diakses dengan method POST")
    else : 
        return ("Nilai ini akan dikembalikan jika endpoint ini diakses dengan method GET")

@app.route('/tes_send_json', methods=['POST'])
def tes_send_json():
    data = request.get_json() 
    nama = data['nama']
    usia = data['usia']
    pekerjaan = data['pekerjaan']
    return ("Halo, {nama}. Usiamu adalah {usia} dan pekerjaanmu adalah {pekerjaan}".format(nama=nama, usia=usia, pekerjaan=pekerjaan))

@app.route('/tes_return_json', methods=['POST'])
def tes_return_json():
    data = request.get_json() 
    df = pd.DataFrame([data])

    return (df.to_json())

@app.route('/get_entities', methods=['POST'])
def get_entities():
    
    data = request.get_json()
    text = data['text']
    doc = nlp(text)
    d = [(ent.label_, ent.text) for ent in doc.ents]
    df = pd.DataFrame(d, columns = ['category', 'value'])
    
    return (df.to_json())

@app.route('/get_entities_normalized', methods=['POST'])
def get_entities_normalizedfoo():
    data = request.get_json() # load received json data
    text = data['text'] # extract 'text' element 
    doc = nlp(text) #
    d = [(ent.label_, ent.text) for ent in doc.ents]
    df = pd.DataFrame(d, columns=['category', 'value'])
    dictionary = {}
    for i in df['category'].unique():
        values = df.query(f"category == '{i}' ")['value'].to_list()
        dictionary[i] = values
    return json.dumps(dictionary)

if __name__ == '__main__':
    app.run(debug=True)
