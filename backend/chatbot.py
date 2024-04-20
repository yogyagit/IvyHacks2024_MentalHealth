from modal_image import image, stub
from modal import asgi_app, Image, Stub, method, enter, Secret

@stub.cls(image = image, gpu="T4", container_idle_timeout=300, 
        secrets=[Secret.from_name("thinkwell-key")],)
class CohereChatbot:
    @enter()
    #def start(self, model='command-r', max_tokens=4000, temperature=0.5):
    def enter(self): 
        print('AG>.inside start for cohere chatbot')
        import cohere
        import os
        self.client = cohere.Client(os.environ["COHERE_API_KEY"])
        self.model = 'command-r'
        self.max_tokens = 4000
        self.temperature = 0.1

    @method()
    def chat(self, message, chat_history=[]):
        response = self.client.chat(
            chat_history=chat_history,
            message=message,
            model=self.model,
            max_tokens=self.max_tokens,
            temperature=self.temperature
        )

        return response.text
