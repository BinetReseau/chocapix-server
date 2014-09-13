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

    # Processing model: User

    from bars_api.models import User

    bars_api_user_1 = User()
    bars_api_user_1.login = u'nadri'
    bars_api_user_1.password = u'changeme'
    bars_api_user_1.name = u'Nadrieril'
    bars_api_user_1.pseudo = u'Nadri'
    bars_api_user_1.last_modified = dateutil.parser.parse("2014-09-13T16:08:41+00:00")
    bars_api_user_1 = importer.save_or_locate(bars_api_user_1)

    bars_api_user_2 = User()
    bars_api_user_2.login = u'ntag'
    bars_api_user_2.password = u''
    bars_api_user_2.name = u'Ntag'
    bars_api_user_2.pseudo = u'Ntag'
    bars_api_user_2.last_modified = dateutil.parser.parse("2014-09-13T16:08:41+00:00")
    bars_api_user_2 = importer.save_or_locate(bars_api_user_2)

    # Processing model: Bar

    from bars_api.models import Bar

    bars_api_bar_1 = Bar()
    bars_api_bar_1.id = u'avironjone'
    bars_api_bar_1.name = u'Aviron J\xf4ne'
    bars_api_bar_1.last_modified = dateutil.parser.parse("2014-09-13T16:08:41+00:00")
    bars_api_bar_1 = importer.save_or_locate(bars_api_bar_1)

    # Processing model: Account

    from bars_api.models import Account

    bars_api_account_1 = Account()
    bars_api_account_1.bar = bars_api_bar_1
    bars_api_account_1.owner = bars_api_user_1
    bars_api_account_1.money = Decimal('100.000')
    bars_api_account_1.last_modified = dateutil.parser.parse("2014-09-13T16:08:41+00:00")
    bars_api_account_1 = importer.save_or_locate(bars_api_account_1)

    bars_api_account_2 = Account()
    bars_api_account_2.bar = bars_api_bar_1
    bars_api_account_2.owner = bars_api_user_2
    bars_api_account_2.money = Decimal('50.000')
    bars_api_account_2.last_modified = dateutil.parser.parse("2014-09-13T16:08:41+00:00")
    bars_api_account_2 = importer.save_or_locate(bars_api_account_2)

    # Processing model: Item

    from bars_api.models import Item

    bars_api_item_1 = Item()
    bars_api_item_1.bar = bars_api_bar_1
    bars_api_item_1.name = u'Chocolat'
    bars_api_item_1.qty = Decimal('10.000')
    bars_api_item_1.price = Decimal('1.000')
    bars_api_item_1.last_modified = dateutil.parser.parse("2014-09-13T16:08:41+00:00")
    bars_api_item_1 = importer.save_or_locate(bars_api_item_1)

    bars_api_item_2 = Item()
    bars_api_item_2.bar = bars_api_bar_1
    bars_api_item_2.name = u'Pizza'
    bars_api_item_2.qty = Decimal('10.000')
    bars_api_item_2.price = Decimal('2.000')
    bars_api_item_2.last_modified = dateutil.parser.parse("2014-09-13T16:08:41+00:00")
    bars_api_item_2 = importer.save_or_locate(bars_api_item_2)

    # Processing model: Transaction

    from bars_api.models import Transaction

    bars_api_transaction_1 = Transaction()
    bars_api_transaction_1.bar = bars_api_bar_1
    bars_api_transaction_1.author = bars_api_user_1
    bars_api_transaction_1.type = u'buy'
    bars_api_transaction_1.timestamp = dateutil.parser.parse("2014-09-13T16:08:41+00:00")
    bars_api_transaction_1.canceled = False
    bars_api_transaction_1.last_modified = dateutil.parser.parse("2014-09-13T16:08:41+00:00")
    bars_api_transaction_1 = importer.save_or_locate(bars_api_transaction_1)

    bars_api_transaction_2 = Transaction()
    bars_api_transaction_2.bar = bars_api_bar_1
    bars_api_transaction_2.author = bars_api_user_1
    bars_api_transaction_2.type = u'give'
    bars_api_transaction_2.timestamp = dateutil.parser.parse("2014-09-13T16:14:43+00:00")
    bars_api_transaction_2.canceled = False
    bars_api_transaction_2.last_modified = dateutil.parser.parse("2014-09-13T16:14:43+00:00")
    bars_api_transaction_2 = importer.save_or_locate(bars_api_transaction_2)

    # Processing model: AccountOperation

    from bars_api.models import AccountOperation

    bars_api_accountoperation_1 = AccountOperation()
    bars_api_accountoperation_1.transaction = bars_api_transaction_1
    bars_api_accountoperation_1.account = bars_api_account_1
    bars_api_accountoperation_1.delta = Decimal('-1.000')
    bars_api_accountoperation_1 = importer.save_or_locate(bars_api_accountoperation_1)

    bars_api_accountoperation_2 = AccountOperation()
    bars_api_accountoperation_2.transaction = bars_api_transaction_2
    bars_api_accountoperation_2.account = bars_api_account_1
    bars_api_accountoperation_2.delta = Decimal('-10.000')
    bars_api_accountoperation_2 = importer.save_or_locate(bars_api_accountoperation_2)

    bars_api_accountoperation_3 = AccountOperation()
    bars_api_accountoperation_3.transaction = bars_api_transaction_2
    bars_api_accountoperation_3.account = bars_api_account_2
    bars_api_accountoperation_3.delta = Decimal('10.000')
    bars_api_accountoperation_3 = importer.save_or_locate(bars_api_accountoperation_3)

    # Processing model: ItemOperation

    from bars_api.models import ItemOperation

    bars_api_itemoperation_1 = ItemOperation()
    bars_api_itemoperation_1.transaction = bars_api_transaction_1
    bars_api_itemoperation_1.item = bars_api_item_1
    bars_api_itemoperation_1.delta = Decimal('-1.000')
    bars_api_itemoperation_1 = importer.save_or_locate(bars_api_itemoperation_1)

