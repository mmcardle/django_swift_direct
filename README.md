Django Swift Direct
===================

Direct Uploads to OpenStack Swift using CORS

![Screenshot](/screenshot.png)

Using the tempurl middleware

Example
-------

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


TODO
----

* Support SLO large objects
