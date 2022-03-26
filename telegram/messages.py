class ErrorMessages:
    FORBIDDEN = 'شما اجازه دسترسی به این قسمت را ندارید'
    INVALID = 'مقدار ورودی شما معتبر نیست! طبق مثال زیر مقدار وارد کنید\n{example}'
    UNKNOWN = 'خطایی ناشناس در یکی از عملیات های اخیر رخ داد.\n{traceback}'
    EXISTS = 'این مقدار قبلا ثبت شده است.\n{value}'


class InfoMessages:
    WELCOME = 'خوش آمدید'
    ACCESS_SUCCESS = 'دسترسی شما به ربات باز شد'
    ACCESS_ALREADY = 'شما از قبل دسترسی کامل به ربات دارید'
    ADD_NUMBER_SUCCESS = "شماره زیر با موفقیت افزوده شد\n{number}"
    EXPORT_CAPTION = 'تعداد {count} شماره در فایل موجود میباشد.'
    INPUT_NUMBER = 'عدد خود را وارد کنید. مثال:\n{example}'


class ButtonTexts:
    ADD_NUMBER = 'افزودن شماره'
    EXPORT = 'خروجی اکسل'
