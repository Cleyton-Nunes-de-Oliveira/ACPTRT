
# 1.Extração de texto dos pdf das sentenças baixas
#
# Cria Corpus (DatasetClassification.CSV) das Sentenças do TRT1
# Le os arquivos .txt e armazena-os em uma lista e depois persiste-o em disco no formato .csv.
#
import io
import pathlib
import pandas as pd
import datasets
from datasets import load_dataset
from datasets import Dataset
from os import listdir
from os.path import isfile, join
import re

    
class Corpus():
    
    def __init__(self):
        # Agrupar estas variaveis em um arquivo para carregar nas classes.
        self.FOLDER_BASE = "/home/info/MyNotebooks/Datasets/SentencasTRT1/"
        #self.PDFs_FOLDER = self.FOLDER_BASE + "PDFs/"
        self.TXTs_FOLDER = self.FOLDER_BASE + "TXTs/"
        #self.CSV_FOLDER  = self.FOLDER_BASE + "CSV/"
        self.DS_FOLDER   = self.FOLDER_BASE + "DS/"
        self.ARQ_CSV     = "Corpus_Sentencas.csv"
        self.ARQ_DS      = "Corpus_Sentencas"
        
        
    def createDS(self):
        # Obtem a lista de arquivos txt no diretorio TXTs
        #files = [self.TXTs_FOLDER+f for f in listdir(self.TXTs_FOLDER) if (isfile(join(self.TXTs_FOLDER, f)) and pathlib.Path(file).suffix == ".txt") ]
        files = [self.TXTs_FOLDER+f for f in listdir(self.TXTs_FOLDER) if isfile(join(self.TXTs_FOLDER, f))]

        dataset = load_dataset('text', data_files=files)
        dataset.save_to_disk(self.DS_FOLDER)        
