import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

class BorobudurChatbot:
    def __init__(self, knowledge_base_path):
        # Memuat environment variables
        load_dotenv()
        api_key = os.getenv('GOOGLE_API_KEY')
        
        # Konfigurasi API Gemini
        genai.configure(api_key=api_key)
        
        # Konfigurasi model
        self.generation_config = {
            'temperature': 0.7,
            'top_p': 1,
            'top_k': 40,
            'max_output_tokens': 500,
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
        
        # Memuat knowledge base
        with open(knowledge_base_path, 'r', encoding='utf-8') as file:
            self.knowledge_base = json.load(file)
        
        # Inisiasi model
        self.model = genai.GenerativeModel(
            model_name='gemini-pro',
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        
        # Memulai sesi chat
        self.chat = self.model.start_chat(history=[])
        
        # Membuat konteks awal
        self.context = self._prepare_context()

    def _prepare_context(self):
        # Membuat konteks dari informasi JSON
        context = f"""Kamu adalah chatbot resmi untuk Desa Borobudur. 
Lokasi: {self.knowledge_base['desa']['lokasi']}
Sejarah Singkat: {self.knowledge_base['desa']['sejarah']}

Informasi Tersedia:
🏛️ Wisata: {', '.join([wisata['nama'] for wisata in self.knowledge_base['wisata']])}
🍲 Kuliner: {', '.join([kuliner['nama'] for kuliner in self.knowledge_base['kuliner']])}
🚌 Transportasi: {', '.join([transport['Nama'] for transport in self.knowledge_base['transportasi']])}

Tolong jawab pertanyaan seputar Desa Borobudur dengan ramah dan informatif."""
        return context

    def generate_response(self, user_input):
        # Tambahkan konteks ke dalam prompt
        full_prompt = f"{self.context}\n\nPertanyaan Pengguna: {user_input}"
        
        try:
            response = self.chat.send_message(full_prompt)
            return response.text
        
        except Exception as e:
            return f"Maaf, terjadi kesalahan: {e}"