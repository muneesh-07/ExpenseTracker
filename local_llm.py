from transformers import pipeline, AutoTokenizer

class FreeAIAssistant:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("distilgpt2")
        self.pipe = pipeline(
            "text-generation",
            model="distilgpt2",
            tokenizer=self.tokenizer,
            device=-1,  # Use CPU
            truncation=True,  # Explicit truncation
            max_length=100,
            pad_token_id=self.tokenizer.eos_token_id
        )
        
    def generate_response(self, prompt):
        # Clean the prompt and add context
        clean_prompt = f"User: {prompt.strip()}\nAssistant:"
        
        # Generate response with proper parameters
        response = self.pipe(
            clean_prompt,
            max_new_tokens=50,
            temperature=0.7,
            do_sample=True,
            top_k=50,
            num_return_sequences=1
        )
        
        # Extract and clean the response
        full_text = response[0]['generated_text']
        assistant_response = full_text.split("Assistant:")[-1].strip()
        
        # Remove any trailing incomplete sentences
        if "." in assistant_response:
            assistant_response = assistant_response.rsplit(".", 1)[0] + "."
        elif "?" in assistant_response:
            assistant_response = assistant_response.rsplit("?", 1)[0] + "?"
            
        return assistant_response or "I didn't understand that."