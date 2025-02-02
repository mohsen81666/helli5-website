from django.shortcuts import render

import requests
from datetime import datetime
import jdatetime
import xmltodict

from helli5.decorators import has_perm
from helli5 import settings
from loginApp.models import StudentProfile


def elearning(request):
    context = {
        'moodle_url': 'https://lms.' + settings.SITE_URL,
        'adobe_connect_url': 'https://class.' + settings.SITE_URL,
        'telegram_url': 'https://t.me/allamehelli5',
        'aparat_url': 'https://www.aparat.com/allamehelli5',
    }
    return render(request, 'elearning.html', context)


@has_perm('loginApp.check_online_classes')
def check_online_classes(request):
    classes = {
        '10': {
            'R': {
                '101': {
                    'sco-id': '75708',
                    'url_path': '/r101',
                },
                '102': {
                    'sco-id': '69026',
                    'url_path': '/r102',
                },
                'all': {
                    'sco-id': '75716',
                    'url_path': '/r10',
                },
            },
            'T': {
                '103': {
                    'sco-id': '67205',
                    'url_path': '/t103',
                },
            },
            'E': {
                '105': {
                    'sco-id': '67800',
                    'url_path': '/e105'
                },
            },
            'RTE': {
                'all': {
                    'sco-id': '37506',
                    'url_path': '/e10'
                },
            }
        },
        '11': {
            'R': {
                '111': {
                    'sco-id': '35124',
                    'url_path': '/c111'
                },
                '112': {
                    'sco-id': '35037',
                    'url_path': '/c112'
                },
                'all': {
                    'sco-id': '37458',
                    'url_path': '/r11'
                },
            },
            'T': {
                '113': {
                    'sco-id': '35082',
                    'url_path': '/c113'
                },
                '114': {
                    'sco-id': '35090',
                    'url_path': '/c114'
                },
                'all': {
                    'sco-id': '37447',
                    'url_path': '/r4qwdibp3oyt'
                },
            },
            'E': {
                '115': {
                    'sco-id': '35098',
                    'url_path': '/c115'
                },
            },
            'RTE': {
                'all': {
                    'sco-id': '42072',
                    'url_path': '/f11'
                },
            }
        },
        '12': {
            'R': {
                '121': {
                    'sco-id': '35169',
                    'url_path': '/c121'
                },
                '122': {
                    'sco-id': '35181',
                    'url_path': '/c122'
                },
                'all': {
                    'sco-id': '37599',
                    'url_path': '/r12'
                },
            },
            'T': {
                '123': {
                    'sco-id': '35189',
                    'url_path': '/c123'
                },
            },
            'E': {
            },
            'RTE': {
                'all': {
                    'sco-id': '42063',
                    'url_path': '/f12'
                },
            }
        },

        'E-All': {
            'sco-id': '68503',
            'url_path': '/e'
        },
    }
    class_times = {
        '1': { 'start': '8:15:00', 'end': '9:30:00'},
        '2': { 'start': '9:45:00', 'end': '11:00:00'},
        '3': { 'start': '11:15:00', 'end': '12:30:00'},
        '4': { 'start': '12:45:00', 'end': '14:00:00'},
    }

    request_date = request.GET.get('date')
    request_grade = request.GET.get('grade')
    request_field = request.GET.get('field')
    request_zang = request.GET.get('zang')
    if request_date is None or request_grade is None or request_field is None or request_zang is None:
        return render(request, 'pa_page.html', context={})

    cls = classes[request_grade][request_field]
    cls_date_jalali = datetime.strptime(request_date , '%Y/%m/%d')
    cls_date = jdatetime.date(cls_date_jalali.year, cls_date_jalali.month, cls_date_jalali.day).togregorian()
    cls_start = class_times[request_zang]['start']
    cls_end = class_times[request_zang]['end']


    # Authentication
    response = requests.get('https://class.allamehelli5edu.ir/api/xml?action=login' +
                            '&login=' + settings.ADOBE_CONNECT_USER +
                            '&password=' + settings.ADOBE_CONNECT_PASSWORD)
    response_content = xmltodict.parse(response.content)
    if response_content['results']['status']['@code'] == 'no-data':
        return render(request, 'pa_page.html', context={'error': 'Not Authenticated!'})
    breeze_session = response.cookies.get('BREEZESESSION')

    # Get Students
    students_query = (StudentProfile.objects
        .filter(grade=request_grade)
        .filter(active=True)
    )
    if request_field != 'RTE':  # if field specified
        students_query = (students_query
            .filter(field=request_field)
        )
    students = students_query.all()

    # Get meetings attendants(adobe-students)
    class_names = ""
    attendants = []
    for meeting in cls:
        xml_response = requests.get(
            'https://class.allamehelli5edu.ir/api/xml?action=report-meeting-attendance&sco-id=' + cls[meeting]['sco-id'] +
            '&' + generate_date_query_param(cls_date, cls_start, cls_end) +
            '&session=' + breeze_session)
        response_content = xmltodict.parse(xml_response.content)
        if response_content['results']['report-meeting-attendance']:
            class_names += '«' + response_content['results']['report-meeting-attendance']['row'][0]['sco-name'] + '»'
            for att in response_content['results']['report-meeting-attendance']['row']:
                attendants.append(att)

    checks = {}
    for student in students:
        id = student.student_id
        checks[id] = {
            'name': student.user.first_name,
            'family': student.user.last_name,
        }
        attendances = [att for att in attendants if 'login' in att and att['login'] == str(id)]
        attendances = sorted(attendances, key=lambda d: d['date-created'])
        if len(attendances) == 0:
            checks[id]['check'] = False
        else:
            checks[id]['check'] = True

            checks[id]['first_in'] = datetime.strptime(
                    attendances[0]['date-created'].split('T')[1].split('.')[0],
                    '%H:%M:%S')

            if 'date-end' in attendances[len(attendances)-1].keys():
                checks[id]['last_out'] = datetime.strptime(
                        attendances[len(attendances)-1]['date-end'].split('T')[1].split('.')[0],
                        '%H:%M:%S')
            else:
                checks[id]['last_out'] = None

            interval = 0
            for att in attendances:
                att_start = datetime.fromisoformat(att['date-created']).replace(tzinfo=None)
                if 'date-end' in att.keys():
                    att_end = datetime.fromisoformat(att['date-end']).replace(tzinfo=None)
                else:
                    att_end = datetime.now().replace(tzinfo=None)
                interval += round((att_end - att_start).total_seconds() / 60)
            checks[id]['interval'] = interval

            checks[id]['attendance_no'] = len(attendances)

    return render(request, 'pa_page.html',
                  context = {
                      'class_names': class_names,
                      'checks': checks,
                    }
                )


def generate_date_query_param(cls_date, start_time, end_time):
    year = cls_date.year
    month = cls_date.month
    day = cls_date.day
    if day % 10 == day:
        day = '0' + str(day)
    if month % 10 == month:
        month = '0' + str(month)
    date_query = (
        'filter-gt-date-created=' + str(year) + '-' + str(month) + '-' + str(day) + 'T' + start_time +
        '&filter-lt-date-created=' + str(year) + '-' + str(month) + '-' + str(day) + 'T' + end_time
    )
    return date_query
