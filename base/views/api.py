from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Task
from base.serializers import TodoSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status


@api_view(['get', 'post'])
def todo_api_list(request):
    if request.method == 'GET':
        tasks = Task.objects.all()
        serializer = TodoSerializer(
            instance=tasks,
            many=True,
            context={'request': request}
        )

        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = TodoSerializer(
            data=request.data,
            context={'request': request}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status.HTTP_201_CREATED
        )


@api_view(['get', 'patch', 'delete'])
def todo_api_detail(request, pk):
    task = get_object_or_404(
        Task.objects.all(),
        pk=pk
    )

    if request.method == 'GET':

        serializer = TodoSerializer(
            instance=task,
            many=False,
            context={'request': request}
        )

        return Response(serializer.data)

    elif request.method == 'PATCH':
        serializer = TodoSerializer(
            instance=task,
            data=request.data,
            many=False,
            context={'request': request},
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    elif request.method == 'DELETE':
        task.delete()

        return Response(status.HTTP_204_NO_CONTENT)
