# Dado o Dataset, tomar um registro e tentar encontrar com regex a classificacao dele e a secao DISPOSITIVO
# Estrutura (Features): (id | text | disp | classif)

import re

#texto  = ds['train']['text'][0]
tam_tokeniz = 1024


padraoImproc = "improcedentes|improcedente"
padraoParcProc = "procedentes em parte|procedente em parte|parcialmente procedentes|parcialmente procedente|parcialmente improcedentes|parcialmente improcedente"
padraoProc = "procedentes|procedente"
padraoOutros = "DISPOSITIVO"

def extraiDispositivo(pattern, text):
    padrao = pattern
    
    for match in re.finditer(pattern, text):
        index = match.start()
        value = match.group()
        print(index, value)

        span = (tam_tokeniz - len(padrao))/2
        texto_inicio = int(match.start() - span)
        texto_fim    = int(match.start() + len(padrao) + span)
        if(texto_fim > len(text)): # nao pode ser maior que o tamanho da string
            texto_fim = len(text)
        
        #print(texto_inicio, texto_fim)
        #print(index)

    return(text[texto_inicio:texto_fim])

def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)    
    
def classDispositivo(examples):
    texto = examples['text']
    
    for i in range(len(texto)):
    
        if((len(t = extraiDispositivo(padraoImproc, texto[i])) != 0)):
            dispositivo   = t
            classificacao = "Improcedente"
            #break
        else:       
            if((len(t = extraiDispositivo(padraoParProc, texto[i])) != 0)):
                dispositivo   = t
                classificacao = "Parcialmente procedente"
                #break
            else: 
                if((len(t = extraiDispositivo(padraoProc, texto[i])) != 0)):
                    dispositivo   = t
                    classificacao = "Procedente"
                    #break
                else:
                    dispositivo = extraiDispositivo(padraoOutros, texto[i])
                    classificacao = "Acordo ou outros"

        examples['disp'][i]    = dispositivo
        examples['classif'][i] = classificacao


                        
