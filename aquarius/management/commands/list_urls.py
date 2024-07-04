from django.core.management.base import BaseCommand
from django.urls import get_resolver, URLPattern, URLResolver
from django.conf import settings

def list_urls(lis, acc=None):
    if acc is None:
        acc = []
    for entry in lis:
        if isinstance(entry, URLPattern):
            if entry.name:
                acc.append(entry.name)
        elif isinstance(entry, URLResolver):
            list_urls(entry.url_patterns, acc)
    return acc

class Command(BaseCommand):
    help = 'List all named URLs in the project'

    def handle(self, *args, **kwargs):
        print(settings.UNFOLD)
        resolver = get_resolver()
        url_names = list_urls(resolver.url_patterns)
        for name in url_names:
            self.stdout.write(name)