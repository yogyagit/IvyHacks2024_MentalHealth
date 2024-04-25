from modal_image import image, stub
from modal import asgi_app, Image, Stub, method, enter, Secret

# @stub.cls(image = image, gpu="T4", container_idle_timeout=300, 
#         secrets=[Secret.from_name("thinkwell-key")],)
# class CohereChatbot:
#     @enter()
#     #def start(self, model='command-r', max_tokens=4000, temperature=0.5):
#     def enter(self): 
#         print('AG>.inside start for cohere chatbot')
#         import cohere
#         import os
#         self.client = cohere.Client(os.environ["COHERE_API_KEY"])
#         self.model = 'command-r'
#         self.max_tokens = 4000
#         self.temperature = 0.1

#     @method()
#     def chat(self, message, chat_history=[]):
#         response = self.client.chat(
#             chat_history=chat_history,
#             message=message,
#             model=self.model,
#             max_tokens=self.max_tokens,
#             temperature=self.temperature
#         )

#         return response.text

@stub.cls(image = image, gpu="A100", container_idle_timeout=1200, 
        secrets=[Secret.from_name("thinkwell-key")],)
class CohereChatbot_local:
    @enter()
    #def start(self, model='command-r', max_tokens=4000, temperature=0.5):
    def enter(self): 
        print('AG>.inside start for cohere chatbot.but local')
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        self.tokenizer = AutoTokenizer.from_pretrained("CohereForAI/c4ai-command-r-v01", local_files_only=True)
        self.model = AutoModelForCausalLM.from_pretrained("CohereForAI/c4ai-command-r-v01", local_files_only=True)

    @method()
    def chat(self, message, chat_history=[]):

        chat_history.append({"role": "user", "content": message})
        for i in chat_history:
            print(f"AG:::{i.keys()}")
            print("AG:::", i["role"])
        print(f"Also, chat hiustory:{chat_history}")
        input_ids = self.tokenizer.apply_chat_template(chat_history, tokenize=True, add_generation_prompt=True, return_tensors="pt")
        ## <BOS_TOKEN><|START_OF_TURN_TOKEN|><|USER_TOKEN|>Hello, how are you?<|END_OF_TURN_TOKEN|><|START_OF_TURN_TOKEN|><|CHATBOT_TOKEN|>

        gen_tokens = self.model.generate(
        input_ids, 
        max_new_tokens=200, 
        do_sample=True, 
        temperature=0.3,
        )

        gen_text = self.tokenizer.decode(gen_tokens[0])

        return gen_text
