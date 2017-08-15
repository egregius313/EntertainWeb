import socket
import errno

from collections import defaultdict

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
        master_response = b'bad request'
        related_color = None
    else:
        button_message = button.message_string
        master_response = send_to_master(button_message)
        related_color = button.related_color

    data = {
        'master_response': master_response.decode(),
        'related_color': related_color
    }
    return JsonResponse(data)


def rgb_message(rgb_encoded):
    rgb_str = rgb_encoded.POST.get('color', None)
    if len(rgb_str) is 11:
        r = rgb_str[:3]
        g = rgb_str[4:7]
        b = rgb_str[8:11]

        if r.isdigit() and g.isdigit() and b.isdigit():
            if 0 <= (int(r) and int(g) and int(b)) <= 255:
                master_response = send_to_master('c:' + rgb_str)
            else:
                master_response = b'bad request'
        else:
            master_response = b'bad request'
    else:
        master_response = b'bad request'

    data = {
        'master_response': master_response.decode()
    }
    return JsonResponse(data)


def send_to_master(message_str):
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
                client_socket.sendall(bytes(message_str, encoding='UTF-8'))
                client_response = client_socket.recv(1024)
        try:
            server_socket.shutdown(socket.SHUT_RDWR)
        except OSError as e:
            if e.errno != errno.ENOTCONN:
                raise
    return client_response
