import openai
import time
import re
import pandas as pd
import os
import sys

utils_path = os.path.join(os.path.dirname(__file__), '..', 'utils')
sys.path.append(utils_path)

from utils.API_KEYS import KEY_TEIXEIRA

# API Key
openai.api_key = KEY_TEIXEIRA
# Counters
MINUTE_TIMER = 0
REQUISITION_COUNTER = 0

# Index (Caso de algum problema no processamento do corpus, use essa variável para colocar 
# o último índice que apareceu no terminal)
CORPUS_STOP_INDEX = 0
CORPUS_SENTENCE_INDEX = CORPUS_STOP_INDEX-1

# Initializing corpusList
sentence_corpus = []
output_sentence_corpus = []

#Lendo o corpus original
df = pd.read_excel('./inputs/polarity_entradas.xlsx')
df = df[CORPUS_STOP_INDEX:]

def setup_corpus(df, sentence_corpus):
    global index
    for index, row in df.iterrows():
        sentence = {
            "sentence": row['FRASE'],
            "target": row['ALVOS'],
        }
        sentence_corpus.append(sentence)

def api_requisition(user_message):
    prompt = "Dada uma sentença e seus respectivos marcadores sobre o mesmo alvo de opinião responda apenas com o caracter (-1) se ela possui conotação negativa, (0) se for neutra ou (1) se for positiva"
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_message}
        ],
        max_tokens=1024,
        temperature=0,
        request_timeout=15
    )
    return [response.choices[0].message.content, response.usage]

def encontrar_valor_numerico(texto):
    try:
        match = re.search(r'(-?1|0|1)', texto)

        if match:
            valor_numerico = match.group(0)
            return int(valor_numerico)
        else:
            return None
    except Exception as e:
        raise Exception("Não foi possível determinar o valor numérico pelo Output do GPT")

def sentence_builder(tweet_dict):
    return f'sentença: "{tweet_dict["sentence"]}", marcadores: {tweet_dict["target"]}'

setup_corpus(df, sentence_corpus)

for sentence in sentence_corpus:
    time.sleep(1)
    print("=======================")

    CORPUS_SENTENCE_INDEX += 1
    print(f'Dict Current Index: {CORPUS_SENTENCE_INDEX}')

    request_200 = False
    while request_200 == False:
        try:
            answer = api_requisition(sentence_builder(sentence))
            request_200 = True
        except:
            df_gpt = pd.DataFrame(output_sentence_corpus)
            df_gpt.to_excel('./outputs/polarity_output.xlsx', index=False)
            print(f"Requisition Time Out Exception, YOU STOP AT INDEX {CORPUS_SENTENCE_INDEX}")
            print(f"TRYING AGAIN")
            time.sleep(3)
    
    print(time.strftime("Request Moment - %Y-%m-%d %H:%M:%S"))
    
    numeric_response = encontrar_valor_numerico(answer[0])
    print(f"GPT Output: {answer[0]}")
    print(f"Numeric Output: {numeric_response}")
    
    tokens_used = int(answer[1].total_tokens)
    
    print(f"Tokens Used: {tokens_used}")
    print("=======================")

    #Adiciono na lista
    output_sentence_corpus.append(
        {
            "FRASE": sentence["sentence"],
            "ALVO": sentence["target"],
            "NUMERIC_RESPONSE": numeric_response,
            "GPT_RESPONSE": answer[0]
        }
    )

    df_gpt = pd.DataFrame(output_sentence_corpus)

df_gpt.to_excel('./outputs/polarity_output.xlsx', index=False)