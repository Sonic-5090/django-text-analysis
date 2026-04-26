"""Views for the analyzer app."""
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .utils import analyze_message


def index(request):
    """Render the main page."""
    example_messages = [
        "Hey bro, what's up? Miss you man!",
        "Dear Mr. Smith, I would like to discuss the project details. Regards.",
        "I love you so much! Can't wait to see you tonight 💕",
        "Excuse me, could you please help me with this?",
        "Hey, do you want to grab lunch sometime?",
    ]
    context = {
        'examples': example_messages,
    }
    return render(request, 'index.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def analyze(request):
    """Analyze the message and return predictions."""
    try:
        data = json.loads(request.body)
        message = data.get('message', '').strip()
        
        if not message:
            return JsonResponse({'error': 'Please enter a message'}, status=400)
        
        result = analyze_message(message)
        
        return JsonResponse(result)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)