from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import (CreateView, DeleteView, FormView,
                                       UpdateView)
from django.views.generic.list import ListView

from base.forms import PositionForm
from base.models import Task


class CustomLoginView(LoginView):
    """
    CustomLoginView estende a LoginView embutida do Django para personalizar o
    processo de login.

    Atributos:
        template_name (str): O nome do template a ser usado para renderizar a
        página de login.
        fields (str): Os campos a serem exibidos no formulário de login. Use
        '__all__' para exibir todos os campos.
        redirect_authenticated_user (bool): Se for True, redireciona o usuário
        para a URL de sucesso se ele já estiver autenticado.

    Métodos:
        get_success_url(): Retorna a URL para redirecionar o usuário após o
        login bem-sucedido.
    """

    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        """
        get_succsess_url() -> str

        Retorna  URL para redirecionar o usuário após o login bem-sucedido.

        Retorna:
            str: A URL para redirecionar o usuário após o login bem-sucedido.
        """
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    """
    RegisterPage é uma visualização baseada em classe que exibe o formulário de
    registro de usuário.

    Herda de:
        FormView: Exibe um formulário e processa os dados enviados pelo
        usuário.

    Atributos:
        template_name (str): O nome do template a ser usado para renderizar a
        página de registro.
        form_class (django.forms.Form): A classe do formulário de registro a
        ser exibido.
        redirect_authenticated_user (bool): Se for True, redireciona o usuário
        para a URL de sucesso se ele já estiver autenticado.
        success_url (django.urls.reverse_lazy): A URL para redirecionar o
        usuário após o registro bem-sucedido.

    Métodos:
        form_valid(form):
            Processa o formulário após ser validado.

            Parâmetros:
                form (django.forms.Form): O formulário preenchido pelo usuário.

            Retorna:
                django.http.HttpResponseRedirect: Redireciona para a URL de
                sucesso após o registro bem-sucedido.

        get(*args, **kwargs):
            Manipula uma solicitação GET para a visualização.

            Parâmetros:
                *args: Argumentos adicionais.
                **kwargs: Argumentos de palavras-chave adicionais.

            Retorna:
                django.http.HttpResponse: Resposta HTTP.
    """

    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        """
        Processa o formulário após ser validado.

        Parâmetros:
            form (django.forms.Form): O formulário preenchido pelo usuário.

        Retorna:
            django.http.HttpResponseRedirect: Redireciona para a URL de sucesso
            após o registro bem-sucedido.
        """

        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        """
        Manipula uma solicitação GET para a visualização.

        Parâmetros:
            *args: Argumentos adicionais.
            **kwargs: Argumentos de palavras-chave adicionais.

        Retorna:
            django.http.HttpResponse: Resposta HTTP.
        """

        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    """
    TaskList é uma visualização baseada em classe que exibe a lista de tarefas
    do usuário logado.

    Herda de:
        LoginRequiredMixin: Garante que o usuário esteja autenticado antes de
        acessar a visualização.
        ListView: Exibe uma lista de objetos em um modelo em uma página.

    Atributos:
        model (django.db.models.Model): O modelo que será utilizado para buscar
        as tarefas.
        context_object_name (str): O nome da variável do contexto que conterá
        os objetos do modelo a serem exibidos na página.

    Métodos:
        get_context_data(**kwargs):
            Retorna um dicionário contendo o contexto para renderizar o
            template.

            Parâmetros:
                **kwargs: Argumentos de palavras-chave adicionais.

            Retorna:
                dict: Um dicionário contendo o contexto para renderizar o
                template com as informações das tarefas do usuário.
    """

    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        """
        Retorna um dicionário contendo o contexto para renderizar o template.

        Parâmetros:
            **kwargs: Argumentos de palavras-chave adicionais.

        Retorna:
            dict: Um dicionário contendo o contexto para renderizar o template
            com as informações das tarefas do usuário.
        """

        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        # Caso não seja inserido no campo de busca, irá listar todas as tasks.
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input
            )

        context['search_input'] = search_input

        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    """
    TaskDetail é uma visualização baseada em classe que exibe os detalhes de
    uma tarefa específica.

    Herda de:
        LoginRequiredMixin: Garante que o usuário esteja autenticado antes de
        acessar a visualização.
        DetailView: Exibe os detalhes de um único objeto em um modelo em uma
        página.

    Atributos:
        model (django.db.models.Model): O modelo que será utilizado para buscar
        a tarefa.
        template_name (str): O nome do template a ser usado para renderizar a
        página de detalhes.
        context_object_name (str): O nome da variável do contexto que conterá o
        objeto do modelo a ser exibido na página.
    """

    model = Task
    template_name = 'base/task.html'
    context_object_name = 'tasks'


