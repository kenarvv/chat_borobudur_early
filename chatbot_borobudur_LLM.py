import google.generativeai as genai

class PalmChatbot:
    def __init__(self, api_key):
        # Konfigurasi API
        genai.configure(api_key=api_key)
        
        # Konfigurasi model
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 1,
            'top_k': 40,
            'max_output_tokens': 200,
        }
        
        # Parameter keamanan
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
        ]
        
        # Inisiasi model
        self.model = genai.GenerativeModel(
            model_name='gemini-pro',
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        
        # Memulai sesi chat
        self.chat = self.model.start_chat(history=[])

    def generate_response(self, user_input):
        try:
            # Kirim pesan dan dapatkan respons
            response = self.chat.send_message(user_input)
            return response.text
        
        except Exception as e:
            return f"Maaf, terjadi kesalahan: {e}"

def main():
    # Hardcode API key
    api_key = 'AIzaSyBT9FCKg6e6fNskfaPFKpITsrIcrQkwnCw'

    chatbot = PalmChatbot(api_key)
    print("Chatbot PaLM: Hai! Aku siap mengobrol. Ketik 'bye' untuk keluar.")

    while True:
        user_input = input("Anda: ").strip()
        
        if user_input.lower() in ['bye', 'keluar', 'exit']:
            print("Chatbot: Sampai jumpa!")
            break
        
        response = chatbot.generate_response(user_input)
        print("Chatbot:", response)

if __name__ == "__main__":
    main()