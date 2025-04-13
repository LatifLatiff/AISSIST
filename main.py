from openai import OpenAI

# 🔑 Buraya kendi API anahtarını gir
client = OpenAI(api_key="YOUR API KEY")
# 👇 Sonsuz döngü başlıyor
while True:
    user_input = input("Sen: ")

    # 🛑 Çıkış komutu
    if user_input.lower() in ["çık", "exit", "quit"]:
        print("Görüşürüz reis 👋")
        break

    # 🤖 OpenAI'den cevap al
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": user_input}
        ]
    )

    # 📩 Cevabı yazdır
    print("Asistan:", response.choices[0].message.content.strip())
