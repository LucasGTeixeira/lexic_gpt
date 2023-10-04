## Como Rodar
Para executar este script, você precisará atender a alguns requisitos prévios.
### Python 3.71 ou superior (requisito para a biblioteca openai)
Para verificar se você tem o Python instalado e conferir a versão, abra seu terminal e digite o seguinte comando:
```bash
$ python --version
```
Se você não tiver o Python instalado ou precisar atualizar para uma versão mais recente, siga estas etapas:

**Atualizando o Python** (apenas se necessário)
Baixe o Python: Vá para o site oficial do Python em python.org e baixe a versão mais recente adequada ao seu sistema operacional.

**Instale o Python**: Execute o instalador baixado e siga as instruções para instalar o Python. Certifique-se de marcar a opção "Adicionar Python ao PATH" durante a instalação.

Após a instalação, verifique novamente a versão do Python para garantir que a instalação tenha sido bem-sucedida

### Python pip
O pip é o gerenciador de pacotes do Python e geralmente é instalado junto com o Python. No entanto, você pode verificar sua presença executando o seguinte comando:

**Linux**
```bash
pip --version
```

**Windows**
```bash
python -m pip --version
```

Se o pip não estiver instalado ou se você precisar atualizá-lo, siga estas etapas:

#### Instalando ou Atualizando o pip (caso necessário)
Caso esteja utilizando um sistema operacional linux:
```bash
sudo apt-get update  # Atualiza a lista de pacotes (apenas para sistemas baseados em Debian/Ubuntu)
sudo apt-get install python-pip  # Instala o pip
```
Caso esteja utilizando windows leia a [documentação do pip](https://pip.pypa.io/en/stable/installation/)

### Biblioteca openai
Para realizarmos as operações de requisições com mais recursos usaremos a biblioteca da openai, para isso é necessário instalar ela pelo pip
```bash
pip install openai
```
## Limitações da ferramenta OpenAI API

Infelizmente, a API do OpenAI possui diversos limites de requisição, sendo eles:

- 3 requisições por minuto
- 40.000 tokens por minuto
- 200 requisições por dia

Além disso, para acessar a API é necessário possuir uma `api_key` gerada pela plataforma da OpenAI. Você pode obter sua chave [aqui](https://platform.openai.com/account/api-keys), tornando o acesso à ferramenta possível.

## Coisas que a Documentação não Menciona

- A geração de créditos de requisições por dia (RPD) não é limitada pelo dia, mas sim pelas horas. A cada 7 minutos e 12 segundos, você ganha uma requisição adicional, permitindo acumular até o máximo absoluto de 200 requisições em um período de 24 horas.

- As chaves de API são apenas um método de controle de acesso. Seu crédito de API está diretamente associado à sua conta, que pode possuir mais de uma chave.

## Descrição do Método ChatCompletion.create

O método `ChatCompletion.create` é uma função que permite a interação com o modelo GPT-3.5 da OpenAI para gerar respostas com base em solicitações de texto. Este método segue um processo de decomposição de uma requisição POST, que pode ser resumido nos seguintes passos:

1. **Escolha do Modelo**: Você deve selecionar o modelo que será usado para a requisição. O modelo escolhido terá um impacto direto na natureza das respostas geradas.

2. **Criação da Mensagem**: Para iniciar a interação com o modelo, você precisa criar uma mensagem. Existem vários papéis (roles) disponíveis, sendo os principais o "system" e o "user". O "system" é usado para definir um contexto global que influenciará o comportamento textual do modelo, enquanto o "user" funciona como a entrada principal, representando a mensagem ou pergunta do usuário.

    2.1. **Role "system"**: Define um parâmetro de contexto global que afeta o comportamento do modelo.
    
    2.2. **Role "user"**: Funciona como a entrada do usuário, especificando a mensagem ou pergunta a ser respondida pelo modelo.

3. **Limite de Tokens da Resposta**: É possível determinar o número máximo de tokens que a resposta gerada pelo modelo pode conter. Isso ajuda a controlar o tamanho da resposta e a economizar custos.

4. **Temperatura do Modelo**: A temperatura é um parâmetro que afeta a criatividade das respostas geradas pelo modelo. Ela varia de 0 a 1 e pode ser ajustada da seguinte maneira:

   - Baixa temperatura (0 a 0,3): Produz saídas mais focadas, coerentes e conservadoras.
   - Temperatura média (0,3 a 0,7): Equilibra criatividade e coerência.
   - Alta temperatura (0,7 a 1): Gera respostas altamente criativas e diversas, mas potencialmente menos coerentes.

Para obter informações detalhadas sobre como utilizar esse método, consulte a documentação da [biblioteca OpenAI](https://github.com/openai/openai-python).
