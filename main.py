import openai
import time
import re
import API_KEYS

# API Key
openai.api_key = API_KEYS.KEY_TEIXEIRA

# Constants
REQUISITIONS_PER_DAY = 200
TOKEN_CREDITS_PER_MINUTE = 40000
REQUISITIONS_PER_MINUTE = 3

# Timers
minute_timer = 0
new_request_timer = 0

# Index
corpus_sentence_index = -1

# Output divergences list
output_divergences_list = []

def api_requisition(user_message):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Dada a seguinte sentença e seu respectivo ator responda apenas com o caracter (-1) se ela possui conotação negativa, (0) se for neutra ou (1) se for positiva"},
            {"role": "user", "content": user_message}
        ],
        max_tokens=1024,
        temperature=0.5
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

def minute_reset():
    global TOKEN_CREDITS_PER_MINUTE, REQUISITIONS_PER_MINUTE, minute_timer
    TOKEN_CREDITS_PER_MINUTE = 40000
    REQUISITIONS_PER_MINUTE = 3
    minute_timer = 0

def compute_requisition():
    global REQUISITIONS_PER_DAY, REQUISITIONS_PER_MINUTE
    REQUISITIONS_PER_DAY -= 1
    REQUISITIONS_PER_MINUTE -= 1

def add_requisition_credit():
    global REQUISITIONS_PER_DAY, new_request_timer
    REQUISITIONS_PER_DAY += 1
    new_request_timer = 0

def sentence_builder(tweet_dict):
    return f'sentença: "{tweet_dict["sentenca"]}", ator: {tweet_dict["ator"]}'

# Sample sentence corpus
sentence_corpus = [
    {
        "sentenca": "O candidato A é o melhor para o país!",
        "ator": "Candidato A",
        "conotacao_esperada": 1,
    },
    {
        "sentenca": "Não confio no político B, ele só faz promessas vazias.",
        "ator": "Político B",
        "conotacao_esperada": -1,
    },
    {
        "sentenca": "A reforma da previdência é um tópico importante.",
        "ator": "Reforma da previdência",
        "conotacao_esperada": 0,
    },
]

# Main loop
for sentence in sentence_corpus:
    if REQUISITIONS_PER_DAY < 1:
        print(f'Task done until index "{corpus_sentence_index}" of the corpus')
        break

    corpus_sentence_index += 1
    answer = api_requisition(sentence_builder(sentence))
    compute_requisition()
    
    print(time.strftime("Request Moment - %Y-%m-%d %H:%M:%S"))
    
    numeric_response = encontrar_valor_numerico(answer[0])
    print(f"GPT Output: {numeric_response}")
    
    tokens_used = int(answer[1].total_tokens)
    TOKEN_CREDITS_PER_MINUTE -= tokens_used
    
    print(f"Tokens Used: {tokens_used}")
    print(f"Avaluable Tokens: {TOKEN_CREDITS_PER_MINUTE}")
    print(f"Expected Output {sentence['conotacao_esperada']}")
    
    if int(sentence["conotacao_esperada"]) != numeric_response:
        output_divergences_list.append(
            {
                "sentenca": sentence["sentenca"],
                "ator": sentence["ator"],
                "gpt_output": numeric_response,
                "conotacao_esperada": sentence["conotacao_esperada"],
            }
        )
    
    print(f"===== Requisitions per day left: {REQUISITIONS_PER_DAY} =====")

    if corpus_sentence_index < len(sentence_corpus) - 1:
        time.sleep(20)  # Pause for 20 seconds except in the last iteration
    
    if minute_timer >= 60:
        minute_reset()
    elif new_request_timer >= 440:
        add_requisition_credit()
