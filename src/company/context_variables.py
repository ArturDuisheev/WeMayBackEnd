from core.env_reader import env


def env_variables(request):
    return {'GOOGLE_CLIENT_ID': env('GOOGLE_CLIENT_ID'),
            'BASE_URL': env('BASE_URL'),
            'FACEBOOK_APP_ID': env('FACEBOOK_APP_ID')}
