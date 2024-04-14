from modal import Image, Stub, Secret

image = Image.debian_slim(python_version="3.10").pip_install(
    "modal==0.62.21",
     "nomic",
     "cohere",
     "fastapi",
     "langchain",
    "langchain-cohere",
    "langchain-community==0.0.29",
    "langchain-openai",
    "langchain-core",
    "langchain-text-splitters",
     ).apt_install("git", "curl")

stub = Stub(
    name="ThinkWell",
    image=image,
    #secrets=[Secret.from_name("nomic-key")],
)