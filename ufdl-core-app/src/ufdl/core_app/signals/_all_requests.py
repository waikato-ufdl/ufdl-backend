from django.dispatch import Signal


all_requests = Signal(providing_args=['request'])
