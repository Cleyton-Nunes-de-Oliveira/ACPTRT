# 4. DATA WRANGLING (com o dataset criado) PROPRIAMENTE:

import datasets
import re
from datasets import Dataset


class DataWrang():
    
    def __init__(self):
        # Carregamento do Dataset criado
        self.FOLDER_BASE = "/home/info/MyNotebooks/Datasets/SentencasTRT1/"
        self.DS_FOLDER   = self.FOLDER_BASE + "DS/"
        #ARQ_DS      = "Corpus_Sentencas"

        self.padraoImproc   = "improcedentes|improcedente"
        self.padraoParcProc = "procedentes em parte|procedente em parte|parcialmente procedentes|parcialmente procedente|parcialmente improcedentes|parcialmente improcedente"
        self.padraoProc     = "procedentes|procedente"
        self.padraoAcordo   = "acordo|Acordo"
        self.tam_tokeniz = 1400

        # Armazenamento em listas dos dados extraidos dos arquivos .txt para formação do novo dataset.
        self.textos         = list()
        self.dispositivos   = list()
        self.classificacoes = list()
        
        self.i = 1
        


    def extraiDispositivo(self, pattern, text):
        padrao = pattern

        texto_inicio = 0
        texto_fim    = 0

        for match in re.finditer(pattern, text.lower()):
            index = match.start()  
            value = match.group()
            print(index, value) # match only one? parece que esta encontrando outras correspondencias também.

            span = (self.tam_tokeniz - len(padrao))/2
            texto_inicio = int(match.start() - span)
            texto_fim    = int(match.start() + len(padrao) + span)
            if(texto_fim > len(text)): # nao pode ser maior que o tamanho da string
                texto_fim = len(text)

            #print(texto_inicio, texto_fim)
            #print(index)

        return(text[texto_inicio:texto_fim])

    #def preprocess_function(examples):
    #    return tokenizer(examples["text"], truncation=True)    


    def classDispositivo(self, examples):     
        
        texto = examples

        t_par    = ""
        t_imp    = ""
        t_proc   = ""
        t_outros = ""

        # parece que esta encontrando outras correspondencias também.
        t_par    = self.extraiDispositivo(self.padraoParcProc, texto)


        if len(t_par) != 0:
            dispositivo   = t_par
            classificacao = "Parcialmente procedente"
            #break
        else: 
            t_imp    = self.extraiDispositivo(self.padraoImproc, texto)
            if len(t_imp) != 0:
                dispositivo   = t_imp
                classificacao = "Improcedente"
                #break
            else: 
                t_proc   = self.extraiDispositivo(self.padraoProc, texto)
                if len(t_proc) != 0:
                    dispositivo   = t_proc
                    classificacao = "Procedente"
                    #break
                else:
                    t_outros = self.extraiDispositivo(self.padraoAcordo, texto)
                    if len(t_outros) != 0:
                        dispositivo   = t_outros
                        classificacao = "Acordo ou outros"
                    else:
                        classificacao = "Nenhuma"
                        dispositivo   = texto[self.tam_tokeniz:-1]
                    # Coloca outro if aninhando e por fim, no else residual, colocar uma flag ("none"?).
                    # Posteriormente, filtrar no dataset classificado aqueles com a flag que nao puderam
                    #  receber nenhuma das classificacoes anteriores e exclui-los do dataset anotado.

        print("PDF: ", self.i, " - Class.: ", classificacao," - Disp.: ", dispositivo)  
        self.i = self.i + 1
        self.textos.append(texto)
        self.dispositivos.append(dispositivo)
        self.classificacoes.append(classificacao)


        return(classificacao)

    
    def proccessAndSaveDsAnot(self):
        listSent  = datasets.load_from_disk(self.DS_FOLDER)['train']['text']
        print("Tam. list. Sent: ", len(listSent), " - Tipo: ", type(listSent))
        listClass = list(map(self.classDispositivo, listSent))
        print("Tam. list. Class: ", len(listClass), " - Tipo: ", type(listClass))
        
        #print("Tam. inicial DS Sent: ")
        #print(len(self.datasetSent))        # 994
        #print("Tipo. DS Sent: ")
        #print(type(self.datasetSent))       # <class 'datasets.arrow_dataset.Dataset'>
        #print(self.datasetSent['text'][0])
        
        # Executa a Extração e  Classificação Regex de Dispositivos e cria Dataset Anotado
        #dados = list(self.datasetSent.map(self.classDispositivo, batched=False))
        #print("Tamanho do DS dados: ")
        #print(len(dados))
         # Salva Dataset Classificado
        # df.head()
        # dados = [textos,dispositivos,classificacoes]
        # Testar a existencia da pasta DsClassAnot e cria-la, caso nao exista
        dados = list(zip(self.textos,self.dispositivos,self.classificacoes))
        print(len(dados))
        #print(len(dados[0]))
        #dados = {'text':self.textos,'disp':self.dispositivos, 'label':self.classificacoes}
        # {column_name → [list of values per element]
       
        # Cria os arquivos na pasta (...)/SentencasTRT1/DsClassAnot
        df = pd.DataFrame(dados, columns=['text','disp','label'])
        dsAnot = Dataset.from_pandas(df)
        #DsClassAnot = Dataset.from_pandas(classifiedDF)
        dsAnot.save_to_disk(self.FOLDER_BASE +"DsClassAnot/")

