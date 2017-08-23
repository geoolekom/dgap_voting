# TODO check importancy of this feature. If essential, make create_paper method of AidRequest class
# all further imports are needed only to make application paper!
from django.core.files import File
from dgap_voting.settings import MEDIA_ROOT, STATIC_ROOT
from .models import user_hash
from .models import AidRequest, AidDocument
from docxtpl import DocxTemplate  # create word document from template
from petrovich.enums import Case, Gender  # склоняем фамилию (в заявлении нужен родительский падеж
from petrovich.main import Petrovich
import datetime

# russian, genitive
MONTH_RU = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}


#  high error rate on non-russians (peoples without middlename)
def get_sex(user):
    if user.userprofile.middlename:
        if user.userprofile.middlename[-1] == "ч":
            return 'male'
    elif user.first_name[-1] in ["a", 'я']:
        return 'female'
    else:
        return 'male'


def create_paper(aid_request: AidRequest):
    today = datetime.date.today()
    date = "{} {} {} г.".format(today.day, MONTH_RU[today.month], today.year)
    user = aid_request.applicant
    userprofile = user.userprofile
    student_info = userprofile.student_info
    sex = get_sex(user)
    if sex == 'female':
        student = "студентки"
        gender = Gender.FEMALE
    else:
        student = "студента"
        gender = Gender.MALE
    p = Petrovich()
    fst = p.firstname(user.first_name, Case.GENITIVE, gender)
    lst = p.firstname(user.last_name, Case.GENITIVE, gender)
    if userprofile.middlename:
        mdl = p.firstname(userprofile.middlename, Case.GENITIVE, gender)
    else:
        mdl = ""
    name = "{} {} {}".format(lst, fst, mdl)
    context = {
        "student": student,
        "group": str(userprofile.group),
        "date": date,
        "name": name,
        "reason": aid_request.category.reason,
    }

    tpl = DocxTemplate(STATIC_ROOT + "/fin_aid/Obrazets_Zayavlenia_Na_Matpomosch.docx")
    tpl.render(context)
    path = MEDIA_ROOT + "/aid_docs/user_{}/application-{}-{}-{}.docx".format(user_hash(user), today.year, today.month, today.day)
    tpl.save(path)
    AidDocument.objects.create(file=File(path), request=aid_request, is_application_paper=True)
    return path
