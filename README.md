# Primeiros passos

* Instalar python na máquina, pode utilizar a versão mais recente: https://www.python.org/downloads/
* Nesse repositório, criar um ambiente python para que seja instalado as bibliotecas necessárias. Caso esteja usando alguma idea, normalmente eles tem auxlio para esse tipo de criação.

## Criando ambiente Python

### Pycharm

Settings -> Project -> Python Interpreter -> Add Interpreter -> Add Local Interpreter -> Virtualenv Environment

Marque a opção de New e dê um nome ao diretório de ambiente na raiz do repositório, comumente é usando o nome `venv`.

### Visual Studio ou sem idea
No windows, deve ser setado o valor de variável de ambiente no PATH para que seja reconhecido o comando python no CMD uma vez instalado, basta seguir os passos:
* Copiar o diretorio onde foi instalado o python (normalmente esse é o diretório onde fica instalado: `C:\Users\seu usuario\AppData\Local\Programs\Python\Python312\`)
* No pesquisar do windows procure por "Editar as váriaveis de ambiente do sistema".
* Ao abrir a janela, clique em `Variável deAmbiente...`
* Em `Váriáveis do sistema` procure por `Path`
* Clique duas vezes e irá abrir uma janela de edição, clique em `Novo`
* e cole o caminho do diretório, clique em `OK`, `OK` e `OK`.
* No repositório deve ser possível criar o amabiente via `CMD`
* * No `CMD` na raíz do projeto digitar o comando `python -m venv venv`
* * Verificar se o diretório `venv` foi criado, se sim, seguir o próximo passo
* * Continuando no `CMD`, digitar o comando `venv\Scripts\activate.bat`, caso esteja usando o `Git Bash`, usar o comando `source venv/Scripts/activate`, isso fará com que fique ativo o uso do Virtual Environment e seja possível administrar as bibliotecas baixadas exclusivamente no repositório. 


Para ver se está funcionando normalmente, teste baixando a biblioteca do stackspot usando o comando `pip install -r addon/globalPlugins/requirements.txt`
 