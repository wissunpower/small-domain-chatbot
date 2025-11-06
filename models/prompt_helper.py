
import abc


class IPromptHelper(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def completion_to_prompt(completion) -> str:
        pass
    
    @staticmethod
    @abc.abstractmethod
    def messages_to_prompt(messages) -> str:
        pass

class QwenPromptHelper(IPromptHelper):
    @staticmethod
    def completion_to_prompt(completion) -> str:
        return f"<|im_start|>system\n<|im_end|>\n<|im_start|>user\n{completion}<|im_end|>\n<|im_start|>assistant\n"
    
    @staticmethod
    def messages_to_prompt(messages) -> str:
        prompt = ""
        for message in messages:
            if message.role == "system":
                prompt += f"<|im_start|>system\n{message.content}<|im_end|>\n"
            elif message.role == "user":
                prompt += f"<|im_start|>user\n{message.content}<|im_end|>\n"
            elif message.role == "assistant":
                prompt += f"<|im_start|>assistant\n{message.content}<|im_end|>\n"
        
        if not prompt.startswith("<|im_start|>system"):
            prompt = "<|im_start|>system\nYou are Qwen, created by Alibaba Cloud. You are a helpful assistant.<|im_end|>\n" + prompt
        
        prompt = prompt + "<|im_start|>assistant\n"
        
        return prompt
