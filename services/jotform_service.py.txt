import os
import requests

API_KEY = os.environ.get('JOTFORM_API_KEY')
BASE_URL = 'https://api.jotform.com'


def list_forms():
    resp = requests.get(f'{BASE_URL}/user/forms', params={'apiKey': API_KEY})
    resp.raise_for_status()
    return resp.json().get('content', [])


def form_submissions(form_id):
    resp = requests.get(f'{BASE_URL}/form/{form_id}/submissions', params={'apiKey': API_KEY})
    resp.raise_for_status()
    return resp.json().get('content', [])


def convert_to_google(form_id):
    """Placeholder converting Jotform form to Google Form."""
    # Implementing full conversion requires Google Forms API
    # Here we just return a not implemented message
    return {
        'form_id': form_id,
        'status': 'not_implemented',
        'message': 'Conversion to Google Forms is not implemented.'
    }
