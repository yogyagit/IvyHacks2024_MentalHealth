from modal_image import image, stub, volume
from modal import asgi_app, Image, Stub, method, enter, Secret

@stub.cls(image=image, gpu="T4", container_idle_timeout=300,
          secrets=[Secret.from_name("thinkwell-key")], volumes={'/data': volume},)
class RagChain:
    @enter()
    def enter(self):
        from langchain_community.retrievers import CohereRagRetriever
        from langchain_core.documents import Document
        from langchain_openai import OpenAIEmbeddings
        from langchain_community.document_loaders import DirectoryLoader
        from langchain_community.document_loaders import TextLoader
        from langchain_cohere import CohereEmbeddings

        from langchain import hub
        from langchain_community.document_loaders import WebBaseLoader
        from langchain_community.vectorstores import Chroma
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.runnables import RunnablePassthrough
        from langchain_text_splitters import RecursiveCharacterTextSplitter
        from langchain_community.vectorstores import FAISS
        print("Inside start..1")
        self.files_dir = "/data/data"
        self.loader = DirectoryLoader(self.files_dir, glob="**/*.txt", loader_cls=TextLoader)
        print("Inside start..2")
        self.docs = self.loader.load()
        print("Inside start..3..")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        print("Inside start..4")
        self.splits = text_splitter.split_documents(self.docs)
        print("Inside start..5")
        #self.vectorstore = Chroma.from_documents(documents=self.splits, embedding=OpenAIEmbeddings())
        self.vectorstore = FAISS.from_documents(documents=self.splits, embedding= CohereEmbeddings(model="embed-english-light-v3.0"))
        #self.vectorstore = Chroma.from_documents(documents=self.splits, embedding= CohereEmbeddings(model="embed-english-light-v3.0"))
        self.retriever = self.vectorstore.as_retriever(search_type="similarity_search", search_kwargs={'k': 4})
        #self.llm = CohereChatbot()
        #print('chatbot created inside ragchain')
         

    @method()
    #def invoke(self, question, prompt , llm, chat_history):
    def invoke(self, question, prompt):
    #def invoke(self, question):
        print("Inside invoke")
        #relevant_docs = self.retriever.search(question, k=5)
        #relevant_docs = self.vectorstore.similarity_search(question)
        relevant_docs = self.vectorstore.max_marginal_relevance_search(question)
        #formatted_docs = "\n\n".join([doc.content for doc in relevant_docs])
        formatted_docs = "\n\n".join([doc.page_content for doc in relevant_docs])
        full_prompt = prompt.format(context=formatted_docs, question=question)
        #full_prompt = prompt.format(question=question)
        #response = llm.chat.remote(message=full_prompt, chat_history=chat_history)

        """
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        rag_chain = (
            {"context": self.retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )
        return rag_chain.invoke({"question": question})
        """

        #return response
        return full_prompt