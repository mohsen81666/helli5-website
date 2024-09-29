from django.template.defaulttags import register

@register.filter
def persian_month_name(month_no):
    month_names = {
        1: 'فروردین', 2: 'اردیبهشت', 3: 'خرداد',
        4: 'تیر', 5: 'مرداد', 6: 'شهریور',
        7: 'مهر', 8: 'آبان', 9: 'آذر',
        10: 'دی', 11: 'بهمن', 12: 'اسفند'
    }
    return month_names.get(month_no)  # using .get to return none if the key is absent