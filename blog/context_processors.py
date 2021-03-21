from blog.forms import SubscriberForm


def subscriber_form(request):
    return {'email_subscribe_form': SubscriberForm()}
