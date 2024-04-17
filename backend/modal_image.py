from modal import Image, Stub, Secret

#image = Image.debian_slim(python_version="3.10.14").pip_install(
image = Image.debian_slim(python_version="3.11").pip_install(
    "modal==0.62.63",
     "nomic",
     "cohere",
     "fastapi",
     "langchain==0.1.14",
    "langchain-cohere",
    #"langchain-nomic",
    "langchain-community==0.0.31",
    "langchain-openai",
    "langchain-core==0.1.40",
    "langchain-text-splitters==0.0.1",
    "chromadb",
    "faiss-cpu",
    "tiktoken",
    "langchain_google_vertexai",
    "google-cloud-bigquery", 
    "pymongo",
     ).apt_install("git", "curl")

stub = Stub(
    name="ThinkWell",
    image=image,
    #secrets=[Secret.from_name("nomic-key")],
)