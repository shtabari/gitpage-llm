from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage
from langchain.memory import ChatMessageHistory
from langchain_core.output_parsers import StrOutputParser

from langchain_community.document_loaders import GCSFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough




chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.5)


def llm_response(question,chat_hist):
    demo_ephemeral_chat_history = ChatMessageHistory()
    if len(chat_hist) != 0:
        for message in chat_hist:
            # print(message['props']['children'][0]['props']['children'],message['props']['children'][1]['props']['children'])
            user_prev = message['props']['children'][0]['props']['children']

            bot_prev = message['props']['children'][1]['props']['children']
            if user_prev.lower()[:3] == "you":
                demo_ephemeral_chat_history.add_user_message(user_prev[4:])
            if bot_prev.lower()[:3] == "bot":
                demo_ephemeral_chat_history.add_ai_message(bot_prev[4:])


        
    # prompt = ChatPromptTemplate.from_messages(
    # [
    #     (
    #         "system",
    #         "You are a helpful assistant. Answer all questions in details and informative.",
    #     ),
    #     MessagesPlaceholder(variable_name="messages"),
    # ]
    # )

    # chain = prompt | chat | StrOutputParser()

    # demo_ephemeral_chat_history.add_user_message(user_message)

    # resp = chain.invoke({"messages": demo_ephemeral_chat_history.messages})

    # return resp.content


    loader = GCSFileLoader(project_name="github-page", bucket="port-llm", blob="rag_data.txt")

    data = loader.load()


    text_splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=0)
    all_splits = text_splitter.split_documents(data)

    vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(k=4)


    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.5)

    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )
    contextualize_q_chain = contextualize_q_prompt | llm | StrOutputParser()

    qa_system_prompt = """You serve as an accommodating Customer Support Chatbot, ensuring customer contentment by addressing their inquiries. 
    Your role is to paraphrase the following context and assist customers with subsequent actions. 
    Provide price matching or discounts to maintain customer satisfaction and loyalty.

    <context>
    {context}
    </context>
    """
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}"),
        ]
    )


    def contextualized_question(input: dict):
        if input.get("chat_history"):
            return contextualize_q_chain
        else:
            return input["question"]


    rag_chain = (
        RunnablePassthrough.assign(
            context=contextualized_question | retriever | format_docs
        )
        | qa_prompt
        | llm
    )

    resp = rag_chain.invoke({"question": question, "chat_history": demo_ephemeral_chat_history.messages})
    return resp.content
