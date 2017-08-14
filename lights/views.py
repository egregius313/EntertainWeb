import socket
from collections import defaultdict

import errno
from django.views import generic
from django.http import JsonResponse

from .models import Button


class IndexView(generic.ListView):
    template_name = 'lights/index.html'
    context_object_name = 'divider_dict'

    def get_queryset(self):
        divider_dict = defaultdict(list)
        for button in Button.objects.all():
            divider_dict[button.parent_divider.divider_name].append(button)
        return divider_dict


def button_pressed(button_xhttp):
    button_id = button_xhttp.POST.get('button_id', None)
    try:
        button = Button.objects.get(pk=button_id)
    except Button.DoesNotExist:
        client_response = b'bad request'
    else:
        button_message = button.message_string

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', 8493))

        server_socket.settimeout(5)  # 5 seconds
        server_socket.listen(1)

        with server_socket:
            try:
                (client_socket, address) = server_socket.accept()
                print('%s connected' % address[0])
            except socket.timeout:
                client_response = b'timeout'
            else:
                with client_socket:
                    client_socket.sendall(bytes(button_message, encoding='UTF-8'))
                    client_response = client_socket.recv(1024)
            try:
                server_socket.shutdown(socket.SHUT_RDWR)
            except OSError as e:
                if e.errno != errno.ENOTCONN:
                    raise
    data = {
        'client_response': client_response.decode()
    }
    return JsonResponse(data)
