import openai
import time
import re
import API_KEYS
import pandas as pd


# API Key
openai.api_key = API_KEYS.KEY_TEIXEIRA

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
df = pd.read_excel('./inputs/entradas.xlsx')
df = df[CORPUS_STOP_INDEX:]

def setup_corpus(df, sentence_corpus):
    global index
    for index, row in df.iterrows():
        sentence = {
            "sentence": row['FRASE'],
            "alvo_esperado": row['ALVOS'],
        }
        sentence_corpus.append(sentence)

def api_requisition(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Dada a seguinte sentença, responda no formato ['alvo1'] o(s) alvo(s) de opinião presente(s) na sentença."},
            {"role": "user", "content": user_message}
        ],
        max_tokens=1024,
        temperature=0,
        request_timeout=15
    )
    return [response.choices[0].message.content, response.usage]

def sentence_builder(tweet_dict):
    return f'sentença: "{tweet_dict["sentence"]}"'

# Main loop
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
            df_gpt.to_excel('./outputs/target_output.xlsx', index=False)
            print(f"Requisition Time Out Exception, YOU STOP AT INDEX {CORPUS_SENTENCE_INDEX}")
            print(f"TRYING AGAIN")
            time.sleep(3)
    
    print(time.strftime("Request Moment - %Y-%m-%d %H:%M:%S"))
    print(f"GPT Output: {answer[0]}")
    tokens_used = int(answer[1].total_tokens)
    print(f"Tokens Used: {tokens_used}")
    print("=======================")

    #Adiciono na lista
    output_sentence_corpus.append(
        {
            "FRASE": sentence["sentence"],
            "ALVO_ESPERADO": sentence["alvo_esperado"],
            "GPT_RESPONSE": answer[0]
        }
    )

    df_gpt = pd.DataFrame(output_sentence_corpus)

df_gpt.to_excel('./outputs/target_output.xlsx', index=False)