### 🚀 Guia de Integração com n8n

Este guia explica como integrar o **Multivozes BR Engine** ao n8n (versão `1.110.1`) de forma simples e direta, utilizando o nó nativo da OpenAI. O processo é rápido e permite que você use as vozes gratuitas da Microsoft em seus fluxos de trabalho.

#### 1️⃣ Passo 1: Configurar as Credenciais da OpenAI

1.  No painel do n8n, clique em **"Credentials"** (Credenciais) no menu lateral esquerdo.

2.  Clique no botão **"New Credential"** (Nova Credencial) no canto superior direito.

3.  Na janela de busca, procure por **"OpenAI API"** e selecione o nó.

4.  Dê um nome para a sua credencial, como `Multivozes BR Engine`.

5.  No campo **"API Key"**, digite a sua chave de API do `.env` do Multivozes (o valor padrão é `AIzaSyA2ee7ScIZ4QknJWJ9qjSXgBy-GymR3QaU`).

6.  Em **"Base URL"** (URL Base), insira o endereço do seu servidor seguido de `/v1`. Por exemplo:
    * Se estiver a correr localmente: `http://localhost:5050/v1`
    * Se estiver a correr num servidor remoto: `http://SEU_IP:5050/v1`

7.  Deixe o campo **"Organization ID"** em branco, pois ele não é necessário para o Multivozes.

8.  Clique no botão **"Save"** para guardar a credencial.

#### 2️⃣ Passo 2: Usar o Nó da OpenAI em um Workflow

1.  Crie um novo workflow no n8n.

2.  Adicione um nó de **"Trigger"** (Acionador) da sua escolha (por exemplo, `Manual Trigger`).

3.  Adicione um novo nó e procure por **"OpenAI"**. Selecione o nó chamado **"OpenAI"**.

4.  No nó da OpenAI, selecione as credenciais que você acabou de criar (`Multivozes BR Engine`).

5.  Em **"Resource"** (Recurso), selecione **"Audio"**.

6.  Em **"Operation"** (Operação), selecione **"Speech"**.

7.  Nos campos de parâmetros, preencha:
    * **Model:** Digite `tts-1`.
    * **Input:** Digite o texto que deseja converter em fala. Você pode usar uma expressão para pegar um texto de outro nó, como `{{ $json.text }}`.
    * **Voice:** Use um dos nomes de voz da tabela abaixo.

#### 🗣️ Vozes Mapeadas da OpenAI

Para simplificar a integração, o Multivozes BR Engine mapeia as vozes populares da OpenAI para as vozes do Edge-TTS. Basta usar o nome da voz da OpenAI diretamente no n8n.

| Nome OpenAI | Voz Edge-TTS | Gênero |
| :--- | :--- | :--- |
| `alloy` | `en-US-JennyNeural` | Feminino |
| `echo` | `en-US-GuyNeural` | Masculino |
| `fable` | `en-GB-SoniaNeural` | Feminino (Britânico) |
| `onyx` | `en-US-EricNeural` | Masculino (Grave) |
| `nova` | `en-US-AvaNeural` | Feminino |
| `shimmer` | `en-US-EmmaNeural` | Feminino |

#### 🖼️ Exemplo de Configuração Visual

A seguir, um exemplo visual da configuração no n8n para maior clareza.

!

#### 3️⃣ Passo 3: Executar o Workflow

1.  Clique em **"Execute Workflow"** para rodar o seu fluxo.

2.  O áudio gerado pelo Multivozes será retornado no campo de saída do nó da OpenAI, no formato de um buffer binário. Você pode então salvar este arquivo, enviá-lo por e-mail, ou usá-lo em outros nós do seu workflow.

Com este guia, a integração com o n8n deve ser muito mais fácil e intuitiva. 🤩


if __name__ == "__main__":
    print(readme_content)

