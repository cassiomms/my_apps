my_apps
=======

Intermed Commander
=======

--> Informações

Site da competição: http://aisandbox.com/



--> Configurando o ambiente

Baixar e instalar http://aisandbox.com/AiGD-TheAiSandbox-0.20.5-win32-bin.exe

Baixar http://aisandbox.com/AiGD-CaptureTheFlag-1.5-sdk.zip

Instalar EGit no eclipse

Clonar o repositório com a URL https://github.com/cassiomms/my_apps.git (importando os projetos)

Nesse ponto, já é pra ter um projeto PyDev no eclipse com o Intermed Commander!

Copiar a pasta da api (dentro da SDK baixada) para o /src do projeto (só para o eclipse não reclamar dos imports)



--> Rodando o projeto no AI Sandbox


Copiar o arquivo do Intermed Commander (intermed_bot.py) para a pasta da SDK

Mudar os bots no arquivo simulate.py, variável global defaults

Ex: defaults = ['examples.BalancedCommander', 'intermed_bot.IntermedCommander']



