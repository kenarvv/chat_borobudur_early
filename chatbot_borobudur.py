import json
import random
from fuzzywuzzy import fuzz

# Load Knowledge Base
def load_knowledge_base(file_path="kb_borobudur.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

# Helper: Search for a role/entity dynamically across all categories
def search_entity(entity_name, kb, threshold=80):
    found_entities = []
    # Search through each category in the knowledge base
    for category in kb:
        for item in kb[category]:
            # Check if the entity name matches either the 'jabatan' or 'nama' field
            if fuzz.partial_ratio(entity_name.lower(), item.get("jabatan", "").lower()) >= threshold or \
               fuzz.partial_ratio(entity_name.lower(), item.get("nama", "").lower()) >= threshold:
                found_entities.append(item)
    return found_entities

# Helper: Match keywords to intents
def detect_intent(user_input):
    user_input = user_input.lower()
    
    # Check for location-related queries
    if "dimana" in user_input or "lokasi" in user_input:
        return "location"
    
    # Check for queries about services
    if "layanan" in user_input or "kantor" in user_input:
        return "services"
    
    # Check for queries about tourist attractions
    if "wisata" in user_input or "tempat wisata" in user_input:
        return "tourism"
    
    # Check for queries about food (kuliner)
    if "kuliner" in user_input or "makanan" in user_input:
        return "food"
    
    # Check for queries about transport
    if "transportasi" in user_input or "stasiun" in user_input or "terminal" in user_input:
        return "transport"
    
    # Check for queries about any role or entity in the knowledge base
    if "desa" in user_input and "kepala" in user_input or "sekretaris" in user_input:
        return "village_council"
    
    # Default intent (fallback)
    return "default"

# Chatbot Logic
def chatbot_borobudur(user_input, knowledge_base, context):
    intent = detect_intent(user_input)
    response = ""

    # Location-related queries
    if intent == "location":
        entity_name = user_input.replace("dimana", "").replace("lokasi", "").strip()
        entity = search_entity(entity_name, knowledge_base)
        if entity:
            for e in entity:
                response += f"{e['nama']} terletak di {e.get('deskripsi', 'Deskripsi tidak tersedia')}. "
        else:
            response = "Maaf, saya tidak menemukan lokasi tersebut."

    # Services-related queries
    elif intent == "services":
        response = "Berikut layanan masyarakat di Desa Borobudur:\n"
        for layanan in knowledge_base["layanan_masyarakat"]:
            response += f"- {layanan['nama']}: Lokasi: {layanan['lokasi']}, Jadwal: {layanan['jadwal']}.\n"

    # Tourist-related queries
    elif intent == "tourism":
        if "nama" in user_input:
            entity_name = user_input.split("nama")[-1].strip()
            entity = search_entity(entity_name, knowledge_base)
            if entity:
                for e in entity:
                    response = f"{e['nama']}: {e.get('deskripsi', 'Deskripsi tidak tersedia')} (Tiket: {e.get('tiket', 'Tidak tersedia')}, Jam: {e.get('jam_operasional', 'Tidak tersedia')})."
            else:
                response = "Maaf, saya tidak menemukan tempat wisata tersebut."
        else:
            response = "Berikut tempat wisata di Desa Borobudur:\n"
            for wisata in knowledge_base["wisata"]:
                response += f"- {wisata['nama']}: {wisata['deskripsi']}.\n"

    # Food-related queries
    elif intent == "food":
        response = "Kuliner khas Desa Borobudur:\n"
        for kuliner in knowledge_base["kuliner"]:
            response += f"- {kuliner['nama']}: {kuliner['deskripsi']} (Harga: {kuliner['harga']}).\n"

    # Transport-related queries
    elif intent == "transport":
        response = "Informasi transportasi di Desa Borobudur:\n"
        for transport in knowledge_base["transportasi"]:
            response += f"- {transport['nama']}: {transport['deskripsi']} (Lokasi: {transport['lokasi']}).\n"

    # Village Council-related queries
    elif intent == "village_council":
        found_role = False
        # Check if any role in the 'perangkat_desa' category matches the user's input
        entity = search_entity(user_input, knowledge_base)
        if entity:
            for e in entity:
                response = f"{e['nama']} adalah {e['jabatan']} di Desa Borobudur. Alamat: {e['alamat']}, Kontak: {e.get('no_hp', 'Tidak tersedia')}."
                found_role = True
                break
        
        if not found_role:
            response = "Maaf, saya tidak menemukan perangkat desa dengan nama tersebut."

    # Default fallback
    elif intent == "default":
        response = random.choice([
            "Maaf, saya tidak mengerti. Bisa dijelaskan lebih lanjut?",
            "Hmm, saya belum punya informasi tentang itu. Coba tanyakan hal lain?"
        ])

    return response

# Main Program
def main():
    kb = load_knowledge_base("kb_borobudur.json")
    context = {}  # Placeholder for future context tracking
    print("Halo! Selamat datang di Chatbot Desa Borobudur. Silakan tanya apa saja tentang desa ini.")
    while True:
        user_input = input("Anda: ")
        if user_input.lower() in ["keluar", "exit", "bye"]:
            print("Chatbot: Terima kasih telah menggunakan layanan ini. Sampai jumpa!")
            break
        response = chatbot_borobudur(user_input, kb, context)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    main()
