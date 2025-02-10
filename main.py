from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode, tools_condition
import os
import json

# Carregamento de credenciais
with open('/mnt/c/Users/renan.cunha/OneDrive - ST IT Tecnologia e Serviços Ltda/Documentos/Renan/Desafio Tech Del/project_langchain_langgraph_chat/code/cred.json', 'r') as f:
    credentials = json.load(f)

os.environ["TAVILY_API_KEY"] = credentials["tavily"]
os.environ["HUGGINGFACEHUB_API_TOKEN"] = credentials["huggingface"]

# Inicializando API
app = FastAPI(title="Chatbot API", description="API para interagir com o chatbot baseado em Langchain e Langgraph.")

# Configuração dos templates
templates = Jinja2Templates(directory="/mnt/c/Users/renan.cunha/OneDrive - ST IT Tecnologia e Serviços Ltda/Documentos/Renan/Desafio Tech Del/project_langchain_langgraph_chat/code/templates")

# Modelo de entrada do usuário
class UserInput(BaseModel):
    message: str

# Configuração do modelo
system_prompt = """Você é um assistente artificial capaz de conversar sobre diversos assuntos, 
                    exceto Engenharia Civil. Se o usuário mencionar esse tema, informe que não pode ajudar."""

hf_endpoint = HuggingFaceEndpoint(
    repo_id="HuggingFaceH4/zephyr-7b-beta",
    task="text-generation",
    max_new_tokens=512,
    temperature=0.5
)

llm = ChatHuggingFace(llm=hf_endpoint)
search_tool = TavilySearchResults(max_results=10)
tools = [search_tool]
llm_with_tools = llm.bind_tools(tools)

graph_builder = StateGraph(dict)

# Função do agente conversacional
def chatbot_node(state: dict):
    messages = state["messages"]

    # Verificação explícita do conteúdo para evitar erros
    try:
        response = llm_with_tools.invoke(messages)
        
        # Verificando se a resposta está no formato esperado
        if hasattr(response, "content"):
            content = response.content
        elif isinstance(response, dict) and "content" in response:
            content = response["content"]
        else:
            content = "Desculpe, não entendi a resposta."

        return {"messages": messages + [{"role": "assistant", "content": content}]}
    
    except Exception as e:
        return {"messages": messages + [{"role": "assistant", "content": f"Erro: {e}"}]}

graph_builder.add_node("chatbot", chatbot_node)
tool_node = ToolNode(tools)
graph_builder.add_node("tools", tool_node)

graph_builder.set_entry_point("chatbot")

# Ajustando a condição para chamar o agente de busca
def custom_tools_condition(state):
    messages = state["messages"]
    last_message = messages[-1]["content"].lower()

    # Chamando o agente de busca apenas se houver necessidade
    if "pesquise" in last_message or "busque" in last_message:
        return True
    return False

graph_builder.add_conditional_edges(
    "chatbot",
    custom_tools_condition,
    {True: "tools", False: END}
)
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})

@app.post("/chat")
def chat(user_input: UserInput):
    try:
        conversation_history = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input.message},
        ]

        result = ""
        for event in graph.stream({"messages": conversation_history}):
            for node, data in event.items():
                if node == "chatbot" and "messages" in data:
                    result = data["messages"][-1]["content"]

        return {"response": result} if result else {"response": "Erro ao processar resposta."}


    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Execução segura
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
