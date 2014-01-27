Django Swift Direct
===================

Direct Uploads to OpenStack Swift using CORS

![Screenshot](/screenshot.png)

Using the tempurl middleware

Example - Template Tags
-----------------------

    {% load swift_direct %}

    <h3>Basic Template Tag</h3>

    {% swift_direct %}

    <h3>Upload to folder</h3>

    {% swift_direct upload_to='documents/uploaded' %}

    <h3>Upload to folder with set filename</h3>

    {% swift_direct upload_to='documents/uploaded' filename='force_filename' %}

    <h3>Include CSS</h3>

    {% swift_direct_css %}

    <h3>Include Javascript</h3>

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

