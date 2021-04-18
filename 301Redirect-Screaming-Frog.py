import pandas as pd
import streamlit as st
import os
import base64
from io import BytesIO

#Import CSV

st.title('Redirections 301 - Screaming Frog')
st.write("Correspondance automatique des 301")
st.write("Ajout d'une phrase pour tester le push")
st.write("Demo : URL")

st.markdown('## ** ① Chargez le fichier CSV des 301 **') 
st.markdown('')

upload1 = st.file_uploader("Choisissez votre fichier (CSV): ", key="1")
df_301 = pd.read_csv(upload1)
st.write('Aperçu :')
st.write(df_301.head())

st.markdown('## ** ② Chargez le fichier CSV des inlinks 301 **') 
st.markdown('')

upload2 = st.file_uploader("Choisissez votre fichier (CSV): ", key="2")
df_inlinks = pd.read_csv(upload2)
st.write('Aperçu :')
st.write(df_inlinks.head())

#Reorganize DF

df_301 = df_301[['Address', 'Redirect URL', 'Status Code']]
df_301 = df_301.rename({'Address': 'URL Redirigée','Redirect URL': 'URL Finale'}, axis=1) 
df_inlinks = df_inlinks[['Source', 'Destination', 'Anchor', 'Link Position']]
df_inlinks = df_inlinks.rename({'Source': 'URL Source','Destination': 'URL Redirigée'}, axis=1)

#Regroup data in 1DF

df = pd.merge(df_inlinks, df_301, how='right', on=['URL Redirigée'])
df = df[["URL Source", "URL Redirigée", "URL Finale", "Status Code", "Anchor", "Link Position"]]
df = df.rename({"URL Finale": "URL Finale (à remplacer dans l'URL source)"}, axis=1)

# #Export in XLSX

st.markdown('## **③ Téléchargez le fichier XLSX**') 
st.markdown('')

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name="Pages en 301 avec l'URL Source")
    workbook = writer.book
    center = workbook.add_format({'align': 'center'})
    worksheet = writer.sheets["Pages en 301 avec l'URL Source"]
    worksheet.set_column('A:A', 10)
    worksheet.set_column('B:D', 70)
    worksheet.set_column('E:E', 15, center)
    worksheet.set_column('F:G', 20)

    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val) 
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="Redirections_301_Full.xlsx">➤ Cliquez pour télécharger</a>' # decode b'abc' => abc

st.markdown(get_table_download_link(df), unsafe_allow_html=True)