import socket
import errno
import datetime

from collections import defaultdict

from django.db.models import F
from django.views import generic
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth import authenticate
from django.utils import timezone

from .models import Button, AccessToken


class IndexView(generic.ListView):
    template_name = 'lights/index.html'
    context_object_name = 'session_dict'

    def get_queryset(self):
        divider_dict = defaultdict(list)

        authenticated = False
        token = self.request.session.get('token')
        if token is not None:
            try:
                matched_token = AccessToken.objects.get(pk=token)
            except AccessToken.DoesNotExist:
                self.request.session.pop('token')
            else:
                timezone.activate(timezone.utc)
                if matched_token.expiry_date > timezone.now():
                    authenticated = True
                else:
                    self.request.session.pop('token')
                    matched_token.delete()

        session_dict = {'authenticated': authenticated, 'divider_dict': divider_dict}

        for button in Button.objects.all():
            divider_dict[button.parent_divider.divider_name].append(button)
        return session_dict


def check_auth(request):
    authenticated = False
    token = request.session.get('token')
    if token is not None:
        try:
            matched_token = AccessToken.objects.get(pk=token)
        except AccessToken.DoesNotExist:
            request.session.pop('token')
        else:
            timezone.activate(timezone.utc)
            if matched_token.expiry_date > timezone.now():
                authenticated = True
            else:
                request.session.pop('token')
                matched_token.delete()
    return authenticated


def status_request(request):
    status_update = '1'

    if check_auth(request):
        master_response = send_to_master(status_update).decode()

        data = {
            'master_response': master_response
        }
        return JsonResponse(data)
    return HttpResponseForbidden


def verify_token(request):
    requested_token = request.POST['token']
    try:
        matched_token = AccessToken.objects.get(pk=requested_token)
    except AccessToken.DoesNotExist:
        response = 'bad request'
    else:
        if matched_token.in_use:
            response = 'bad request'
        else:
            matched_token.in_use = True
            matched_token.save()

            time_difference = matched_token.expiry_date - timezone.now()
            request.session['token'] = matched_token.token
            request.session.set_expiry(time_difference.total_seconds())

            response = 'success'

    data = {
        'response': response
    }
    return JsonResponse(data)


def verify_password(request):
    if check_auth(request):
        password_raw = request.POST['password']
        user = authenticate(request, username='michael', password=password_raw)
        if user is not None:
            token = AccessToken.objects.create()
            access_token = token.token
        else:
            access_token = 'bad request'

        data = {
            'access_token': access_token
        }
        return JsonResponse(data)
    return HttpResponseForbidden


def modify_life(request):
    if check_auth(request):
        hours_to_add = request.POST['hours']
        access_token = request.POST['access_token']
        if hours_to_add.isdigit() and int(hours_to_add) > 0:
            hours_to_add = int(hours_to_add)
            try:
                token = AccessToken.objects.get(pk=access_token)
                token.expiry_date = F('expiry_date') + datetime.timedelta(hours=hours_to_add)
                token.save()
            except AccessToken.DoesNotExist:
                response = 'bad request'
            else:
                response = 'success'
        else:
            response = 'bad request'

        data = {
            'response': response
        }
        return JsonResponse(data)
    return HttpResponseForbidden


def button_pressed(request):
    if check_auth(request):
        button_id = request.POST.get('button_id', None)
        try:
            button = Button.objects.get(pk=button_id)
        except Button.DoesNotExist:
            master_response = b'bad request'
            related_color = None
        else:
            button_message = button.message_string
            master_response = send_to_master(button_message)
            related_color = button.related_color
            svg_image = button.svg_image

        data = {
            'master_response': master_response.decode(),
            'related_color': related_color,
            'svg_image': svg_image
        }
        return JsonResponse(data)
    return HttpResponseForbidden


def rgb_message(request):
    if check_auth(request):
        rgb_str = request.POST.get('color', None)
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
    return HttpResponseForbidden


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
