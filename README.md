# <p align="center"> 🤖 Skynet
<p align="center">
<img loading="lazy" src="http://img.shields.io/static/v1?label=STATUS&message=%20FINALIZADO&color=GREEN&style=for-the-badge"/>
</p>

## ⚙️ Versão<a name="versao"></a>

Atualmente está disponível a **Versão 1.0** do presente projeto, disponibilizada em Setembro/2024.

## 📝 Descrição do Projeto:

Este projeto consiste no desenvolvimento de um chatbot inteligente capaz de recomendar filmes com base nas preferências do usuário.<br>
Como parte desse desafio, foi implementada uma API que converte textos em áudio utilizando o serviço AWS Polly. Posteriormente, o chatbot foi construído utilizando o Amazon Lex V2, o qual interage com a API para fornecer respostas por voz, criando uma experiência de recomendação de filmes mais dinâmica e interativa.<br> 
Para acessar nossa aplicação, clique aqui: [Skynet Chatbot - Slack Workspace](https://join.slack.com/t/grupo-1compass-uol/shared_invite/zt-2r8k4rgie-xyqya4tGwYMv0zRz318k8Q).

## 🎯 Especificações do Projeto:

O projeto é dividido em duas etapas principais:

##### Parte 1: API de Conversão de Texto em Áudio:

- O projeto começa com a criação de uma API usando o framework Serverless que permite ao usuário enviar uma frase de texto.
- Essa frase é transformada em áudio no formato MP3 utilizando o serviço AWS Polly.
- O áudio gerado é armazenado em um bucket S3 público, e as referências são salvas em uma tabela do DynamoDB.
- A API verifica se o áudio da frase já foi gerado anteriormente. Se sim, retorna o URL do áudio existente; caso contrário, gera o áudio, salva no S3 e registra no DynamoDB.

O deploy da API é realizado na AWS, com endpoints específicos para validação.

##### Parte 2: Criação do Chatbot:

- A segunda parte envolve a criação de um chatbot utilizando o Amazon Lex V2.
- O chatbot é projetado para interagir com o usuário e pode ser integrado a plataformas como Slack ou web.
- Ele captura frases, utiliza intents (intencionalidades), slots (dados extraídos do usuário), e lida com falhas de compreensão de forma robusta.
- Opcionalmente, o chatbot pode retornar respostas em áudio usando a API de conversão criada na primeira parte.



## ⚙️ Tecnologias Utilizadas:
<p align="center">
  <a href="https://go-skill-icons.vercel.app/">
    <img src="https://go-skill-icons.vercel.app/api/icons?i=vscode,python,aws,dynamodb,git,github,mysql,slack,postman" />
  </a>
</p>

  - **VSCode**:IDE escolhida para escrever, editar e depurar o código do projeto.
  - **Python**: Linguagem de programação utilizada.
  - **Serverless/Lambda**: O projeto foi desenvolvido com o framework Serverless. O Lambda permite rodar o código sem a necessidade de gerenciar servidores.
  - **AWS Cloud**: A AWS fornece os serviços de computação, armazenamento, processamento de áudio e interação de chatbot, integrando-os em uma solução completa que facilita a implementação da API e do chatbot com escalabilidade e sem a necessidade de gerenciar infraestrutura física.
  - **AWS Polly**: Responsável por converter o texto inserido pelo usuário em áudio (MP3). Polly é um serviço de síntese de fala que gera o áudio com base na frase fornecida.
  - **Amazon S3**: Utilizado para armazenar os arquivos de áudio gerados pela AWS Polly. O S3 atua como um repositório onde os áudios são salvos e disponibilizados para acesso via URL.
  - **Amazon DynamoDB**: Um banco de dados NoSQL usado para armazenar as referências dos áudios gerados, como o hash único da frase e o link do áudio. Isso permite verificar se um áudio já foi criado anteriormente.
  - **Amazon Lex V2**: Serviço utilizado para criar o chatbot que interage com o usuário. Lex processa a entrada de texto do usuário, reconhece intenções, e pode retornar respostas em texto ou áudio.
  - **AWS IAM (Identity and Access Management)**: Gerencia as credenciais e permissões de acesso aos serviços AWS utilizados, garantindo que os componentes da aplicação possam interagir de forma segura.
  - **Git e Github**: Para versionamento da aplicação.
  - **MySQL**: Sistema de gerenciamento de banco de dados relacional utilizado para armazenar e gerenciar os dados do projeto.
  - **Slack**: No projeto, o Slack atua como a plataforma de mensageria que conecta o chatbot criado com Amazon Lex V2 aos usuários.
  - **Postman**: Para testar as rotas e funcionamento da aplicação.

## 🛠 Como Abrir e Executar Esse Projeto:

**1. Clone o repositório**:

```
git clone --branch grupo-6 https://github.com/Compass-pb-aws-2024-JUNHO/sprints-6-7-pb-aws-junho.git
```
**2. Abra o repositório clonado em uma IDE de sua escolha, neste projeto a IDE utilizada foi o Visual Studio Code (VSCode)**:

**3. Recomendamos o uso de um ambiente virtual para que não aja conflito de versões, nesse projeto utilizamos um módulo nativo da própria linguagem Python, o Virtual Enviroment (venv), para sua instalação, abra o terminal do VSCode dentro da pasta raiz do projeto**:
```
python -m venv venv

.\venv\Scritps\activate

```
**4. Para saber se o acesso ao ambiente virtual foi bem sucedido, o prefixo venv deverá estar presente no caminho do projeto do seu terminal, exemplo**: 
```
(venv) PS C:\Users\usuário\sprints-6-7-pb-aws-junho>
```
**5. No terminal, instale o framework Serverless através do comando**:
```
npm install -g serverless
```
**6. Após a instalação do framework do projeto, configure suas credenciais AWS**:

##### Opção 1 - Via AWS CLI (Opção que recomendamos):

Instale a AWS CLI e configure suas credenciais com:

```
aws configure
```
Você será solicitado a fornecer:

- AWS Access Key ID: Sua chave de acesso.<br>
- AWS Secret Access Key: Sua chave secreta.<br>
- Default region name: Por exemplo, us-east-1 (Escolha a região que você está utilizando).<br>
- Default output format: Pode ser json.

##### Opção 2 - Via Serverless Framework:

Outra forma de configurar as credenciais é diretamente pelo Serverless:

```
serverless config credentials --provider aws --key <AWS_ACCESS_KEY> --secret <AWS_SECRET_KEY>
```
##### Substitua AWS_ACCESS_KEY e AWS_SECRET_KEY pelas suas credenciais da AWS.


**7. Instale as dependências**:
```
npm install
# ou
pip install -r requirements.txt: 
```
**8. Faça o deploy da aplicação no Serverless Framework**:

Agora que tudo está configurado, faça o deploy da aplicação para a AWS. Navegue até o diretório do projeto (onde está o arquivo serverless.yml):

```
serverless deploy
```

##### Esse comando irá:

- Criar funções Lambda.<br>
- Configurar o API Gateway.<br>
- Configurar outras integrações AWS necessárias.


**9. Verifique os endpoints gerados. Esses endpoints são URLs para as funções Lambda. Use-os para fazer requisições à API, seja via navegador, Postman, ou outra ferramenta**:

endpoints:
```
  GET - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/hello
  POST - https://xxxxxxxxxx.execute-api.us-east-1.amazonaws.com/dev/tts
```
**10. Teste a API localmente**:

```
serverless invoke local --function v1Description
```

## 🌐  🤖 Testando o Chatbot no Slack:

Para interagir com o chatbot desenvolvido neste projeto, siga as etapas abaixo:

1. **Acesse o Slack**:

Certifique-se de ter uma conta no Slack. Caso não tenha, você pode criar uma em slack.com.<br>

2. **Conecte-se ao Workspace**:

O chatbot está implementado no workspace "Grupo-1 Compass-UOL". Se você ainda não faz parte deste workspace, precisará ser convidado para ter acesso. O convite para acessar nosso workspace está na seção "**Descrição do Projeto**", no início dessa documentação. Basta acessá-lo por lá.<br>

3. **Acesse o Canal do Chatbot**:

Atualmente, o chatbot está disponível no workspace Grupo-1 Compass-UOL e pode ser acessado diretamente na aba "Apps".<br>
![ambiente_slack](https://github.com/user-attachments/assets/60496325-43e6-455d-9035-c71b58a6ef11)


4. **Inicie uma Conversa**:

No canal ou diretamente na aba do app, você pode começar uma conversa digitando um comando ou uma frase que o bot reconheça. Por exemplo, você pode digitar `@SkynetBot [sua frase]` para interagir com o bot.

Exemplos de como interagir com nosso chatbot:

- @SkynetBot Me dê uma recomendação de filme.<br>
- Me indique um filme dos anos 2000.<br>
- Sugira um filme de terror.<br>
- Eu gostaria de ver um filme dos EUA.
- Quero assistir a um filme longo.
![interação_chatbot_referencia](https://github.com/user-attachments/assets/405df4b0-9c56-40b7-b8b8-bd07ea568543)


## 📂  Estrutura do Projeto:

### Estrutura de Diretórios:

A estrutura do projeto é organizada da seguinte maneira:

```
sprints-6-7-pb-aws-junho/
│
├── api_tts/                               # Diretório principal da API TTS
│   ├── handler.py                         # Função Lambda da API TTS - Text To Speech
│   ├── serverless.yml                     # Configuração do Serverless Framework
│   ├── README.md                          # Documentação do projeto API TTS
│   └── gitignore.txt                      # Arquivos e pastas ignoradas pelo Git
│
├── assets/                                # Recursos do projeto
│   ├── Banco de Dados/                    # Base de dados utilizada
│   │   └── filmes.csv                     # Base de dados para sugestões do chatbot
│   │
│   ├── Botsdeteste/                       # Chatbots utilizados para testes
│   │   └── ...                            # Chatbots de teste .zip
│   │
│   ├── Docs/                              # Documentos relacionados ao projeto
│   │   └── Skynet Bot - Fluxograma da interação final.pdf  # Fluxograma da interação
│   │
│   └── Images/                            # Recursos visuais ou arquivos estáticos
│   │   └── skynet_chatbot.jpg             # Imagem oficial do chatbot no Slack
│   └── sprints6-7.jpg                     # Imagem ou arquivo da Sprint 6-7
│
├── lexv2/                                 # Recursos do Lex V2
│   └── Bot/                               # Recursos do chatbot
│       └── ...                            # Modelo oficial do chatbot .zip
│   └── Lambda/                            # Diretório da lambda oficial
│        └── ...                           # Função lambda.zip
│        └── lambda_function.py            # Função lambda.py
│
└── README.md                              # Documentação do projeto Skynet - Chatbot (geral)
```

## 😵‍💫 Dificuldades Encontradas:

- **Compreensão da Estrutura da Lambda**: Dificuldades em entender como funciona a estrutura de uma função Lambda.
- **Orquestração de Microserviços**: Desafios em orquestrar os microserviços para que se comuniquem entre si, especialmente com serviços como Polly, S3, DynamoDB e Lex V2.
- **Gerenciamento do Tempo de Aprendizado**: Dificuldades em consumir todo o conteúdo da trilha de aprendizado disponibilizada dentro do tempo adequado.
- **Assimilação do Fluxograma de Interações**: Certas dificuldades em entender o fluxograma de interações do usuário com o chatbot.
- **Configuração do Ambiente de Desenvolvimento**: Desafios na configuração do ambiente de desenvolvimento, incluindo a instalação de dependências e a configuração das credenciais AWS.
- **Testes de Integração**: Dificuldades em realizar testes de integração entre os diferentes serviços da AWS e o chatbot, garantindo que todas as partes funcionem em conjunto.

## Licença:
Este projeto está licenciado sob a [MIT License](LICENSE).



## 🌐 Equipe:
🧑 💻 Este projeto foi desenvolvido por:
| [<img loading="lazy" src="https://avatars.githubusercontent.com/u/25685390?v=4" width=115><br><sub>John Sousa</sub>](https://github.com/johnSousa23) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/173844663?v=4" width=115><br><sub>Moniza Oliveira</sub>](https://github.com/MONIZA-OLIVEIRA) |  [<img loading="lazy" src="https://avatars.githubusercontent.com/u/101699095?v=4" width=115><br><sub>Nathalia de Oliveira Santos dos Reis</sub>](https://github.com/NathaliaOSReis)  |
| :---: | :---: | :---: |
