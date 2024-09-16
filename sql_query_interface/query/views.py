# query/views.py

from django.shortcuts import render
from django.db import connection, DatabaseError
from .forms import SQLQueryForm


def execute_query(query):
    with connection.cursor() as cursor:
        try:
            cursor.execute(query)
            if query.strip().upper().startswith("SELECT"):
                columns = [col[0] for col in cursor.description]
                results = cursor.fetchall()
                return columns, results, None
            else:
                return None, None, None
        except DatabaseError as e:
            return None, None, str(e)


def query_view(request):
    form = SQLQueryForm()
    results = None
    columns = None
    error = None
    executed_query = None
    if request.method == 'POST':
        form = SQLQueryForm(request.POST)
        if form.is_valid():
            executed_query = form.cleaned_data['query']
            columns, results, error = execute_query(executed_query)
    return render(request, 'query/query.html', {
        'form': form,
        'results': results,
        'columns': columns,
        'error': error,
        'executed_query': executed_query
    })
