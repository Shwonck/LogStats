# LogStats CLI

Ferramenta em linha de comando para análise e geração de estatísticas a partir de arquivos de log.

## 🐳 Como Executar via Docker

Não é necessário ter o Python instalado localmente para rodar a aplicação, apenas o Docker.

### 1. Construir a Imagem Docker

Na raiz do projeto, execute:

```bash
docker build -t logstats .
```

### 2. Executar a Análise

Mapeie o diretório atual (onde está o seu arquivo de log) para dentro do container e passe o nome do log como argumento:

```bash
docker run --rm -v "$(pwd):/app" logstats access.log
```

### 3. Filtrar por Data (`--since`)

```bash
docker run --rm -v "$(pwd):/app" logstats access.log --since "2026-07-21T09:00:00"
```

### 🧪 Executar Testes Unitários no Container

```bash
docker run --rm --entrypoint pytest logstats
```