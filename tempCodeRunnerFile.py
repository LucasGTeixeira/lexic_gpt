for sentence in sentence_corpus:
#     if TOKEN_CREDITS_PER_MINUTE <= 500: 
#         print(f'Task done until index "{CORPUS_SENTENCE_INDEX}" of the corpus')
#         raise Exception("Token limit Reached")

#     CORPUS_SENTENCE_INDEX += 1
#     answer = api_requisition(sentence_builder(sentence))
#     compute_requisition()
    
#     print(time.strftime("Request Moment - %Y-%m-%d %H:%M:%S"))
    
#     numeric_response = encontrar_valor_numerico(answer[0])
#     print(f"GPT Output: {numeric_response}")
    
#     tokens_used = int(answer[1].total_tokens)
#     TOKEN_CREDITS_PER_MINUTE -= tokens_used
    
#     print(f"Tokens Used: {tokens_used}")
#     print(f"Avaluable Tokens: {TOKEN_CREDITS_PER_MINUTE}")
#     print("=======================")

#     #Adiciono na lista
#     output_sentence_corpus.append(
#         {
#             "FRASE": sentence["sentence"],
#             "ALVO": sentence["target"],
#             "CONOTACAO_GPT": numeric_response,
#         }
#     )


# df = pd.DataFrame(output_sentence_corpus)

# print(df.head())
# df.to_excel('gpt_output.xlsx', index=False)