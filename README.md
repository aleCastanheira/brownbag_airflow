# brownbag_airflow
Projeto criado para uma apresentação no Brownbag GFT para a equipe de dados.


## Setup
Vamos executar o projeto usando docker, para isso vamos executar mapeando a pasta de DAGs deste repositório com a do container
```
docker run -d -p 8080:8080 -v C:\Users\alexa\workspace\brownbag_airflow\dags:/usr/local/airflow/dags  puckel/docker-airflow webserver
```

Dentro do container, instalar as dependências do projeto:
```
pip install -r /usr/local/airflow/dags/requirements.txt
```

Ao abrir o navegador o Webserver
```
localhost:8080/admin
```

Acessar http://localhost:8080/admin/variable/ e adicionar as seguintes variáveis
- feed_tech = http://rss.uol.com.br/feed/tecnologia.xml
- feed_sports = https://www.uol.com.br/esporte/ultimas/index.xml
- feed_cinema = http://rss.uol.com.br/feed/cinema.xml



----

## Contato
https://www.linkedin.com/in/alexandre-castanheira/