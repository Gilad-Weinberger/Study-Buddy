from django.core.management.base import BaseCommand
from django.contrib.auth.management.commands import createsuperuser

class Command(createsuperuser.Command):
    help = 'Create a superuser account.'

    def add_arguments(self, parser):
        super().add_arguments(parser)
        # Add an argument for the username
        parser.add_argument(
            '--username',
            dest='username',
            default=None,
            help='Specifies the username for the superuser.',
        )

    def get_input_data(self, field, message, default=None):
        if field == 'username':
            username = self.options.get('username')
            if username:
                return username
        return super().get_input_data(field, message, default)

    def handle(self, *args, **options):
        # Check if the username was provided, otherwise prompt for it
        if not options['username']:
            options['username'] = input('Username: ')

        super().handle(*args, **options)
