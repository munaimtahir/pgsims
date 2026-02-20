from django.shortcuts import render
from django.http import HttpResponse
from sims.logbook.forms import LogbookReviewForm

def test_crispy_view(request):
    """Test view to check crispy forms"""
    try:
        form = LogbookReviewForm()
        
        # Test template rendering
        template_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Crispy Forms Test</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-4">
        <h2>Crispy Forms Test</h2>
        
        {% load crispy_forms_tags %}
        
        <form method="post">
            {% csrf_token %}
            
            <p>Form has {{ form|length }} fields</p>
            
            <div class="mb-3">
                <h4>Testing overall_score field:</h4>
                {% if form.overall_score %}
                    {{ form.overall_score|as_crispy_field }}
                {% else %}
                    <p>overall_score field not found</p>
                {% endif %}
            </div>
            
            <div class="mb-3">
                <h4>Testing status field:</h4>
                {% if form.status %}
                    {{ form.status|as_crispy_field }}
                {% else %}
                    <p>status field not found</p>
                {% endif %}
            </div>
            
            <div class="mb-3">
                <h4>All form fields:</h4>
                <ul>
                {% for field_name, field in form.fields.items %}
                    <li>{{ field_name }}: {{ field|class_name }}</li>
                {% endfor %}
                </ul>
            </div>
            
        </form>
    </div>
</body>
</html>
        """
        
        from django.template import Template, Context
        template = Template(template_content)
        context = Context({'form': form})
        
        return HttpResponse(template.render(context))
        
    except Exception as e:
        import traceback
        error_info = traceback.format_exc()
        return HttpResponse(f"<h1>Error:</h1><pre>{error_info}</pre>")
