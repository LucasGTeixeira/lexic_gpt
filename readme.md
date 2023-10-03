## O método ChatCompletion.create funciona como uma decomposição de uma requisição POST.
1- Escolhe o modelo que fará a requisição
2- Cria uma variável de mensagem
2.1- Existem vários roles diferentes, dentre eles, usaremos o role "system" que determina um parâmetro de contexto, que dita o comportamento textual do modelo e também usaremos o role "user" que funciona exatamente como o input do chatGPT web
3- Determina um numero máximo de tokens da resposta
4- Determina a "temperatura" do modelo (quanto mais próximo de 0 mais objetivo ele é)
    - Low temperature (0 to 0.3): More focused, coherent, and conservative outputs.
    - Medium temperature (0.3 to 0.7): Balanced creativity and coherence.
    - High temperature (0.7 to 1): Highly creative and diverse, but potentially less coherent.
(tirado da documentação da biblioteca openai)