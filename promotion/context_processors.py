from promotion.models import JoinApplication


def get_application_count():
    return len(JoinApplication.objects.filter(is_rejected=False, is_approved=False))


# function to add application_list notification dot to all pages

def application_processor(request):
    application_count = get_application_count()
    return {'application_count': application_count}
