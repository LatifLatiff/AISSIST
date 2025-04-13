import os
import uuid
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from openai import OpenAI
os.makedirs("static", exist_ok=True)


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs("static", exist_ok=True)

client = OpenAI(api_key="YOUR API KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    response_text = ""
    chart_path = None

    if request.method == "POST":
        uploaded_file = request.files.get("file")
        
        if uploaded_file and uploaded_file.filename.endswith(".csv"):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
            uploaded_file.save(file_path)

            try:
                # CSV oku
                df = pd.read_csv(file_path)
                preview = df.head(5).to_string()

                # OpenAI'ye gönderilecek içerik
                prompt = f"Şu CSV verisini analiz et ve istatistiksel özet çıkar:\n\n{preview}"

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )

                response_text = response.choices[0].message.content.strip()

                # Sayısal sütunlardan grafik çiz
                numeric_cols = df.select_dtypes(include=["number"]).columns
                if len(numeric_cols) > 0:
                    first_numeric = numeric_cols[0]
                    chart_filename = f"static/chart_{uuid.uuid4().hex}.png"

                    plt.figure(figsize=(8, 4))
                    df[first_numeric].head(20).plot(kind="bar", color="orange", title=first_numeric)
                    plt.ylabel(first_numeric)
                    plt.tight_layout()
                    plt.savefig(chart_filename)
                    plt.close()

                    chart_path = chart_filename
                else:
                    response_text += "\n\nGrafik için sayısal veri bulunamadı."

            except Exception as e:
                response_text = f"Hata oluştu: {str(e)}"

        else:
            response_text = "Lütfen .csv uzantılı bir dosya yükleyin."

    return render_template("index.html", response=response_text, chart=chart_path)

if __name__ == "__main__":
    app.run(debug=True)
