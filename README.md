# Chatbot com Langchain e Langgraph

Este repositório apresenta um chatbot desenvolvido utilizando as bibliotecas **Langchain** e **Langgraph**, projetado para interagir com os usuários sobre diversos assuntos, com exceção de **Engenharia Civil**. Caso o usuário tente abordar esse tema, o chatbot responderá educadamente que não pode fornecer informações.

## Objetivo do Projeto

O objetivo deste projeto é criar um assistente virtual capaz de interagir de forma natural com o usuário, aproveitando um modelo de linguagem baseado na API da **Hugging Face**. Além disso, o chatbot pode utilizar ferramentas auxiliares para complementar suas respostas, como mecanismos de busca.

## Principais Tecnologias Utilizadas

- **Langchain**: Framework para a criação de agentes conversacionais baseados em LLMs.
- **Langgraph**: Biblioteca para a construção de fluxos conversacionais estruturados.
- **Hugging Face API**: Utilização do modelo **zephyr-7b-beta** para geração de respostas.
- **Tavily Search API**: Ferramenta de busca para complementar respostas do chatbot.

## Funcionamento do Script

1. **Inicialização do modelo de linguagem**: O script configura um modelo de linguagem da **Hugging Face** para processar mensagens e gerar respostas.
2. **Configuração das ferramentas**: O chatbot pode utilizar a API de busca para fornecer informações adicionais quando necessário.
3. **Fluxo de interação**: O Langgraph é utilizado para definir a lógica do chatbot, garantindo que ele possa interagir com o usuário e chamar ferramentas quando apropriado.
4. **Filtro de conteúdo**: Qualquer menção a **Engenharia Civil** é identificada e tratada com uma resposta apropriada informando que o chatbot não pode ajudar sobre esse tema.

## Como Executar

Para rodar o chatbot localmente:

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-repositorio/chatbot-langchain.git
   ```
2. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o script principal:
   ```bash
   python main.py
   ```
4. Interaja com o chatbot diretamente no terminal.

## Melhorias Futuras

- Ajustes no tratamento de mensagens para garantir respostas mais precisas.
- Expansão das ferramentas utilizadas para melhorar a qualidade das respostas.
- Implementação de uma interface web para facilitar o uso do chatbot.

Este projeto está em evolução e sugestões são bem-vindas!

