    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse
    from modal_image import image, stub
    from modal import asgi_app

    from langchain_cohere import ChatCohere
    from langchain_community.retrievers import CohereRagRetriever
    from langchain_core.documents import Document


    from langchain import hub
    from langchain_community.document_loaders import WebBaseLoader
    from langchain_community.vectorstores import Chroma
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    web_app = FastAPI()

    @web_app.post("/foo")
    async def foo(request: Request):
        body = await request.json()
        return body


    @web_app.get("/bar")
    async def bar(arg="world"):
        return HTMLResponse(f"<h1>Hello Fast {arg}!</h1>")


    @stub.function(image=image)
    @asgi_app()
    def fastapi_app():
        llm = ChatCohere()
        print('AG: llm init')
        # print("AG::", len(module_texts))
        # print("AG::", module_texts.keys())

        loader = DirectoryLoader(files_dir, glob="**/*.txt", loader_cls=TextLoader)
        docs = loader.load()
        #print(docs)
        print('AG: loaded docs')

        #pdb.set_trace()

        prompt = hub.pull("rlm/rag-prompt")
        #print(prompt)
        #print(type(prompt))
        # print(f'AG prompt::{prompt}')
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        print('AG: split text')
        splits = text_splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(documents=splits, embedding=OpenAIEmbeddings())
        print('AG: vector stroe created')
        retriever = vectorstore.as_retriever()
        print('AG: retriever created')

        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)

        rag_chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        return web_app