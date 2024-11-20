import matplotlib
matplotlib.use('Agg')
import plotly.express as px
from flask import *
from config import app, db
from formularios import *
import os
import pandas as pd
from models import Course
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import LabelEncoder
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

if not os.path.isdir("upload"):
    os.mkdir("upload")


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        # Get form data
        level = request.form.get("level")
        content_duration = float(request.form.get("content_duration"))
        subject = request.form.get("subject")
        is_paid = request.form.get("is_paid") == "true"
        
        # Get all courses from database
        courses = Course.query.all()
        
        if not courses:
            flash("Não há dados suficientes para fazer a previsão. Por favor adicione dados primeiro.")
            return render_template("/index.html")

        # Prepare data for model
        df = pd.DataFrame([{
            'level': c.level,
            'content_duration': c.content_duration,
            'subject': c.subject,
            'is_paid': c.is_paid,
            'price': c.price
        } for c in courses])

        # Encode categorical variables
        le_level = LabelEncoder()
        le_subject = LabelEncoder()
        
        df['level_encoded'] = le_level.fit_transform(df['level'])
        df['subject_encoded'] = le_subject.fit_transform(df['subject'])
        
        # Prepare features
        X = df[['level_encoded', 'content_duration', 'subject_encoded', 'is_paid']].values
        y = df['price'].values

        # Train model
        model = LinearRegression()
        model.fit(X, y)
        
        # Prepare input data for prediction
        input_level = le_level.transform([level])[0]
        input_subject = le_subject.transform([subject])[0]
        input_data = np.array([[input_level, content_duration, input_subject, is_paid]])
        
        # Make prediction
        predicted_price = model.predict(input_data)[0]
        
        return jsonify({'predicted_price': round(predicted_price, 2)})

    # Get unique values for dropdowns
    levels = db.session.query(Course.level).distinct().all()
    subjects = db.session.query(Course.subject).distinct().all()
    
    # Default values if database is empty
    if not levels:
        levels = [('All Levels',), ('Beginner Level',), ('Intermediate Level',), ('Expert Level',)]
    if not subjects:
        subjects = [('Web Development',), ('Business Finance',), ('Musical Instruments',), 
                   ('Graphic Design',), ('Business',), ('Other',)]
    
    return render_template("/index.html", 
                         levels=[level[0] for level in levels],
                         subjects=[subject[0] for subject in subjects])


@app.route("/adicionar", methods=["POST", "GET"])
def adicionar():
    formulario = FileForm()
    graph1_html, graph2_html, graph3_html = None, None, None

    if formulario.validate_on_submit():
        f = formulario.file.data
        filename = f"upload/{f.filename}"
        f.save(filename)

        csv_file = filename
        df = pd.read_csv(csv_file)

        for i, row in df.iterrows():
            course = Course(
                course_title=row['course_title'],
                is_paid=row['is_paid'],
                price=row['price'],
                level=row['level'],
                content_duration=row['content_duration'],
                subject=row['subject']
            )
            db.session.add(course)
        db.session.commit()

        courses = Course.query.all()
        df = pd.DataFrame([{
            'level': c.level,
            'content_duration': c.content_duration,
            'subject': c.subject,
            'is_paid': c.is_paid,
            'price': c.price
        } for c in courses])

        # Gráfico 1: Preço médio por nível
        plt.figure(figsize=(10, 6))
        df.groupby('level')['price'].mean().plot(kind='bar', color='skyblue')
        plt.title("Preço Médio por Nível")
        plt.ylabel("Preço Médio")
        plt.xlabel("Nível")
        plt.xticks(rotation=0)  # Rotaciona os rótulos no eixo X em 45 graus
        img1 = io.BytesIO()
        plt.savefig(img1, format='png')
        img1.seek(0)
        graph_price_level = base64.b64encode(img1.getvalue()).decode()
        plt.close()

        # Gráfico 2: Contagem de cursos por assunto
        plt.figure(figsize=(10, 6))
        df['subject'].value_counts().plot(kind='bar', color='purple')
        plt.title("Número de Cursos por Assunto")
        plt.ylabel("Número de Cursos")
        plt.xlabel("Assunto")
        plt.xticks(rotation=0)
        img2 = io.BytesIO()
        plt.savefig(img2, format='png')
        img2.seek(0)
        graph_subjects = base64.b64encode(img2.getvalue()).decode()
        plt.close()

        # Gráfico 3: Proporção de cursos pagos e gratuitos
        plt.figure(figsize=(8, 8))
        df['is_paid'].value_counts().plot(
            kind='pie', labels=['Pago', 'Gratuito'], autopct='%1.1f%%', startangle=90, colors=['gold', 'lightblue']
        )
        plt.title("Proporção de Cursos Pagos e Gratuitos")
        img3 = io.BytesIO()
        plt.savefig(img3, format='png')
        img3.seek(0)
        graph_paid_free = base64.b64encode(img3.getvalue()).decode()
        plt.close()

        # Gráfico 4: Duração média dos cursos por nível
        plt.figure(figsize=(10, 6))
        df.groupby('level')['content_duration'].mean().plot(kind='bar', color='green')
        plt.title("Duração Média dos Cursos por Nível")
        plt.ylabel("Duração Média (Horas)")
        plt.xlabel("Nível")
        plt.xticks(rotation=0)
        img4 = io.BytesIO()
        plt.savefig(img4, format='png')
        img4.seek(0)
        graph_duration_level = base64.b64encode(img4.getvalue()).decode()
        plt.close()

        # Gráfico 5: Distribuição de preços dos cursos pagos
        plt.figure(figsize=(10, 6))
        df[df['is_paid'] == True]['price'].plot(kind='hist', bins=15, color='orange', edgecolor='black')
        plt.title("Distribuição de Preços dos Cursos Pagos")
        plt.xlabel("Preço")
        plt.ylabel("Frequência")
        img5 = io.BytesIO()
        plt.savefig(img5, format='png')
        img5.seek(0)
        graph_price_distribution = base64.b64encode(img5.getvalue()).decode()
        plt.close()



        # Passar todos os gráficos para o template
        return render_template(
            "/adicionar.html",
            attr=formulario,
            graph_price_level=graph_price_level,
            graph_subjects=graph_subjects,
            graph_paid_free=graph_paid_free,
            graph_duration_level=graph_duration_level,
            graph_price_distribution=graph_price_distribution,
        )


    return render_template("/adicionar.html", attr=formulario)


if __name__ == "__main__":

    if not os.path.isdir("upload"):
        os.mkdir("upload")

    app.run(debug=True)
