from modal import Image, Stub, Secret, Volume

volume = Volume.from_name("my-data-volume", create_if_missing=True)

huggingface_model_registry = {
    "cohere": "CohereForAI/c4ai-command-r-v01",
    #"cohere": "CohereForAI/c4ai-command-r-v01-4bit",
}
def download_model_bnb():
    from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

    # download all models
    for _, model in huggingface_model_registry.items(): 
        bnb_config = BitsAndBytesConfig(load_in_8bit=True)
        model_id = "CohereForAI/c4ai-command-r-v01"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForCausalLM.from_pretrained(model_id, quantization_config=bnb_config)

def download_model():
    # pip install 'transformers>=4.39.1'
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from transformers.utils import move_cache

    # download all models
    for _, model in huggingface_model_registry.items(): 
        tokenizer = AutoTokenizer.from_pretrained(model)
        model = AutoModelForCausalLM.from_pretrained(model)
    
    #model.save_pretrained("/data/model") 
    #volume.commit()
    move_cache()
    # tokenizer.save_pretrained("/data/tokenizer") 



#image = Image.debian_slim(python_version="3.10.14").pip_install(
#image = Image.debian_slim(python_version="3.11").from_registry(
image = Image.debian_slim().from_registry(
        "nvidia/cuda:12.1.0-base-ubuntu22.04", add_python="3.11").pip_install(
    "modal==0.62.63",
        "vllm",
        "torch",
        "transformers",
        "ray",
        "hf-transfer",
        "huggingface_hub",
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
    "tensorflow",
    "bitsandbytes",
    "tblib",
    "accelerate",
     ).apt_install(
         "git",
           "curl").run_function(download_model, shared_volumes={"/data": volume}, timeout=60*30)

stub = Stub(
    name="ThinkWell",
    image=image,
    #secrets=[Secret.from_name("nomic-key")],
)

