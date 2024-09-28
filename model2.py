import re
import google.generativeai as genai
from credentials import GEMINI_API

class ChatBot:
    def __init__(self, model, enable_cot):
        genai.configure(api_key = GEMINI_API)
        self.model = genai.GenerativeModel(model_name= model, generation_config= self.get_model_config(enable_cot=enable_cot))
        
        self.base_tone = """
        Role:
        You are a helpful conversational assistant.\n
        You will use chain of thoughts approch if and only if asked.\
        """

        self.cot_tone = """
        __Chain_Of_Thoughts__:
        You will impliment chain of thoughts approach if and only if asked explicitly.\
        Don't repeat same information while thinking\
        Use this format for chain of thoughts approach:\n
        <thinking>\
        (Break prompt into individual parts and think step by step. This is not a final user output)\
        </thinking>\n
        <preliminary>
        (Generate ideas based upon previous thoughts and give preliminary result. Include important steps which you can forget. This is not visible to user)\
        </preliminary>\n
        Let's think step by step.\
        """
        self.cot_result_tone = """
        Consolidate your thoughts from previous section to give final answer for user's prompt. This part will be visible to user.\
        """

        self.web_search_flag = False
        self.summarize_data_flag = False
        self.start_chat_flag = False
        self.chat_obj = None

    def get_model_config(self, temp:float = 0.5, tokens : int = 512, enable_cot = False) -> genai.types.GenerationConfig:
        tokens = 1024 if enable_cot else tokens
        temp = 0.8 if enable_cot else temp
        return genai.types.GenerationConfig(
            temperature = temp,
            max_output_tokens = tokens
        )

    def chat(self, prompt: str):

        
        # Initial model setup          
        if not self.start_chat_flag:
            set_tone  = [self.base_tone, self.cot_tone]
            self.chat_obj = self.model.start_chat(history=[])
            prompt = f"Instructions:{set_tone}, Prompt:{prompt}"
            self.start_chat_flag = True
        else:
            prompt = f"Prompt: {prompt}"

        model_response = self.chat_obj.send_message(prompt)
        return model_response.parts[0].text
        
    def chat_cot(self, prompt: str):

        # Initial model setup          
        if not self.start_chat_flag:
            set_tone  = [self.base_tone, self.cot_tone]
            self.chat_obj = self.model.start_chat(history=[])
            prompt = f"Instructions:{set_tone}.Use chain of thoughts approach only this time. Prompt:{prompt}"
            self.start_chat_flag = True
        else:
            prompt = f"Use chain of thoughts approach this time. Prompt:{prompt}"
        
        model_response = self.chat_obj.send_message(prompt)
        result = model_response.parts[0].text

        thought = re.search(r'<thinking>(.*?)</thinking>', result, re.DOTALL)
        preliminary = re.search(r'<preliminary>(.*?)</preliminary>', result, re.DOTALL)

        model_response = self.chat_obj.send_message(self.cot_result_tone)
        result = model_response.parts[0].text

        return result

    def restart_chat(self):
        self.start_chat_flag = False
