import os
import re
import PyPDF2
import pymysql
import logging
from PyPDF2 import PdfReader

conexao = pymysql.connect(host='',user='',passwd='',db='')
#Lendo os diretorios
diretorio = "C:/NF_Danfe"
#Array de diretorios
arquivos_pdf = []
#Lendo todos os arruivos e exibindo quantidade
for nome_arquivo in os.listdir(diretorio):
    if nome_arquivo.lower().endswith('.pdf'):
        arquivos_pdf.append(nome_arquivo)

quantidade_pdf = len(arquivos_pdf)
print(f'Quantidade de arquivos PDF encontrados: {quantidade_pdf}')

# Loop para acessar cada arquivo PDF
for nome_arquivo in arquivos_pdf:
    caminho_arquivo = os.path.join(diretorio, nome_arquivo)
    pdf_reader = PdfReader(caminho_arquivo)
    
    # Acessa o conteúdo do PDF
    for pagina in pdf_reader.pages:
        conteudo_pdf = pagina.extract_text()
        #print(f'Conteúdo da páginazinha do arquivozinho "{nome_arquivo}":\n{conteudo}\n')

        # Escrever o conteúdo do PDF em um arquivo TXT

   
        NumeroNota = re.findall('\n(\d{3}.\d{3}.\d{3})\n',conteudo_pdf)
        CnpjPrestador = re.findall('\s(\d{2}.\d{3}.\d{3}\/\d{4}\-\d{2})',conteudo_pdf)
        CnpjTomador = re.findall('\s(\d{3}.\d{3}.\d{3}\-\d{2})',conteudo_pdf)
        NomePrestador = re.findall('BEMOS\s\w+\s(\w+\s?\w+\s?\w+\s?\w+)',conteudo_pdf)
        NomeTomador = re.findall('\n(\w+\s\w+\s\w+\s\w+)\s\d{3}.\d{3}.\d{3}',conteudo_pdf)
        ValorNota = re.findall('\s\d{2}\,\d{2}\s(\d[0-9]?\d{1}?\,\d{2})',conteudo_pdf)
        Municipio = re.findall('\s?(\w+)\,?\s?\w\w\s\-\s\w+\:',conteudo_pdf)
        ICMS = re.findall('\d{2}\,\d{2}\n(\d{1}\,\d{2})',conteudo_pdf)
        DataEmissao = re.findall('\w+(\d{2}\/\d{2}\/\d{4})',conteudo_pdf)

        #print(NumeroNota, CnpjTomador, CnpjPrestador, NomePrestador, NomeTomador, ValorNota,Municipio, DataEmissao)
        cursor = conexao.cursor()
        #Valida se os valores retornaram vazio, se sim, nao insere no banco.

        VAR = (NomePrestador, NomeTomador, NumeroNota, CnpjPrestador, CnpjTomador, ValorNota, Municipio, DataEmissao)
        if (VAR) == 0 :
            ValorNota = 0
            #Marca flag falha no banco de dados
         

        SQL = "INSERT INTO nf_danfe (NomePrestador, NomeTomador, NumeroNota, CnpjPrestador, CnpjTomador, ValorNota, Municipio, DataEmissao) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        VAR = (NomePrestador, NomeTomador, NumeroNota, CnpjPrestador, CnpjTomador, ValorNota, Municipio, DataEmissao)
        
        try:

            cursor.execute((SQL), (VAR))
            cursor.execute("INSERT INTO exec (tipo, data) VALUES ('Sucesso', NOW())")
            conexao.commit()
            print("Sucesso")
        except:
            print("Falha")
            cursor.execute("INSERT INTO exec (tipo, data) VALUES ('Falha', NOW())")
            conexao.commit()
          