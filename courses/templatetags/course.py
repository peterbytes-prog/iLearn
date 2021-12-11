from django import template
from django.urls import resolve
from django.urls import reverse_lazy
register = template.Library()

@register.filter
def model_name(obj):
    try:
        return obj._meta.model_name
    except AttributeError:
        return None
@register.filter
def is_instructor(obj):
    try:
        if obj.is_superuser or obj.instructor:
            return True
        else:
            return False
    except:

        return None

@register.filter
def get_name(obj):
    return obj.get_full_name() or obj.username

@register.filter
def is_current(request,name):
    current_url = resolve(request.path_info).url_name
    nav = {
    'home':['course_list','course_detail'],
    'my_courses':['student_course_detail','student_registration','student_enroll_course',"student_course_list",'student_course_detail_module','course_chat_room','student_course_a_assignment_detail','student_course_assignment_detail','test_page','test_review_page'],
    'my_submitted_courses':[
        'manage_course_list',
        'course_edit',
        'course_delete',
        'course_module_update',
        'module_content_create',
        'module_content_update',
        'module_content_delete',
        'module_content_list',
        'course_list_subject',
        'course_assignment_update',
    ],
    'course_create':['course_create'],
    'profile-detail':['profile-detail']
    }

    if current_url in nav.get(name,[]):
        return True
    else:
        return False

@register.filter
def render_choice(item,attempt=False):
    return item.render(attempt)
