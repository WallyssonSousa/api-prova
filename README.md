# api-prova
Essa api funciona em conjunto com a api de gestão escolar e com a api de reservar sala. 1- Gestão Escolar, 2- Reservar sala e 3- Adicionar prova

---

## 🚀 Tecnologias Utilizadas

---

## 📁 Estrutura do Projeto

---

## Como Rodar o Projeto (Via Docker)
### 🔨 Fazendo o build da imagem
```sh
docker compose build
```
Isso usará o build definido no docker-compose.yml, criará a imagem api-prova:1.0 e já prepara tudo pro up.
### 🚀 Rodando a aplicação
```sh
docker compose up
```
ou em modo "background":
```sh
docker compose up -d
```
### ⛔ Parando a aplicação:
```sh
Ctrl+C
```
ou em modo "background":
```sh
docker compose down
```
### ❌ Apagando a imagem:
**Usando docker compose:**
```sh
docker compose down --rmi all
```
`--rmi all` remove todas as imagens construídas pelo docker compose;
`-v` se quiser também remover volumes

---

## ⚙️ Como Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/WallyssonSousa/api-prova.git
cd api-prova

# Criar e Ativar um Ambiente Virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

#  Instalar Dependências
pip install -r requirements.txt

# Configurar o Banco de Dados
flask db init
flask db migrate -m "Inicialização do banco de dados"
flask db upgrade

# Rodar o Servidor Flask - O servidor será iniciado em http://127.0.0.1:5002/
python app.py

# Como Executar os Testes
pytest