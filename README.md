# Modelo de pandemia baseado em agentes

Esse é um modelo toy (SIR) de pandemias feito como atividade da disciplina Modelagem e Simulação Computacional (IMD0607) da UFRN.

## Para instalar o ambiente e rodar o modelo

- Clonar este repositório, e uma vez clonado:

```bash
# Criar o ambiente com python>=3.6
python3 -m venv .venv

# Ativar o ambiente
source .venv/bin/activate

# Instalar as dependências
pip install -r requirements.txt

# Rodar a simulação e salvar os dados resultantes
cd src/
python batch_run.py

# Servir página web com o modelo
cd src/
mesa runserver
```

Após rodar o último comando, será servida uma página em `localhost:8521`, que você pode acessar pelo seu navegador.

Grupo:

- Daniel Barbosa
- João Vitor Cavalcante
- João Vitor Venceslau
- Vitor Gabriel Saldanha
