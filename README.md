Django Swift Direct
===================

Direct Uploads to OpenStack Swift using CORS

![Screenshot](/screenshot.png)

Using the tempurl middleware

Example - Template Tags
-----------------------

    {% load swift_direct %}

### Basic Template Tag

    {% swift_direct %}

### Upload to folder

    {% swift_direct upload_to='documents/uploaded' %}

### Upload to folder with set filename

    {% swift_direct upload_to='documents/uploaded' filename='force_filename' %}

### Include CSS

    {% swift_direct_css %}

### Include Javascript

    {% swift_direct_js %}

Example - Forms
-----------------------

    from django.forms import Form
    from swift_direct.fields import SwiftDirectField


    class ExampleForm(Form):
        image = SwiftDirectField(upload_to='images/%Y/%m/%d/')
        document = SwiftDirectField(upload_to='documents/%Y/%m/%d/')

* * *

    {% extends "base.html" %}

    {% block post_style %}
        {{ form.media.css }}
    {% endblock %}

    {% block content %}
        <div class="well">
            <form method="POST">
                {% csrf_token %}
                {{ form }}
                <button type="submit">Submit!</button>
            </form>
        </div>
    {% endblock content %}

    {% block post_script %}
        {{ form.media.js }}
    {% endblock %}

