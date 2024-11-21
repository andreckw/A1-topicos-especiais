# A1-topicos-especiais

## Funcionalidades
    Upload e Flexibilidade dos Dados:

    A aplicação permite o upload de arquivos CSV contendo dados de cursos, como temas, preço, duração, nível de dificuldade, etc. Os dados são automaticamente processados e armazenados em um banco de dados SQLite.

    Através de gráficos interativos utilizando Plotly, a aplicação realiza a visualização de dados, como popularidade por tema de curso, preços médios por nível, distribuição de alunos por área de estudo, entre outros.

    Machine Learning com Personalização de Modelos:

    A aplicação utiliza modelos de Machine Learning para realizar previsões baseadas nos dados dos cursos, como prever o preço de um curso com base em seu nível e área de estudo.
    
    Treinamento Dinâmico do Modelo:

    O modelo de machine learning pode ser treinado dinamicamente com novos dados importados. À medida que mais dados são adicionados ao banco, o modelo é atualizado e otimizado.
    A capacidade de treinar modelos em tempo real permite um ajuste contínuo para melhorar a precisão das previsões.

## Tecnologias Utilizadas

- **Flask**: Framework web para construção da aplicação.
- **Matplotlib**: Para a criação de gráficos.
- **Plotly**: Biblioteca para gráficos interativos e visualização de dados.
- **Pandas**: Biblioteca para análise e manipulação de dados.
- **SQLAlchemy**: ORM para interação com o banco de dados.
- **SQLite**: Banco de dados utilizado para armazenar as informações dos cursos.
- **HTML/CSS**: Para a criação da interface web.
 
## Comandos para criação do VENV
``` shell
    py -m venv .venv
    .venv/Scripts/activate

## Os gráficos interativos podem demorar um pouco a carreagar
```


## Comandos para o flask
``` shell
    pip install flask
    pip install -U Flask-SQLAlchemy
    pip install -U Flask-WTF
    pip install pandas
    pip install -U scikit-learn
    
    flask --app main run
```


## Estilo do CSS
Foi utilizado o [Bulma Css Framework](https://bulma.io/documentation/)