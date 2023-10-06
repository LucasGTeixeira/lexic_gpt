import openai
import time
import re
import scripts.API_KEYS as API_KEYS
import pandas as pd

# API Key
openai.api_key = API_KEYS.KEY_TEIXEIRA

# Constants
TOKEN_CREDITS_PER_MINUTE = 90000
REQUISITIONS_PER_MINUTE = 3500

# Counters
MINUTE_TIMER = 0
REQUISITION_COUNTER = 0

# Index
CORPUS_STOP_INDEX = 0
CORPUS_SENTENCE_INDEX = CORPUS_STOP_INDEX-1

# Initializing corpusList
sentence_corpus = []
output_sentence_corpus = []

#Lendo o corpus original
df = pd.read_excel('nci_outputs.xlsx')
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
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Dada a sentença $<$sentença$>$ e o alvo sendo $<$alvo$>$ qual a polaridade associada a ele, negativa (-1), positiva (1) ou neutra (0)?'"},
            {"role": "user", "content": user_message}
        ],
        max_tokens=1024,
        temperature=0.5,
        request_timeout=30
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
    return f'$<$sentença$>$: "{tweet_dict["sentence"]}", $<$alvo$>$: {tweet_dict["target"]}'

# Configuring sentences and target dict

# Main loop
setup_corpus(df, sentence_corpus)

#Caso ocorra algum problema
# sentence_corpus = sentence_corpus[stop_index:]
for sentence in sentence_corpus:
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
            print(f"Requisition Time Out Exception, YOU STOP AT INDEX {CORPUS_SENTENCE_INDEX}")
            print(f"TRYING AGAIN")
            time.sleep(2)
    
    print(time.strftime("Request Moment - %Y-%m-%d %H:%M:%S"))
    
    numeric_response = encontrar_valor_numerico(answer[0])
    print(f"GPT Numeric Output: {numeric_response}")
    print(f"GPT Text Output: {answer[0]}")
    
    tokens_used = int(answer[1].total_tokens)
    
    print(f"Tokens Used: {tokens_used}")

    #Adiciono na lista
    output_sentence_corpus.append(
        {
            "FRASE": sentence["sentence"],
            "ALVO": sentence["target"],
            "POLARIDADE_GPT": numeric_response,
            "TEXT_GPT": answer[0], 
        }
    )

    df_gpt = pd.DataFrame(output_sentence_corpus)

df_gpt.to_excel('nci_final.xlsx', index=False)