class TaskCreate(LoginRequiredMixin, CreateView):
    """
    TaskCreate é uma visualização baseada em classe que exibe um formulário
    para criar uma nova tarefa.

    Herda de:
        LoginRequiredMixin: Garante que o usuário esteja autenticado antes de
        acessar a visualização.
        CreateView: Exibe um formulário para criar um novo objeto em um modelo.

    Atributos:
        model (django.db.models.Model): O modelo que será utilizado para criar
        a tarefa.
        fields (list): Uma lista de campos do modelo que serão exibidos no
        formulário.
        success_url (django.urls.reverse_lazy): A URL para redirecionar o
        usuário após a criação bem-sucedida da tarefa.

    Métodos:
        form_valid(form):
            Processa o formulário após ser validado.

            Parâmetros:
                form (django.forms.Form): O formulário preenchido pelo usuário.

            Retorna:
                django.http.HttpResponseRedirect: Redireciona para a URL de
                sucesso após a criação bem-sucedida da tarefa.
    """

    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        """
        Processa o formulário após ser validado.

        Parâmetros:
            form (django.forms.Form): O formulário preenchido pelo usuário.

        Retorna:
            django.http.HttpResponseRedirect: Redireciona para a URL de sucesso
            após a criação bem-sucedida da tarefa.
        """

        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    """
    TaskUpdate é uma visualização baseada em classe que exibe um formulário
    para atualizar uma tarefa existente.

    Herda de:
        LoginRequiredMixin: Garante que o usuário esteja autenticado antes de
        acessar a visualização.
        UpdateView: Exibe um formulário para atualizar um objeto existente em
        um modelo.

    Atributos:
        model (django.db.models.Model): O modelo que será utilizado para buscar
        a tarefa a ser atualizada.
        fields (list): Uma lista de campos do modelo que serão exibidos no
        formulário para atualização.
        success_url (django.urls.reverse_lazy): A URL para redirecionar o
        usuário após a atualização bem-sucedida da tarefa.
    """

    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    """
    TaskDelete é uma visualização baseada em classe que exibe uma página de
    confirmação para excluir uma tarefa.

    Herda de:
        LoginRequiredMixin: Garante que o usuário esteja autenticado antes de
        acessar a visualização.
        DeleteView: Exibe uma página de confirmação para excluir um objeto em
        um modelo.

    Atributos:
        model (django.db.models.Model): O modelo que será utilizado para buscar
        a tarefa a ser excluída.
        fields (str): A string '__all__' que indica para usar todos os campos
        do modelo.
        success_url (django.urls.reverse_lazy): A URL para redirecionar o
        usuário após a exclusão bem-sucedida da tarefa.
        template_name (str): O nome do template a ser usado para renderizar a
        página de confirmação de exclusão.
    """

    model = Task
    fields = '__all__'
    success_url = reverse_lazy('tasks')
    template_name = 'base/task_delete.html'


class TaskReorder(View):

    """
    TaskReorder é uma visualização baseada em classe que processa a reordenação
    das tarefas do usuário.

    Herda de:
        View: Manipula as solicitações HTTP diretamente sem exibir um template.

    Métodos:
        post(request):
            Manipula uma solicitação POST para a visualização.

            Parâmetros:
                request (django.http.HttpRequest): A solicitação HTTP POST.

            Retorna:
                django.http.HttpResponseRedirect: Redireciona para a URL de
                lista de tarefas após a reordenação bem-sucedida.
    """

    def post(self, request):
        """
        Manipula uma solicitação POST para a visualização.

        Parâmetros:
            request (django.http.HttpRequest): A solicitação HTTP POST.

        Retorna:
            django.http.HttpResponseRedirect: Redireciona para a URL de lista
            de tarefas após a reordenação bem-sucedida.
        """

        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))
