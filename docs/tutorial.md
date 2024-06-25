# Tutorial da Aplicação

## Descrição

Este tutorial explica como usar a aplicação web containerizada feita no Trabalho 1 da discplina de "Desenvolvimento e Operações na Web".

## Como iniciar:

Para iniciar o processo de desenvolvimento da aplicação web conteinerizada, siga os passos abaixo:

## Passo 1 (Servidor de desenvolvimento):

1. Criar duas máquinas virtuais sendo respectivamente, uma para o servidor de desenvolvimento e uma para o servidor de produção com a imagem docker utilizando o multipass:
   ```bash
   multipass launch -n srvdev docker

   multipass launch -n srvprod docker

2. Iniciar o servidor de desenvolvimento:
   ```bash
   multipass shell srvdev

3. Criar um diretório com o nome da companhia fictícia escolhida:
    ```bash
    mkdir sua-companhia/

4. Entrar no diretório:
    ```bash
    cd sua-companhia/

5. Criar um diretório para o banco de dados e um para o web:
    ```bash
    mkdir db

    mkdir web

## Passo 2 (Configurando o banco de dados):

1. Entrar no diretório do banco de dados:
    ```bash
    cd db

2. Criar um arquivo "Dockerfile":
    ```bash
    vi Dockerfile

3. Dentro do arquivo "Dockerfile" escrever os comandos necessários para o funcionamento do banco de dados:
    ```bash
    FROM postgres
    ENV TZ=America/Sao_Paulo
    COPY ./nome-banco-de-dados.sql /docker-entrypoint-initdb.d/

4. Criar o arquivo sql para o banco de dados e inserir o código para sua criação:
    ```bash
    vi nome-banco-de-dados.sql

## Passo 3 (Iniciar o serviço do container do banco de dados):

1. Retornar ao diretório principal e criar um arquivo denominado compose.yaml:
    ```bash
    cd ..
    vi compose.yaml

2. Dentro do arquivo "compose.yaml" colocar os comandos necessários para o container ser iniciado:
    ```bash
    services:
        db:
            build: ./db
            environment:
            POSTGRES_USER: webuser
            POSTGRES_PASSWORD: crud321
            POSTGRES_DB: contact
            volumes:
            - postgresqldata:/var/lib/postgresql/data

    volumes:
        postgresqldata:

3. Iniciar os serviços definidos:
    ```bash
    docker compose up -d

## Passo 4 (Configurando o web)

1. Entrar no diretório "web" e criar o arquivo "Dockefile":
    ```bash
    cd web
    vi Dockerfile

2. Dentro do arquivo "Dockerfile" escrever os comandos necessários para o funcionamento do container web:
    ```bash
    FROM php:8.1-apache

    RUN apt-get update && apt-get install -y libpq-dev

    ENV TZ=America/Sao_Paulo
    RUN docker-php-ext-install pdo_pgsql pgsql
    RUN rm -Rf /var/www/html/
    COPY ./www /var/www/html/

3. Voltar ao diretório principal e atualizar o arquivo "compose.yaml" para colocar os comandos necessários para o container web:
    ```bash
    cd ..
    vi compose.yaml

    services:
        db:
            build: ./db
            environment:
            POSTGRES_USER: webuser
            POSTGRES_PASSWORD: crud321
            POSTGRES_DB: contact
            volumes:
            - postgresqldata:/var/lib/postgresql/data

        web:
            build: ./web
            ports:
            - "80:80"
            depends_on:
            - db
            environment:
            DATABASE_URL: postgres://webuser:crud321@db:5432/contact

    volumes:
        postgresqldata:

4. Voltar ao diretório web para fazer a criação da aplicação web CRUD dentro do diretório www:
    ```bash
    cd web
    git clone https://web:seu-token@github.com/seu-usuario/seu-arquivo-crud.git www

5. Entrar no diretório www e atualizar as credenciais de conexão com o banco de dados do seu arquivo ".php":
    ```bash
    cd www
    vi seu-arquivo.php

6. Voltar ao diretório principal e inicializar o container web:
    ```bash
    cd ..
    cd ..
    docker compose up -d

7. Verificar se os containers estão funcionando (Caso não estejam, utilize o comando "docker compose logs" para verificar quais são os erros):
    ```bash
    docker compose ps

8. Verificar no navegador utilizando o IP da máquina virtual, se a aplicação CRUD está funcionando:
    ```bash
    Para verificar o IP no console:
    ip -c -br -4 a

    No navegador:
    http://ip-do-srvdev

9. Remover os containers e os volumes para subir em produção:
    ```bash
    docker compose down --rmi all -v

## Passo 5 (Subir em produção)

1. Compactar a aplicação:
    ```bash
    cd ..
    tar -cvzf sua-companhia.tar.gz sua-companhia/

2. Copiar o arquivo compactado para dentro da sua atual máquina virtual:
    ```bash
    cp sua-companhia.tar.gz srvdev/

3. Sair da máquina virtual:
    ```bash
    exit

4. Copiar o arquivo compactado do servidor de desenvolvimento para o servidor de produção:
    ```bash
    cp multipass/srvdev/sua-companhia.tar.gz multipass/srvprod/

5. Entrar no servidor de produção e descompactar o arquivo:
    ```bash
    multipass shell srvprod

    tar -xvzf srvprod/sua-companhia.tar.gz

6. Acesse o diretório:
    ```bash
    cd sua-companhia/

7. Inicialize os containers:
    ```bash
    docker compose up -d

8. Verifique a aplicação em seu navegador:
    ```bash
    Para verificar o IP no console:
    ip -c -br -4 a

    No navegador:
    http://ip-do-srvprod