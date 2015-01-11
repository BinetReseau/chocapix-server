#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones inteact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# manage.py dumpscript bars_api
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script

from django.db import transaction

class BasicImportHelper(object):

    def pre_import(self):
        pass

    # You probably want to uncomment on of these two lines
    # @transaction.atomic  # Django 1.6
    # @transaction.commit_on_success  # Django <1.6
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(self, original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = { pk_name: pk_value }
        the_obj = the_class.objects.get(**search_data)
        #print(the_obj)
        return the_obj


    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper
    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper ) , {} )()
except ImportError as e:
    if str(e) == "No module named import_helper":
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)

def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()

def import_data():
    # Initial Imports

    # Processing model: Bar

    from bars_api.models.bar import Bar

    bars_api_bar_1 = Bar()
    bars_api_bar_1.id = u'avironjone'
    bars_api_bar_1.name = u'Aviron J\xf4ne'
    bars_api_bar_1.last_modified = dateutil.parser.parse("2014-12-02T17:46:55+00:00")
    bars_api_bar_1 = importer.save_or_locate(bars_api_bar_1)

    # Processing model: Item

    from bars_api.models.item import Item

    bars_api_item_1 = Item()
    bars_api_item_1.bar = bars_api_bar_1
    bars_api_item_1.name = u'Chocolat'
    bars_api_item_1.keywords = u''
    bars_api_item_1.qty = 2.0
    bars_api_item_1.unit = u''
    bars_api_item_1.unit_value = 1.0
    bars_api_item_1.buy_unit = u''
    bars_api_item_1.buy_unit_value = 1.0
    bars_api_item_1.price = 1.0
    bars_api_item_1.buy_price = 1.0
    bars_api_item_1.deleted = False
    bars_api_item_1.last_modified = dateutil.parser.parse("2014-12-02T17:46:57+00:00")
    bars_api_item_1 = importer.save_or_locate(bars_api_item_1)

    bars_api_item_2 = Item()
    bars_api_item_2.bar = bars_api_bar_1
    bars_api_item_2.name = u'Pizza'
    bars_api_item_2.keywords = u''
    bars_api_item_2.qty = -9.0
    bars_api_item_2.unit = u''
    bars_api_item_2.unit_value = 1.0
    bars_api_item_2.buy_unit = u''
    bars_api_item_2.buy_unit_value = 1.0
    bars_api_item_2.price = 2.0
    bars_api_item_2.buy_price = 1.0
    bars_api_item_2.deleted = False
    bars_api_item_2.last_modified = dateutil.parser.parse("2014-12-02T19:52:44+00:00")
    bars_api_item_2 = importer.save_or_locate(bars_api_item_2)

    bars_api_item_3 = Item()
    bars_api_item_3.bar = bars_api_bar_1
    bars_api_item_3.name = u'Tomates'
    bars_api_item_3.keywords = u'tomates'
    bars_api_item_3.qty = 10.0
    bars_api_item_3.unit = u''
    bars_api_item_3.unit_value = 1.0
    bars_api_item_3.buy_unit = u''
    bars_api_item_3.buy_unit_value = 1.0
    bars_api_item_3.price = 1.5
    bars_api_item_3.buy_price = 1.0
    bars_api_item_3.deleted = False
    bars_api_item_3.last_modified = dateutil.parser.parse("2014-12-02T17:46:55+00:00")
    bars_api_item_3 = importer.save_or_locate(bars_api_item_3)

    bars_api_item_4 = Item()
    bars_api_item_4.bar = bars_api_bar_1
    bars_api_item_4.name = u'Nutella'
    bars_api_item_4.keywords = u'nutella tartiner'
    bars_api_item_4.qty = 4.0
    bars_api_item_4.unit = u'g'
    bars_api_item_4.unit_value = 0.00158730159
    bars_api_item_4.buy_unit = u'pot'
    bars_api_item_4.buy_unit_value = 1.0
    bars_api_item_4.price = 8.0
    bars_api_item_4.buy_price = 8.0
    bars_api_item_4.deleted = False
    bars_api_item_4.last_modified = dateutil.parser.parse("2014-12-02T19:51:40+00:00")
    bars_api_item_4 = importer.save_or_locate(bars_api_item_4)

    bars_api_item_5 = Item()
    bars_api_item_5.bar = bars_api_bar_1
    bars_api_item_5.name = u'Spaghetti'
    bars_api_item_5.keywords = u'pates italie'
    bars_api_item_5.qty = 10.0
    bars_api_item_5.unit = u''
    bars_api_item_5.unit_value = 1.0
    bars_api_item_5.buy_unit = u''
    bars_api_item_5.buy_unit_value = 1.0
    bars_api_item_5.price = 1.4
    bars_api_item_5.buy_price = 1.0
    bars_api_item_5.deleted = False
    bars_api_item_5.last_modified = dateutil.parser.parse("2014-12-02T17:46:55+00:00")
    bars_api_item_5 = importer.save_or_locate(bars_api_item_5)

    bars_api_item_6 = Item()
    bars_api_item_6.bar = bars_api_bar_1
    bars_api_item_6.name = u'Dosette Nespresso'
    bars_api_item_6.keywords = u'caf\xe9'
    bars_api_item_6.qty = 230.0
    bars_api_item_6.unit = u''
    bars_api_item_6.unit_value = 1.0
    bars_api_item_6.buy_unit = u''
    bars_api_item_6.buy_unit_value = 1.0
    bars_api_item_6.price = 0.48
    bars_api_item_6.buy_price = 1.0
    bars_api_item_6.deleted = False
    bars_api_item_6.last_modified = dateutil.parser.parse("2014-12-02T17:46:55+00:00")
    bars_api_item_6 = importer.save_or_locate(bars_api_item_6)

    bars_api_item_7 = Item()
    bars_api_item_7.bar = bars_api_bar_1
    bars_api_item_7.name = u'1664'
    bars_api_item_7.keywords = u'bi\xe8re'
    bars_api_item_7.qty = 23.0
    bars_api_item_7.unit = u''
    bars_api_item_7.unit_value = 1.0
    bars_api_item_7.buy_unit = u''
    bars_api_item_7.buy_unit_value = 1.0
    bars_api_item_7.price = 1.2
    bars_api_item_7.buy_price = 1.0
    bars_api_item_7.deleted = False
    bars_api_item_7.last_modified = dateutil.parser.parse("2014-12-02T17:46:55+00:00")
    bars_api_item_7 = importer.save_or_locate(bars_api_item_7)

    bars_api_item_8 = Item()
    bars_api_item_8.bar = bars_api_bar_1
    bars_api_item_8.name = u'Pizza 4 fromages'
    bars_api_item_8.keywords = u'pizza'
    bars_api_item_8.qty = 3.0
    bars_api_item_8.unit = u''
    bars_api_item_8.unit_value = 1.0
    bars_api_item_8.buy_unit = u''
    bars_api_item_8.buy_unit_value = 1.0
    bars_api_item_8.price = 3.4
    bars_api_item_8.buy_price = 1.0
    bars_api_item_8.deleted = False
    bars_api_item_8.last_modified = dateutil.parser.parse("2014-12-05T17:30:07+00:00")
    bars_api_item_8 = importer.save_or_locate(bars_api_item_8)

    bars_api_item_9 = Item()
    bars_api_item_9.bar = bars_api_bar_1
    bars_api_item_9.name = u'Pizza bolognaise'
    bars_api_item_9.keywords = u'pizza'
    bars_api_item_9.qty = 13.0
    bars_api_item_9.unit = u''
    bars_api_item_9.unit_value = 1.0
    bars_api_item_9.buy_unit = u''
    bars_api_item_9.buy_unit_value = 1.0
    bars_api_item_9.price = 3.1
    bars_api_item_9.buy_price = 1.0
    bars_api_item_9.deleted = False
    bars_api_item_9.last_modified = dateutil.parser.parse("2014-12-02T17:46:55+00:00")
    bars_api_item_9 = importer.save_or_locate(bars_api_item_9)

    bars_api_item_10 = Item()
    bars_api_item_10.bar = bars_api_bar_1
    bars_api_item_10.name = u'Margharitta'
    bars_api_item_10.keywords = u'pizza'
    bars_api_item_10.qty = 2.0
    bars_api_item_10.unit = u''
    bars_api_item_10.unit_value = 1.0
    bars_api_item_10.buy_unit = u''
    bars_api_item_10.buy_unit_value = 1.0
    bars_api_item_10.price = 2.8
    bars_api_item_10.buy_price = 1.0
    bars_api_item_10.deleted = False
    bars_api_item_10.last_modified = dateutil.parser.parse("2014-12-02T17:46:55+00:00")
    bars_api_item_10 = importer.save_or_locate(bars_api_item_10)

    # Processing model: User

    from bars_api.models.user import User

    bars_api_user_1 = User()
    bars_api_user_1.username = u'nadri'
    bars_api_user_1.password = u'ea5a02ec18194e1a86cf8eefd9a4132dc4b2f351a5833df531ffb914b2b6c54e2a12d6118864b945ac5a2496534eadeb15c574ae0672242798557bbbecd86c4d'
    bars_api_user_1.full_name = u'Nadrieril'
    bars_api_user_1.pseudo = u'Nadri'
    bars_api_user_1.last_login = dateutil.parser.parse("2014-11-28T17:39:02+00:00")
    bars_api_user_1.last_modified = dateutil.parser.parse("2014-12-02T17:46:55+00:00")
    bars_api_user_1 = importer.save_or_locate(bars_api_user_1)

    bars_api_user_2 = User()
    bars_api_user_2.username = u'ntag'
    bars_api_user_2.password = u'1672f03cc47e96bd91a92e07e067fa928d6daddbc2e44adc3128fe20f6ca65aa24e08772e0c623214d46a09c621c0e35037e17d53ad0d717ccf60679f125e26d'
    bars_api_user_2.full_name = u'Basile Bruneau'
    bars_api_user_2.pseudo = u'NTag'
    bars_api_user_2.last_login = dateutil.parser.parse("2014-11-28T17:39:02+00:00")
    bars_api_user_2.last_modified = dateutil.parser.parse("2014-12-02T17:46:55+00:00")
    bars_api_user_2 = importer.save_or_locate(bars_api_user_2)

    bars_api_user_3 = User()
    bars_api_user_3.username = u'tizot'
    bars_api_user_3.password = u'65da4a123003996c17272ca96647e52036b138cff1ed46c5dc116f15eada181e61fda94fa312a1ebd91b52b83c15ea97be0a6c9629515299aef1066ab8ef3f29'
    bars_api_user_3.full_name = u'Camille Masset'
    bars_api_user_3.pseudo = u'Tizot'
    bars_api_user_3.last_login = dateutil.parser.parse("2014-11-28T17:39:02+00:00")
    bars_api_user_3.last_modified = dateutil.parser.parse("2014-12-02T17:46:55+00:00")
    bars_api_user_3 = importer.save_or_locate(bars_api_user_3)

    # Processing model: Account

    from bars_api.models.account import Account

    bars_api_account_1 = Account()
    bars_api_account_1.bar = bars_api_bar_1
    bars_api_account_1.owner = bars_api_user_1
    bars_api_account_1.money = -1974.00024
    bars_api_account_1.last_modified = dateutil.parser.parse("2014-12-02T17:47:18+00:00")
    bars_api_account_1 = importer.save_or_locate(bars_api_account_1)

    bars_api_account_2 = Account()
    bars_api_account_2.bar = bars_api_bar_1
    bars_api_account_2.owner = bars_api_user_2
    bars_api_account_2.money = 42.0730158728
    bars_api_account_2.last_modified = dateutil.parser.parse("2014-12-05T17:30:07+00:00")
    bars_api_account_2 = importer.save_or_locate(bars_api_account_2)

    bars_api_account_3 = Account()
    bars_api_account_3.bar = bars_api_bar_1
    bars_api_account_3.owner = bars_api_user_3
    bars_api_account_3.money = 1005.0
    bars_api_account_3.last_modified = dateutil.parser.parse("2014-12-02T19:52:50+00:00")
    bars_api_account_3 = importer.save_or_locate(bars_api_account_3)
