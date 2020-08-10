from django.dispatch import Signal

# Signal which is fired on all requests to the server
all_requests = Signal(providing_args=['request'])
