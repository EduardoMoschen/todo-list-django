# To-Do List em Django

Bem-vindo à aplicação To-Do List! Esta é uma aplicação simples de lista de tarefas construída em Django.

## Visão geral

A aplicação permite que os usuários gerenciem uas tarefas diárias de forma fácil e organizada. Os usuários podem adicioanr, concluir e excluir tarefas de suas listas, mas para isso é necessário se registrar.

## Requisitos

Para a execução, você precisará do seguinte:

- Python 3.8 ou superior
- Django 4.0 ou superior


## Instalação

1. Clone este repositório para o seu sistema local:

    `
    git clone https://github.com/EduardoMoschen/to-do-list-django.git
    `

2. Instale as dependências:

    `
    pip install -r requirements.txt
    `

3. Aplique as migrações do banco de dados:

    `
    python manage.py migrate
    `

4. Execute o servidor de desenvolvimento:

    `
    python manage.py runserver
    `

5. Agora você já pode acessar a aplicação :rocket:

    `
    http://127.0.0.1:8000/
    `

## Uso

O To-Do List é fácil de usar:

1. Acesse a aplicação em `http://127.0.0.1:8000/`

2. Para começar a usar, clique em 'Register' na página inicial.

3. Preencha os campos com um 'username' e a digite uma senha - precisará repetir a senha.

4. Após o registro, você já poderá criar novas tarefas clicando em 'New Task', onde irá pedir o nome dela e a descrição dela. Ao finalizar, basta clicar em 'Submit'.

5. A partir da tarefa criada anteriormente, você poderá decidir se quer adicionar outras, concluir ou excluir. Se quiser concluir, clique no nome e marque a opção 'complete'. Caso queira excluir, clique no 'x' que está à direita do nome.

6. Caso tenha mais que uma tarefa e deseja definir prioridades entre elas, há um símbolo com 'três pontos' ao lado da opção de excluir. Este símbolo serve para 'arrastar' as tarefas, como um *drag-and-drop*.


## Contribuindo

Se você quiser contribuir para o desenvolvimento desta aplicação, siga os passos abaixo:

1. Faça um fork deste repositório no GitHub.

2. Crie uma branch para a sua contribuição:

    `
    git checkout -n minha-contribuicao
    `

3. Faça suas alterações e commit:

    `
    git commit -m "Minha contribuição"
    `

4. Envie suas alterações para o seu fork:

    `
    git push origin minha-contribuição
    `

5. Abra um Pull Request no repositório original para revisão.

# Licença

Esta aplicação é distribuída sob a licença **MIT**.