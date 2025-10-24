# Atualizador de Porta do qBittorrent

Este projeto contém um script Python (`qbittorrent_port_updater.py`) que detecta a porta redirecionada de uma VPN WireGuard (como ProtonVPN) usando o script `port-checker.py` e atualiza a porta de escuta do qBittorrent para corresponder a ela. O script executa em um loop, verificando a porta a cada 45 segundos e atualizando o qBittorrent se necessário. Este README fornece instruções para configurar e executar o script no **Windows** em português brasileiro.

## Pré-requisitos

Antes de executar o script, certifique-se de ter:

- **Python 3.x**: Versão 3.9 ou superior recomendada.
- **qBittorrent**: Instalado com a interface web (Web UI) ativada.
- **VPN WireGuard**: Configurada com NAT-PMP ou redirecionamento de porta ativado (ex.: ProtonVPN).
- **port-checker.py**: Um script que detecta a porta redirecionada da VPN e exibe `The forwarded port is: <porta>`.

## Instalação no Windows

Siga estas etapas para instalar as dependências e executar o script no Windows.

### 1. Instalar o Python
1. **Baixar o Python**:
   - Acesse [python.org](https://www.python.org/downloads/windows/) ou instale pelo Microsoft Store.
   - Escolha Python 3.9 ou superior (ex.: Python 3.11).
2. **Instalar o Python**:
   - Execute o instalador.
   - Marque a opção **"Add Python to PATH"** durante a instalação.
   - Verifique a instalação abrindo o Prompt de Comando ou PowerShell e executando:
     ```
     python --version
     ```
     Você deve ver a versão do Python (ex.: `Python 3.11.0`).
3. **Comando Alternativo**:
   - Se `python` não funcionar, tente `py` ou `python3`. O script usa `sys.executable` para lidar com isso automaticamente.

### 2. Instalar Bibliotecas Python Necessárias
O script requer a biblioteca `requests`. As bibliotecas `configparser` e `pathlib` já estão incluídas na biblioteca padrão do Python.

1. Abra o Prompt de Comando ou PowerShell.
2. Instale a biblioteca `requests` usando pip:
   ```
   pip install requests
   ```
3. Verifique a instalação:
   ```
   pip show requests
   ```
   Você deve ver detalhes sobre o pacote `requests` instalado.

### 3. Instalar o natpmpc (Opcional)
O script chama o `natpmpc` para renovar mapeamentos NAT-PMP, mas isso só é necessário se o seu `port-checker.py` depende do `natpmpc`. Se o `port-checker.py` detecta a porta de forma independente (ex.: via API da VPN), pule esta etapa.

1. **Baixar o libnatpmp**:
   - Acesse [miniupnp.free.fr](http://miniupnp.free.fr/libnatpmp.html) e baixe o código-fonte do `libnatpmp`.
2. **Compilar o natpmpc**:
   - Instale um compilador C, como [MinGW](http://www.mingw.org/) ou [MSYS2](https://www.msys2.org/).
   - No MSYS2, instale as dependências:
     ```
     pacman -S mingw-w64-x86_64-gcc
     ```
   - Extraia o código-fonte do `libnatpmp`, navegue até o diretório e compile:
     ```
     make
     ```
   - Isso gera o `natpmpc.exe`.
3. **Adicionar natpmpc ao PATH**:
   - Copie o `natpmpc.exe` para o mesmo diretório do `qbittorrent_port_updater.py` ou para um diretório incluído no PATH do sistema (ex.: `C:\Windows`).
   - Para adicionar ao PATH:
     - Pesquise por “Variáveis de Ambiente” no Windows.
     - Edite a variável “Path” em “Variáveis do Sistema” ou “Variáveis do Usuário” e adicione o diretório contendo `natpmpc.exe`.
   - Verifique executando:
     ```
     natpmpc
     ```
     Se não houver erro de “comando não encontrado”, está corretamente instalado.
4. **Alternativa**:
   - Se o `port-checker.py` lida com a detecção de porta sem o `natpmpc` (ex.: usando uma API da VPN), você não precisa do `natpmpc`. O script exibirá um aviso se o `natpmpc` estiver ausente, mas continuará se o `port-checker.py` funcionar.

### 4. Configurar o qBittorrent
1. **Instalar o qBittorrent**:
   - Baixe e instale o qBittorrent em [qbittorrent.org](https://www.qbittorrent.org/download).
2. **Ativar a Interface Web**:
   - Abra o qBittorrent e vá para `Ferramentas > Preferências > Interface Web`.
   - Marque “Ativar a Interface Web”.
   - Anote o host (ex.: `http://localhost:8080`), nome de usuário e senha.
   - Certifique-se de que o qBittorrent está em execução ao executar o script.
3. **Testar o Acesso à Interface Web**:
   - Abra um navegador e acesse a Interface Web (ex.: `http://localhost:8080`).
   - Faça login com seu nome de usuário e senha para confirmar que está funcionando.

### 5. Configurar o port-checker.py
- Certifique-se de que o `port-checker.py` está no mesmo diretório do `qbittorrent_port_updater.py`.
- Verifique se ele funciona no Windows executando:
  ```
  python port-checker.py
  ```
- Ele deve exibir algo como `The forwarded port is: 60661`.
- Se o `port-checker.py` usa o `natpmpc`, certifique-se de que o `natpmpc.exe` está instalado (veja a etapa 3).
- Se ele usa uma API da VPN ou outro método, confirme que o cliente VPN está em execução e configurado para redirecionamento de porta.

### 6. Configurar a VPN
- Certifique-se de que sua VPN (ex.: ProtonVPN) está instalada e em execução no Windows.
- Ative o NAT-PMP ou redirecionamento de porta nas configurações do cliente VPN (consulte a documentação da sua VPN).
- Teste o redirecionamento de porta executando o `port-checker.py` enquanto conectado à VPN.

## Executando o Script
1. **Colocar os Scripts**:
   - Salve `qbittorrent_port_updater.py` e `port-checker.py` em um diretório (ex.: `C:\Users\SeuNome\wg-port-checker`).
2. **Executar o Script**:
   - Abra o Prompt de Comando ou PowerShell e navegue até o diretório:
     ```
     cd C:\Users\SeuNome\wg-port-checker
     ```
   - Execute o script:
     ```
     python qbittorrent_port_updater.py
     ```
   - Se `python` não funcionar, tente:
     ```
     py qbittorrent_port_updater.py
     ```
3. **Primeira Execução**:
   - Se não houver um arquivo `.env`, o script solicitará o host, nome de usuário e senha da Interface Web do qBittorrent.
   - Esses dados são salvos no arquivo `.env` para execuções futuras.
   - Para redefinir as credenciais, delete o arquivo `.env` e execute o script novamente.
4. **Comportamento Esperado**:
   - O script verifica a porta redirecionada da VPN a cada 45 segundos usando o `port-checker.py`.
   - Compara a porta redirecionada com a porta atual do qBittorrent e atualiza o qBittorrent se houver diferença.
   - Os logs mostram carimbos de data/hora, portas detectadas, porta do qBittorrent e resultados das atualizações.

## Exemplo de Saída
```
Este script usa port-checker.py para detectar a porta redirecionada da VPN WireGuard e atualiza o qBittorrent.
Certifique-se de que port-checker.py está no mesmo diretório e que você está conectado à VPN.
Credenciais carregadas do arquivo .env.
Executando em loop para verificar a porta a cada 45 segundos. Pressione Ctrl+C para parar.

[2025-10-24 15:45:00] Iniciando nova iteração do loop
[2025-10-24 15:45:00] natpmpc não encontrado. Certifique-se de que está instalado ou verifique se port-checker.py lida com a detecção de porta independentemente.
[2025-10-24 15:45:00] Porta redirecionada detectada: 60661
[2025-10-24 15:45:00] Porta atual do qBittorrent: 12345
[2025-10-24 15:45:00] Diferença de porta detectada. Porta redirecionada: 60661, Porta do qBittorrent: 12345
[2025-10-24 15:45:00] Porta de escuta do qBittorrent definida com sucesso para 60661
[2025-10-24 15:45:00] Porta do qBittorrent atualizada de 12345 para 60661
```

## Solução de Problemas
1. **Falha no port-checker.py**:
   - Execute `python port-checker.py` para verificar se ele exibe `The forwarded port is: <porta>`.
   - Se ele depende do `natpmpc`, certifique-se de que o `natpmpc.exe` está instalado e no PATH.
   - Verifique as configurações da VPN para redirecionamento de porta.

2. **Erros no qBittorrent**:
   - Se aparecer `qBittorrent login failed` ou `Error communicating with qBittorrent`, verifique:
     - A Interface Web do qBittorrent está ativada e em execução.
     - O host, nome de usuário e senha no arquivo `.env` estão corretos.
     - Delete o arquivo `.env` e execute novamente para reinserir as credenciais.

3. **natpmpc Não Encontrado**:
   - Se o `port-checker.py` não requer o `natpmpc`, ignore o aviso.
   - Caso contrário, instale o `natpmpc` conforme descrito na etapa 3 ou modifique o `port-checker.py` para usar uma API da VPN.

4. **Problemas com a VPN**:
   - Certifique-se de que a VPN está conectada e o NAT-PMP/redirecionamento de porta está ativado.
   - Teste com o `port-checker.py` ou execute manualmente `natpmpc -g 10.2.0.1 -a 1 0 udp 60` (se instalado).

5. **Problemas com o Comando Python**:
   - Se `python` falhar, tente `py` ou `python3`.
   - Verifique se o Python está no PATH executando `python --version`.

## Notas
- **Segurança**: O arquivo `.env` armazena as credenciais do qBittorrent em texto puro. Mantenha-o seguro e exclua-o de sistemas de controle de versão (ex.: adicione `.env` ao `.gitignore`).
- **Estabilidade da Porta da VPN**: Algumas VPNs (ex.: ProtonVPN) podem reutilizar a mesma porta a menos que a conexão seja reiniciada. O script verifica a porta do qBittorrent em cada iteração para lidar com alterações externas.
- **Modificações**: Se o `port-checker.py` lida com a detecção de porta sem o `natpmpc`, você pode remover a chamada ao `renew_natpmp_mapping()` comentando a linha no script:
  ```python
  # renew_natpmp_mapping()  # Ignorado, assumindo que port-checker.py lida com a detecção de porta
  ```

Para assistência adicional, compartilhe a saída do console e detalhes sobre sua configuração (ex.: provedor de VPN, versão do qBittorrent, versão do Python).






# qBittorrent Port Updater

This project contains a Python script (`qbittorrent_port_updater.py`) that detects the forwarded port from a WireGuard VPN (e.g., ProtonVPN) using `port-checker.py` and updates the qBittorrent listening port to match it. The script runs in a loop, checking the port every 45 seconds and updating qBittorrent if necessary. This README provides instructions for setting up and running the script on **Windows**.

## Prerequisites

Before running the script, ensure you have the following:

- **Python 3.x**: Version 3.9 or later recommended.
- **qBittorrent**: Installed with the Web UI enabled.
- **WireGuard VPN**: Configured with NAT-PMP or port forwarding enabled (e.g., ProtonVPN).
- **port-checker.py**: A script that detects the forwarded VPN port and outputs `The forwarded port is: <port>`.

## Installation on Windows

Follow these steps to install the dependencies and run the script on Windows.

### 1. Install Python
1. **Download Python**:
   - Visit [python.org](https://www.python.org/downloads/windows/) or install via the Microsoft Store.
   - Choose Python 3.9 or later (e.g., Python 3.11).
2. **Install Python**:
   - Run the installer.
   - Check the box for **"Add Python to PATH"** during installation.
   - Verify installation by opening a Command Prompt or PowerShell and running:
     ```
     python --version
     ```
     You should see the Python version (e.g., `Python 3.11.0`).
3. **Alternative Command**:
   - If `python` doesn’t work, try `py` or `python3`. The script uses `sys.executable` to handle this automatically.

### 2. Install Required Python Libraries
The script requires the `requests` library. The `configparser` and `pathlib` libraries are included in Python’s standard library.

1. Open a Command Prompt or PowerShell.
2. Install `requests` using pip:
   ```
   pip install requests
   ```
3. Verify installation:
   ```
   pip show requests
   ```
   You should see details about the installed `requests` package.

### 3. Install natpmpc (Optional)
The script calls `natpmpc` to renew NAT-PMP mappings, but this step is only required if your `port-checker.py` script depends on `natpmpc`. If `port-checker.py` detects the port independently (e.g., via a VPN API), you can skip this step.

1. **Download libnatpmp**:
   - Visit [miniupnp.free.fr](http://miniupnp.free.fr/libnatpmp.html) and download the `libnatpmp` source code.
2. **Compile natpmpc**:
   - Install a C compiler like [MinGW](http://www.mingw.org/) or [MSYS2](https://www.msys2.org/).
   - In MSYS2, install dependencies:
     ```
     pacman -S mingw-w64-x86_64-gcc
     ```
   - Extract the `libnatpmp` source, navigate to the directory, and compile:
     ```
     make
     ```
   - This generates `natpmpc.exe`.
3. **Add natpmpc to PATH**:
   - Copy `natpmpc.exe` to the same directory as `qbittorrent_port_updater.py` or to a directory in your system’s PATH (e.g., `C:\Windows`).
   - To add to PATH:
     - Search for “Environment Variables” in Windows.
     - Edit the “Path” variable in “System Variables” or “User Variables” and add the directory containing `natpmpc.exe`.
   - Verify by running:
     ```
     natpmpc
     ```
     If it runs without a “command not found” error, it’s correctly installed.
4. **Alternative**:
   - If `port-checker.py` handles port detection without `natpmpc` (e.g., using a VPN API), you don’t need `natpmpc`. The script will log a warning if `natpmpc` is missing but continue if `port-checker.py` works.

### 4. Set Up qBittorrent
1. **Install qBittorrent**:
   - Download and install qBittorrent from [qbittorrent.org](https://www.qbittorrent.org/download).
2. **Enable Web UI**:
   - Open qBittorrent and go to `Tools > Preferences > Web UI`.
   - Check “Enable the Web UI”.
   - Note the host (e.g., `http://localhost:8080`), username, and password.
   - Ensure qBittorrent is running when you execute the script.
3. **Test Web UI Access**:
   - Open a browser and navigate to the Web UI (e.g., `http://localhost:8080`).
   - Log in with your username and password to confirm it’s working.

### 5. Set Up port-checker.py
- Ensure `port-checker.py` is in the same directory as `qbittorrent_port_updater.py`.
- Verify it works on Windows by running:
  ```
  python port-checker.py
  ```
- It should output something like `The forwarded port is: 60661`.
- If `port-checker.py` uses `natpmpc`, ensure `natpmpc.exe` is installed (see step 3).
- If it uses a VPN API or another method, confirm your VPN client is running and configured for port forwarding.

### 6. Configure the VPN
- Ensure your VPN (e.g., ProtonVPN) is installed and running on Windows.
- Enable NAT-PMP or port forwarding in the VPN client settings (refer to your VPN’s documentation).
- Test port forwarding by running `port-checker.py` while connected to the VPN.

## Running the Script
1. **Place Scripts**:
   - Save `qbittorrent_port_updater.py` and `port-checker.py` in a directory (e.g., `C:\Users\YourName\wg-port-checker`).
2. **Run the Script**:
   - Open Command Prompt or PowerShell and navigate to the directory:
     ```
     cd C:\Users\YourName\wg-port-checker
     ```
   - Run the script:
     ```
     python qbittorrent_port_updater.py
     ```
   - If `python` doesn’t work, try:
     ```
     py qbittorrent_port_updater.py
     ```
3. **First Run**:
   - If no `.env` file exists, the script will prompt for qBittorrent’s Web UI host, username, and password.
   - These are saved to `.env` for future runs.
   - To reset credentials, delete the `.env` file and rerun the script.
4. **Expected Behavior**:
   - The script checks the VPN’s forwarded port every 45 seconds using `port-checker.py`.
   - It compares the forwarded port to qBittorrent’s current port and updates qBittorrent if they differ.
   - Logs show timestamps, detected ports, qBittorrent’s port, and update results.

## Example Output
```
This script uses port-checker.py to detect the forwarded WireGuard port and updates qBittorrent.
Ensure port-checker.py is in the same directory and you are connected to the VPN.
Loaded credentials from .env file.
Running in loop to renew the port every 45 seconds. Press Ctrl+C to stop.

[2025-10-24 15:45:00] Starting new loop iteration
[2025-10-24 15:45:00] natpmpc not found. Ensure it is installed or verify port-checker.py handles port detection independently.
[2025-10-24 15:45:00] Detected forwarded port: 60661
[2025-10-24 15:45:00] Current qBittorrent port: 12345
[2025-10-24 15:45:00] Port mismatch detected. Forwarded port: 60661, qBittorrent port: 12345
[2025-10-24 15:45:00] Successfully set qBittorrent listening port to 60661
[2025-10-24 15:45:00] qBittorrent port updated from 12345 to 60661
```

## Troubleshooting
1. **port-checker.py Fails**:
   - Run `python port-checker.py` to verify it outputs `The forwarded port is: <port>`.
   - If it depends on `natpmpc`, ensure `natpmpc.exe` is installed and in PATH.
   - Check VPN settings for port forwarding.

2. **qBittorrent Errors**:
   - If you see `qBittorrent login failed` or `Error communicating with qBittorrent`, verify:
     - qBittorrent Web UI is enabled and running.
     - Host, username, and password in `.env` are correct.
     - Delete `.env` and rerun to re-prompt for credentials.

3. **natpmpc Not Found**:
   - If `port-checker.py` doesn’t require `natpmpc`, ignore the warning.
   - Otherwise, install `natpmpc` as described in step 3 or modify `port-checker.py` to use a VPN API.

4. **VPN Issues**:
   - Ensure the VPN is connected and NAT-PMP/port forwarding is enabled.
   - Test with `port-checker.py` or manually run `natpmpc -g 10.2.0.1 -a 1 0 udp 60` (if installed).

5. **Python Command Issues**:
   - If `python` fails, try `py` or `python3`.
   - Verify Python is in PATH by running `python --version`.

## Notes
- **Security**: The `.env` file stores qBittorrent credentials in plain text. Keep it secure and exclude it from version control (e.g., add `.env` to `.gitignore`).
- **VPN Port Stability**: Some VPNs (e.g., ProtonVPN) may reuse the same port unless the connection resets. The script checks qBittorrent’s port every iteration to handle external changes.
- **Modifications**: If `port-checker.py` handles port detection without `natpmpc`, you can remove the `renew_natpmp_mapping()` call in the script by commenting it out:
  ```python
  # renew_natpmp_mapping()  # Skipped, assuming port-checker.py handles port detection
  ```

For further assistance, share the console output and details about your setup (e.g., VPN provider, qBittorrent version, Python version).
