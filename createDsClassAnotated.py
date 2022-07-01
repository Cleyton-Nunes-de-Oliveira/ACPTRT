
# 12.
#
# Copia que funcionou sem as variaveis:
import datasets
import re
from datasets import Dataset

# Carregamento do Dataset criado
FOLDER_BASE = "/home/info/MyNotebooks/Datasets/SentencasTRT1/"
DS_FOLDER   = FOLDER_BASE + "DS/"
ARQ_DS      = "Corpus_Sentencas"

ds = datasets.load_from_disk(DS_FOLDER)


padraoImproc   = "improcedentes|improcedente"
padraoParcProc = "procedentes em parte|procedente em parte|parcialmente procedentes|parcialmente procedente|parcialmente improcedentes|parcialmente improcedente"
padraoProc     = "procedentes|procedente"
padraoOutros   = "DISPOSITIVO"
tam_tokeniz = 1400


# Armazenamento em listas dos dados extraidos dos arquivos .txt para formação do novo dataset.
textos         = list()
dispositivos   = list()
classificacoes = list()


def extraiDispositivo(pattern, text):
    padrao = pattern
    
    texto_inicio = 0
    texto_fim    = 0
    
    for match in re.finditer(pattern, text.lower()):
        index = match.start()  
        value = match.group()
        print(index, value) # match only one? parece que esta encontrando outras correspondencias também.

        span = (tam_tokeniz - len(padrao))/2
        texto_inicio = int(match.start() - span)
        texto_fim    = int(match.start() + len(padrao) + span)
        if(texto_fim > len(text)): # nao pode ser maior que o tamanho da string
            texto_fim = len(text)
        
        #print(texto_inicio, texto_fim)
        #print(index)

    return(text[texto_inicio:texto_fim])

#def preprocess_function(examples):
#    return tokenizer(examples["text"], truncation=True)    
    
    
def classDispositivo(examples):
    sentencas    = examples['text']
    
    for i in range(len(sentencas)):
        
        texto = sentencas[i]
        
        t_imp    = ""
        t_par    = ""
        t_proc   = ""
        t_outros = ""
        
        # parece que esta encontrando outras correspondencias também.
        t_par    = extraiDispositivo(padraoParcProc, texto)
        
             
        if len(t_par) != 0:
            dispositivo   = t_par
            classificacao = "Parcialmente procedente"
            #break
        else: 
            t_imp    = extraiDispositivo(padraoImproc, texto)
            if len(t_imp) != 0:
                dispositivo   = t_imp
                classificacao = "Improcedente"
                #break
            else: 
                t_proc   = extraiDispositivo(padraoProc, texto)
                if len(t_proc) != 0:
                    dispositivo   = t_proc
                    classificacao = "Procedente"
                    #break
                else:
                    t_outros = extraiDispositivo(padraoOutros, texto)
                    dispositivo   = texto[tam_tokeniz:-1]
                    classificacao = "Acordo ou outros"
         
        print(i," - ",classificacao," - ", dispositivo)            
        textos.append(texto)
        dispositivos.append(dispositivo)
        classificacoes.append(classificacao)
        
                
        
    #df.head()
    #dados = [textos,dispositivos,classificacoes]
    # Testar a existencia da pasta DsClassAnot e cria-la, caso nao exista
    dados = list(zip(textos,dispositivos,classificacoes))
    df = pd.DataFrame(dados, columns=['text','disp','label'])
    DsClassAnot = Dataset.from_pandas(df)
    DsClassAnot.save_to_disk(DS_FOLDER+"DsClassAnot/")  # Especificar a pasta DsClassAnot?

