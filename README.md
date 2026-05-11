# adp-rh-saintgobain


Automação de processos de RH via integração com a API da ADP.
Busca dados de funcionários, aplica transformações e exporta relatórios em Excel.

---

## Estrutura do projeto

adp-rh-saintgobain/
│
├── main.py                  >> ponto de entrada
├── fake_adp.py              >> servidor local para desenvolvimento sem acesso real
├── requirements.txt
├── .env.example             >> modelo de variáveis de ambiente
│
├── src/
│   ├── config.py            >> lê e valida o .env
│   ├── auth/
│   │   └── token.py         >> OAuth2: busca, cache e renovação de token
│   ├── utils/
│   │   └── http.py          >> get() e post() com retry automático
│   └── workers/
│       ├── buscar.py        >> funções de negócio + paginação
│       └── exportar.py      >> exporta DataFrame para Excel
│
├── tests/
│   └── test_auth.py         >> testes do módulo de autenticação
│
└── data/output/             >> relatórios gerados (.xlsx)>

---

## Como rodar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/adp-rh-saintgobain.git
cd adp-rh-saintgobain
```

### 2. Instale as dependências

```bash
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

Preencha o `.env` com suas credenciais. Para desenvolvimento local, use:

ADP_CLIENT_ID=qualquer-coisa
ADP_CLIENT_SECRET=qualquer-coisa
ADP_TOKEN_URL=http://localhost:5000/auth/oauth/v2/token
ADP_BASE_URL=http://localhost:5000

### 4. Suba o servidor de desenvolvimento

```bash
python fake_adp.py
```

### 5. Em outro terminal, rode o projeto

```bash
python main.py
```

### 6. Para rodar os testes

```bash
pytest tests/
```
