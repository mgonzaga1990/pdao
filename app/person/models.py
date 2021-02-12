from address.models import *
from django.db import models

from address.models import Barangy


class Person(models.Model):
    class ETHNIC_GROUP(models.IntegerChoices):
        IGOROT = 0,
        BICOLANO = 1,

    class RELIGIONS(models.IntegerChoices):
        CHRISTIAN = 0,
        MUSLIM = 1,
        BUDDIST = 2

    class SUFFIX(models.IntegerChoices):
        JR = 0,
        SR = 1,
        II = 2,
        III = 3,
        IV = 4,
        V = 5

    class GENDER(models.IntegerChoices):
        MALE = 1,
        FEMALE = 2

    class CIVIL_STATUS(models.IntegerChoices):
        SINGLE = 0,
        MARRIED = 1,
        SEPARATED = 2,
        LIVE_IN = 3,
        WIDOW = 4

    class BLOOD_TYPES(models.IntegerChoices):
        A_PLUS = 0,
        A_MINUS = 1,
        AB_PLUS = 2,
        AB_MINUS = 3,
        B_PLUS = 4,
        B_MINUS = 5,
        O_PLUS = 6,
        O_MINUS = 7

    class EMPLOYMENT_TYPES(models.IntegerChoices):
        PERMANENT_OR_REGULAR = 0,
        SEASONAL = 1,
        CASUAL = 2,
        EMERGENCY = 3

    class EMPLOYMENT_CATEGORY(models.IntegerChoices):
        GOVERNMENT = 0,
        PRIVATE = 1,

    class EMPLOYMENT_STATUS(models.IntegerChoices):
        EMPLOYED = 0,
        UNEMPLOYED = 1,
        SELF_EMPLOYED = 2

    class EMPLOYMENT_OCCUPATION(models.IntegerChoices):
        MANAGER = 0,
        PROFESSIONAL = 1,
        TECHNICAL_AND_ASSOCIATE_PROFESSIONAL = 2,
        CLERICAL_SUPPORT_WORKERS = 3,
        SERVICE_AND_SALES_WORKERS = 4,
        SKILLED_AGRICULTURAL_FORESTRY_AND_FISHERY_WORKERS = 5,
        CRAFT_AND_RELATED_TRADE_WORKERS = 6,
        PLANT_AND_MACHINE_OPERATORS_AND_ASSEMBLERS = 7,
        ELEMENTARY_OCCUPATIONS = 8,
        ARMED_FORCES_OCCUPATIONS = 9,
        OTHERS = 10

    pwd_id = models.CharField(u'PWD No.', max_length=35,
                              help_text=u'Persons with Disability Number (RR-PPMM-BBB-NNNNNNN)')

    last_name = models.CharField(max_length=35)
    first_name = models.CharField(max_length=35)
    middle_name = models.CharField(max_length=35)

    birthday = models.DateField(auto_now_add=True)
    suffix = models.IntegerField(choices=SUFFIX.choices, null=True)
    gender = models.IntegerField(choices=GENDER.choices, null=True)
    birthday = models.DateField()
    cover_photo = models.ImageField(upload_to="profile", blank=True, null=True)
    religion = models.IntegerField(choices=RELIGIONS.choices, null=True)
    ethnic_group = models.IntegerField(choices=ETHNIC_GROUP.choices, null=True)
    civil_status = models.IntegerField(choices=CIVIL_STATUS.choices, null=True)

    #
    blood_type = models.IntegerField(choices=BLOOD_TYPES.choices, null=True)
    sss_no = models.CharField(u'SSS No.', max_length=25, help_text=u'Social Security Number')
    gsis_no = models.CharField(u'GSIS No.', max_length=25, help_text=u'Please provide if any')
    pagibig_no = models.CharField(max_length=25)
    philhealth_no = models.CharField(max_length=25)
    #
    # # contact section
    phone_number = models.CharField(max_length=25)
    mobile_number = models.CharField(max_length=25)
    email = models.CharField(max_length=25)

    #
    # # employment section
    status = models.IntegerField(choices=EMPLOYMENT_STATUS.choices, null=False)
    category = models.IntegerField(choices=EMPLOYMENT_CATEGORY.choices, null=True)
    type_of_emp = models.IntegerField(choices=EMPLOYMENT_TYPES.choices, null=True)
    occupation = models.IntegerField(choices=EMPLOYMENT_OCCUPATION.choices, null=True)
    others = models.CharField(max_length=25)

    #
    # # organization section
    org_aff = models.CharField(u'Organization Affiliated',max_length=25)
    org_contact_person = models.CharField(u'Contact Person',max_length=25)
    org_address = models.CharField(u'Office Address',max_length=25)
    org_tel = models.CharField(u'Tel. Nos.',max_length=25)

    def fullname(self):
        return self.last_name + ', ' + self.first_name + ' ' + self.middle_name + ' ' + str(Person.SUFFIX(self.status).name).lower()

    def __str__(self):
        return self.fullname()


class Address(models.Model):
    house_no_and_street = models.CharField(max_length=25)
    purok = models.CharField(u'Purok', max_length=25)
    barangy = models.ForeignKey(Barangy, on_delete=models.CASCADE)
    person = models.ForeignKey(Person, null=False, on_delete=models.CASCADE)
    default = models.BooleanField(default=False)

    def __str__(self):
        return str(self.barangy.municipality.name)

    def to_string(self):
        return str(self.address_line_one + self.address_line_two + self.purok)
