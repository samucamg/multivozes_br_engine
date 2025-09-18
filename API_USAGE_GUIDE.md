# 🚀 Guia de Uso da API e Exemplos

Este guia mostra como interagir diretamente com a API do **Multivozes BR Engine** para gerar áudio a partir de texto. Vamos focar em exemplos práticos usando `curl`, uma ferramenta de linha de comando presente na maioria dos sistemas.

---

### 📋 Pré-requisitos para Executar os Exemplos

Antes de testar os comandos abaixo, garanta que você tem o seguinte:

* **Servidor Multivozes Ativo:** O seu motor deve estar instalado e a correr.
* **Endereço e Chave de API:** Você precisa de saber o endereço (`IP:PORTA`) do seu servidor e a sua `API_KEY`.
* **`curl`:** Ferramenta de linha de comando para fazer requisições. Já vem instalada na maioria dos sistemas (Linux, macOS, Windows 10+).
* **`Python` (Opcional):** Apenas para o exemplo em Python, é preciso ter o Python e a biblioteca `requests` (`pip install requests`).
* **`FFmpeg` (Opcional):** Necessário apenas se você quiser testar a reprodução direta de áudio (`| ffplay ...`).

#### ⚙️ Requisitos de Servidor Recomendados

Para uma boa performance do **Multivozes BR Engine**, recomendamos um servidor (VPS) com as seguintes especificações mínimas:

* **CPU:** 2 vCores
* **RAM:** 4 GB
* **Disco:** 20 GB de espaço livre

O projeto foi testado e funciona perfeitamente nos seguintes sistemas operacionais (64 bits):
* **Linux:**
    * Ubuntu 22.04 / 24.04 LTS
    * Debian 11 / 12
    * AlmaLinux 8 / 9
    * Sistemas ARM64 com Ubuntu (ex: Oracle Cloud)
* **Windows:**
    * Windows 10 / 11, utilizando WSL2 com Ubuntu 22.04 ou 24.04

---

### 📌 Endpoint Principal: `/v1/audio/speech`

Este é o coração da API. É para este "endereço" que enviaremos os nossos pedidos para gerar áudio.

#### Parâmetros da Requisição

Todos os parâmetros são enviados num formato JSON no corpo (body) do pedido.

* **`input` (obrigatório):** O texto que você quer converter para áudio. (Ex: `"Olá, mundo!"`)
* **`model` (opcional):** O modelo a ser usado. Para compatibilidade, pode ser `"tts-1"` ou `"tts-1-hd"`. O padrão é `"tts-1"`.
* **`voice` (opcional):** A voz a ser usada. Pode ser um dos nomes da OpenAI (`alloy`, `echo`, etc.) ou o nome técnico de qualquer voz do Edge TTS (ex: `"pt-BR-FranciscaNeural"`). Se não for especificado, usará a voz padrão definida no seu ficheiro `.env`.
* **`response_format` (opcional):** O formato do áudio. Opções: `mp3`, `opus`, `aac`, `flac`, `wav`, `pcm`. O padrão é `mp3`.
* **`speed` (opcional):** A velocidade da fala, onde `1.0` é a velocidade normal. Valores menores são mais lentos e maiores são mais rápidos. (Ex: `0.9` para mais lento, `1.2` para mais rápido).

---

### 🛠️ Exemplos Práticos com `curl`

**Lembre-se:** Substitua `SUA_CHAVE_API_AQUI` pela chave que você configurou no seu ficheiro `.env`. Se o servidor estiver noutra máquina, substitua `localhost` pelo IP do servidor.

#### Exemplo 1: Gerar e Salvar um Áudio em Português

Este é o caso de uso mais comum. Enviamos um texto e salvamos o resultado num ficheiro `audio.mp3`.

```bash
curl -X POST http://localhost:5050/v1/audio/speech \\
  -H "Authorization: Bearer SUA_CHAVE_API_AQUI" \\
  -H "Content-Type: application/json" \\
  -d '{
    "model": "tts-1",
    "input": "Olá, mundo! Este é um teste de geração de áudio com o Multivozes BR Engine.",
    "voice": "alloy"
  }' \\
  --output audio.mp3
```
Após executar, um ficheiro `audio.mp3` será criado na sua pasta.

#### Exemplo 2: Usando uma Voz Técnica e Mudando a Velocidade

Em vez de usar o nome `echo`, vamos pedir diretamente a voz do "Antônio" e deixá-la um pouco mais rápida.

```bash
curl -X POST http://localhost:5050/v1/audio/speech \\
  -H "Authorization: Bearer SUA_CHAVE_API_AQUI" \\
  -H "Content-Type: application/json" \\
  -d '{
    "input": "Testando a voz masculina pt-BR-AntonioNeural com uma velocidade um pouco mais alta.",
    "voice": "pt-BR-AntonioNeural",
    "speed": 1.1
  }' \\
  --output audio_rapido.mp3
```

#### Exemplo 3: Ouvir o Áudio Diretamente (Requer `ffplay`)

Se você tiver o `ffmpeg` instalado, pode usar o `ffplay` para ouvir o áudio gerado sem o salvar num ficheiro.

```bash
curl -X POST http://localhost:5050/v1/audio/speech \\
  -H "Authorization: Bearer SUA_CHAVE_API_AQUI" \\
  -H "Content-Type: application/json" \\
  -d '{
    "input": "Este áudio será reproduzido imediatamente.",
    "voice": "nova"
  }' | ffplay -autoexit -nodisp -i -
```
O áudio começará a tocar assim que for gerado.

---

### 🐍 Exemplo de Uso em Python

Claro, você não precisa de se limitar ao `curl`. Aqui está um exemplo de como chamar a API a partir de um script Python usando a biblioteca `requests`.

```python
import requests
import shutil

# --- Configurações ---
API_URL = "http://localhost:5050/v1/audio/speech"
API_KEY = "SUA_CHAVE_API_AQUI"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
DATA = {
    "model": "tts-1",
    "input": "Este áudio foi gerado a partir de um script Python!",
    "voice": "shimmer"
}
OUTPUT_FILE = "audio_python.mp3"

# --- Fazendo a Requisição ---
try:
    # Usamos stream=True para lidar com a resposta de forma eficiente
    response = requests.post(API_URL, headers=HEADERS, json=DATA, stream=True)

    # Verifica se a requisição foi bem-sucedida
    if response.status_code == 200:
        print(f"Sucesso! A salvar o áudio em '{OUTPUT_FILE}'...")
        # Escreve o conteúdo da resposta para um ficheiro
        with open(OUTPUT_FILE, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        print("Áudio salvo com sucesso!")
    else:
        # Imprime o erro se algo der errado
        print(f"Erro ao gerar áudio: {response.status_code}")
        print(response.json())

except requests.exceptions.RequestException as e:
    print(f"Erro de conexão: {e}")

```
Este script faz o mesmo que o Exemplo 1, mas de forma programática dentro do Python.
"""


