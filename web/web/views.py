from django.shortcuts import render


def temp_view(request):
    return render(request, 'index.html')