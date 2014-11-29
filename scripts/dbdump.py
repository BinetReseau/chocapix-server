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

    from bars_api.auth import User

    bars_api_user_1 = User()
    bars_api_user_1.username = u'nadri'
    bars_api_user_1.password = u'ea5a02ec18194e1a86cf8eefd9a4132dc4b2f351a5833df531ffb914b2b6c54e2a12d6118864b945ac5a2496534eadeb15c574ae0672242798557bbbecd86c4d'
    bars_api_user_1.full_name = u'Nadrieril'
    bars_api_user_1.pseudo = u'Nadri'
    bars_api_user_1.last_login = dateutil.parser.parse("2014-11-28T17:39:02+00:00")
    bars_api_user_1.last_modified = dateutil.parser.parse("2014-11-28T17:39:02+00:00")
    bars_api_user_1 = importer.save_or_locate(bars_api_user_1)

    bars_api_user_2 = User()
    bars_api_user_2.username = u'ntag'
    bars_api_user_2.password = u'1672f03cc47e96bd91a92e07e067fa928d6daddbc2e44adc3128fe20f6ca65aa24e08772e0c623214d46a09c621c0e35037e17d53ad0d717ccf60679f125e26d'
    bars_api_user_2.full_name = u'Basile Bruneau'
    bars_api_user_2.pseudo = u'NTag'
    bars_api_user_2.last_login = dateutil.parser.parse("2014-11-28T17:39:02+00:00")
    bars_api_user_2.last_modified = dateutil.parser.parse("2014-11-29T16:51:44+00:00")
    bars_api_user_2 = importer.save_or_locate(bars_api_user_2)

    bars_api_user_3 = User()
    bars_api_user_3.username = u'tizot'
    bars_api_user_3.password = u'65da4a123003996c17272ca96647e52036b138cff1ed46c5dc116f15eada181e61fda94fa312a1ebd91b52b83c15ea97be0a6c9629515299aef1066ab8ef3f29'
    bars_api_user_3.full_name = u'Camille Masset'
    bars_api_user_3.pseudo = u'Tizot'
    bars_api_user_3.last_login = dateutil.parser.parse("2014-11-28T17:39:02+00:00")
    bars_api_user_3.last_modified = dateutil.parser.parse("2014-11-29T16:52:09+00:00")
    bars_api_user_3 = importer.save_or_locate(bars_api_user_3)

    # Processing model: Bar

    from bars_api.models import Bar

    bars_api_bar_1 = Bar()
    bars_api_bar_1.id = u'avironjone'
    bars_api_bar_1.name = u'Aviron J\xf4ne'
    bars_api_bar_1.last_modified = dateutil.parser.parse("2014-11-28T17:39:02+00:00")
    bars_api_bar_1 = importer.save_or_locate(bars_api_bar_1)

    # Processing model: Account

    from bars_api.models import Account

    bars_api_account_1 = Account()
    bars_api_account_1.bar = bars_api_bar_1
    bars_api_account_1.owner = bars_api_user_1
    bars_api_account_1.money = Decimal('-925.000')
    bars_api_account_1.last_modified = dateutil.parser.parse("2014-11-29T16:09:04+00:00")
    bars_api_account_1 = importer.save_or_locate(bars_api_account_1)

    bars_api_account_2 = Account()
    bars_api_account_2.bar = bars_api_bar_1
    bars_api_account_2.owner = bars_api_user_2
    bars_api_account_2.money = Decimal('48.000')
    bars_api_account_2.last_modified = dateutil.parser.parse("2014-11-29T13:39:44+00:00")
    bars_api_account_2 = importer.save_or_locate(bars_api_account_2)

    bars_api_account_3 = Account()
    bars_api_account_3.bar = bars_api_bar_1
    bars_api_account_3.owner = bars_api_user_3
    bars_api_account_3.money = Decimal('1000.000')
    bars_api_account_3.last_modified = dateutil.parser.parse("2014-11-29T16:09:46+00:00")
    bars_api_account_3 = importer.save_or_locate(bars_api_account_3)

    # Processing model: Item

    from bars_api.models import Item

    bars_api_item_1 = Item()
    bars_api_item_1.bar = bars_api_bar_1
    bars_api_item_1.name = u'Chocolat'
    bars_api_item_1.keywords = u''
    bars_api_item_1.qty = Decimal('7.000')
    bars_api_item_1.price = Decimal('1.000')
    bars_api_item_1.deleted = False
    bars_api_item_1.last_modified = dateutil.parser.parse("2014-11-29T12:15:49+00:00")
    bars_api_item_1 = importer.save_or_locate(bars_api_item_1)

    bars_api_item_2 = Item()
    bars_api_item_2.bar = bars_api_bar_1
    bars_api_item_2.name = u'Pizza'
    bars_api_item_2.keywords = u''
    bars_api_item_2.qty = Decimal('-2.000')
    bars_api_item_2.price = Decimal('2.000')
    bars_api_item_2.deleted = False
    bars_api_item_2.last_modified = dateutil.parser.parse("2014-11-29T13:39:44+00:00")
    bars_api_item_2 = importer.save_or_locate(bars_api_item_2)

    bars_api_item_3 = Item()
    bars_api_item_3.bar = bars_api_bar_1
    bars_api_item_3.name = u'Tomates'
    bars_api_item_3.keywords = u'tomates'
    bars_api_item_3.qty = Decimal('10.000')
    bars_api_item_3.price = Decimal('1.500')
    bars_api_item_3.deleted = False
    bars_api_item_3.last_modified = dateutil.parser.parse("2014-11-29T15:05:48+00:00")
    bars_api_item_3 = importer.save_or_locate(bars_api_item_3)

    bars_api_item_4 = Item()
    bars_api_item_4.bar = bars_api_bar_1
    bars_api_item_4.name = u'Nutella'
    bars_api_item_4.keywords = u'nutella tartiner'
    bars_api_item_4.qty = Decimal('100.000')
    bars_api_item_4.price = Decimal('2.400')
    bars_api_item_4.deleted = False
    bars_api_item_4.last_modified = dateutil.parser.parse("2014-11-29T15:06:50+00:00")
    bars_api_item_4 = importer.save_or_locate(bars_api_item_4)

    bars_api_item_5 = Item()
    bars_api_item_5.bar = bars_api_bar_1
    bars_api_item_5.name = u'Spaghetti'
    bars_api_item_5.keywords = u'pates italie'
    bars_api_item_5.qty = Decimal('10.000')
    bars_api_item_5.price = Decimal('1.400')
    bars_api_item_5.deleted = False
    bars_api_item_5.last_modified = dateutil.parser.parse("2014-11-29T15:07:21+00:00")
    bars_api_item_5 = importer.save_or_locate(bars_api_item_5)

    bars_api_item_6 = Item()
    bars_api_item_6.bar = bars_api_bar_1
    bars_api_item_6.name = u'Dosette Nespresso'
    bars_api_item_6.keywords = u'caf\xe9'
    bars_api_item_6.qty = Decimal('230.000')
    bars_api_item_6.price = Decimal('0.480')
    bars_api_item_6.deleted = False
    bars_api_item_6.last_modified = dateutil.parser.parse("2014-11-29T15:07:41+00:00")
    bars_api_item_6 = importer.save_or_locate(bars_api_item_6)

    bars_api_item_7 = Item()
    bars_api_item_7.bar = bars_api_bar_1
    bars_api_item_7.name = u'1664'
    bars_api_item_7.keywords = u'bi\xe8re'
    bars_api_item_7.qty = Decimal('23.000')
    bars_api_item_7.price = Decimal('1.200')
    bars_api_item_7.deleted = False
    bars_api_item_7.last_modified = dateutil.parser.parse("2014-11-29T15:07:56+00:00")
    bars_api_item_7 = importer.save_or_locate(bars_api_item_7)

    bars_api_item_8 = Item()
    bars_api_item_8.bar = bars_api_bar_1
    bars_api_item_8.name = u'Pizza 4 fromages'
    bars_api_item_8.keywords = u'pizza'
    bars_api_item_8.qty = Decimal('5.000')
    bars_api_item_8.price = Decimal('3.400')
    bars_api_item_8.deleted = False
    bars_api_item_8.last_modified = dateutil.parser.parse("2014-11-29T15:08:40+00:00")
    bars_api_item_8 = importer.save_or_locate(bars_api_item_8)

    bars_api_item_9 = Item()
    bars_api_item_9.bar = bars_api_bar_1
    bars_api_item_9.name = u'Pizza bolognaise'
    bars_api_item_9.keywords = u'pizza'
    bars_api_item_9.qty = Decimal('13.000')
    bars_api_item_9.price = Decimal('3.100')
    bars_api_item_9.deleted = False
    bars_api_item_9.last_modified = dateutil.parser.parse("2014-11-29T15:09:01+00:00")
    bars_api_item_9 = importer.save_or_locate(bars_api_item_9)

    bars_api_item_10 = Item()
    bars_api_item_10.bar = bars_api_bar_1
    bars_api_item_10.name = u'Margharitta'
    bars_api_item_10.keywords = u'pizza'
    bars_api_item_10.qty = Decimal('2.000')
    bars_api_item_10.price = Decimal('2.800')
    bars_api_item_10.deleted = False
    bars_api_item_10.last_modified = dateutil.parser.parse("2014-11-29T15:09:15+00:00")
    bars_api_item_10 = importer.save_or_locate(bars_api_item_10)

    # Processing model: Transaction

    from bars_api.models import Transaction

    bars_api_transaction_1 = Transaction()
    bars_api_transaction_1.bar = bars_api_bar_1
    bars_api_transaction_1.author = bars_api_user_1
    bars_api_transaction_1.type = u'give'
    bars_api_transaction_1.timestamp = dateutil.parser.parse("2014-11-28T17:39:02+00:00")
    bars_api_transaction_1.canceled = False
    bars_api_transaction_1.last_modified = dateutil.parser.parse("2014-11-29T16:53:38+00:00")
    bars_api_transaction_1 = importer.save_or_locate(bars_api_transaction_1)

    bars_api_transaction_2 = Transaction()
    bars_api_transaction_2.bar = bars_api_bar_1
    bars_api_transaction_2.author = bars_api_user_1
    bars_api_transaction_2.type = u'buy'
    bars_api_transaction_2.timestamp = dateutil.parser.parse("2014-11-28T18:27:14+00:00")
    bars_api_transaction_2.canceled = False
    bars_api_transaction_2.last_modified = dateutil.parser.parse("2014-11-29T09:57:51+00:00")
    bars_api_transaction_2 = importer.save_or_locate(bars_api_transaction_2)

    bars_api_transaction_3 = Transaction()
    bars_api_transaction_3.bar = bars_api_bar_1
    bars_api_transaction_3.author = bars_api_user_1
    bars_api_transaction_3.type = u'buy'
    bars_api_transaction_3.timestamp = dateutil.parser.parse("2014-11-29T10:06:25+00:00")
    bars_api_transaction_3.canceled = False
    bars_api_transaction_3.last_modified = dateutil.parser.parse("2014-11-29T10:06:25+00:00")
    bars_api_transaction_3 = importer.save_or_locate(bars_api_transaction_3)

    bars_api_transaction_4 = Transaction()
    bars_api_transaction_4.bar = bars_api_bar_1
    bars_api_transaction_4.author = bars_api_user_1
    bars_api_transaction_4.type = u'buy'
    bars_api_transaction_4.timestamp = dateutil.parser.parse("2014-11-29T10:06:42+00:00")
    bars_api_transaction_4.canceled = False
    bars_api_transaction_4.last_modified = dateutil.parser.parse("2014-11-29T10:06:42+00:00")
    bars_api_transaction_4 = importer.save_or_locate(bars_api_transaction_4)

    bars_api_transaction_5 = Transaction()
    bars_api_transaction_5.bar = bars_api_bar_1
    bars_api_transaction_5.author = bars_api_user_1
    bars_api_transaction_5.type = u'buy'
    bars_api_transaction_5.timestamp = dateutil.parser.parse("2014-11-29T10:07:28+00:00")
    bars_api_transaction_5.canceled = False
    bars_api_transaction_5.last_modified = dateutil.parser.parse("2014-11-29T10:07:28+00:00")
    bars_api_transaction_5 = importer.save_or_locate(bars_api_transaction_5)

    bars_api_transaction_6 = Transaction()
    bars_api_transaction_6.bar = bars_api_bar_1
    bars_api_transaction_6.author = bars_api_user_1
    bars_api_transaction_6.type = u'give'
    bars_api_transaction_6.timestamp = dateutil.parser.parse("2014-11-29T10:29:03+00:00")
    bars_api_transaction_6.canceled = False
    bars_api_transaction_6.last_modified = dateutil.parser.parse("2014-11-29T10:29:03+00:00")
    bars_api_transaction_6 = importer.save_or_locate(bars_api_transaction_6)

    bars_api_transaction_7 = Transaction()
    bars_api_transaction_7.bar = bars_api_bar_1
    bars_api_transaction_7.author = bars_api_user_1
    bars_api_transaction_7.type = u'buy'
    bars_api_transaction_7.timestamp = dateutil.parser.parse("2014-11-29T10:53:57+00:00")
    bars_api_transaction_7.canceled = False
    bars_api_transaction_7.last_modified = dateutil.parser.parse("2014-11-29T10:53:57+00:00")
    bars_api_transaction_7 = importer.save_or_locate(bars_api_transaction_7)

    bars_api_transaction_8 = Transaction()
    bars_api_transaction_8.bar = bars_api_bar_1
    bars_api_transaction_8.author = bars_api_user_1
    bars_api_transaction_8.type = u'buy'
    bars_api_transaction_8.timestamp = dateutil.parser.parse("2014-11-29T12:15:49+00:00")
    bars_api_transaction_8.canceled = False
    bars_api_transaction_8.last_modified = dateutil.parser.parse("2014-11-29T12:15:49+00:00")
    bars_api_transaction_8 = importer.save_or_locate(bars_api_transaction_8)

    bars_api_transaction_9 = Transaction()
    bars_api_transaction_9.bar = bars_api_bar_1
    bars_api_transaction_9.author = bars_api_user_3
    bars_api_transaction_9.type = u'punish'
    bars_api_transaction_9.timestamp = dateutil.parser.parse("2014-11-29T16:09:04+00:00")
    bars_api_transaction_9.canceled = False
    bars_api_transaction_9.last_modified = dateutil.parser.parse("2014-11-29T16:09:04+00:00")
    bars_api_transaction_9 = importer.save_or_locate(bars_api_transaction_9)

    # Processing model: AccountOperation

    from bars_api.models import AccountOperation

    bars_api_accountoperation_1 = AccountOperation()
    bars_api_accountoperation_1.transaction = bars_api_transaction_1
    bars_api_accountoperation_1.account = bars_api_account_1
    bars_api_accountoperation_1.delta = Decimal('-10.000')
    bars_api_accountoperation_1 = importer.save_or_locate(bars_api_accountoperation_1)

    bars_api_accountoperation_2 = AccountOperation()
    bars_api_accountoperation_2.transaction = bars_api_transaction_1
    bars_api_accountoperation_2.account = bars_api_account_2
    bars_api_accountoperation_2.delta = Decimal('10.000')
    bars_api_accountoperation_2 = importer.save_or_locate(bars_api_accountoperation_2)

    bars_api_accountoperation_3 = AccountOperation()
    bars_api_accountoperation_3.transaction = bars_api_transaction_2
    bars_api_accountoperation_3.account = bars_api_account_1
    bars_api_accountoperation_3.delta = Decimal('-1.000')
    bars_api_accountoperation_3 = importer.save_or_locate(bars_api_accountoperation_3)

    bars_api_accountoperation_4 = AccountOperation()
    bars_api_accountoperation_4.transaction = bars_api_transaction_3
    bars_api_accountoperation_4.account = bars_api_account_1
    bars_api_accountoperation_4.delta = Decimal('-2.000')
    bars_api_accountoperation_4 = importer.save_or_locate(bars_api_accountoperation_4)

    bars_api_accountoperation_5 = AccountOperation()
    bars_api_accountoperation_5.transaction = bars_api_transaction_4
    bars_api_accountoperation_5.account = bars_api_account_1
    bars_api_accountoperation_5.delta = Decimal('-1.000')
    bars_api_accountoperation_5 = importer.save_or_locate(bars_api_accountoperation_5)

    bars_api_accountoperation_6 = AccountOperation()
    bars_api_accountoperation_6.transaction = bars_api_transaction_5
    bars_api_accountoperation_6.account = bars_api_account_1
    bars_api_accountoperation_6.delta = Decimal('-2.000')
    bars_api_accountoperation_6 = importer.save_or_locate(bars_api_accountoperation_6)

    bars_api_accountoperation_7 = AccountOperation()
    bars_api_accountoperation_7.transaction = bars_api_transaction_6
    bars_api_accountoperation_7.account = bars_api_account_1
    bars_api_accountoperation_7.delta = Decimal('-2.000')
    bars_api_accountoperation_7 = importer.save_or_locate(bars_api_accountoperation_7)

    bars_api_accountoperation_8 = AccountOperation()
    bars_api_accountoperation_8.transaction = bars_api_transaction_6
    bars_api_accountoperation_8.account = bars_api_account_1
    bars_api_accountoperation_8.delta = Decimal('2.000')
    bars_api_accountoperation_8 = importer.save_or_locate(bars_api_accountoperation_8)

    bars_api_accountoperation_9 = AccountOperation()
    bars_api_accountoperation_9.transaction = bars_api_transaction_7
    bars_api_accountoperation_9.account = bars_api_account_1
    bars_api_accountoperation_9.delta = Decimal('-6.000')
    bars_api_accountoperation_9 = importer.save_or_locate(bars_api_accountoperation_9)

    bars_api_accountoperation_10 = AccountOperation()
    bars_api_accountoperation_10.transaction = bars_api_transaction_8
    bars_api_accountoperation_10.account = bars_api_account_1
    bars_api_accountoperation_10.delta = Decimal('-3.000')
    bars_api_accountoperation_10 = importer.save_or_locate(bars_api_accountoperation_10)

    bars_api_accountoperation_11 = AccountOperation()
    bars_api_accountoperation_11.transaction = bars_api_transaction_9
    bars_api_accountoperation_11.account = bars_api_account_1
    bars_api_accountoperation_11.delta = Decimal('-1000.000')
    bars_api_accountoperation_11 = importer.save_or_locate(bars_api_accountoperation_11)

    # Processing model: ItemOperation

    from bars_api.models import ItemOperation

    bars_api_itemoperation_1 = ItemOperation()
    bars_api_itemoperation_1.transaction = bars_api_transaction_2
    bars_api_itemoperation_1.item = bars_api_item_1
    bars_api_itemoperation_1.delta = Decimal('-1.000')
    bars_api_itemoperation_1 = importer.save_or_locate(bars_api_itemoperation_1)

    bars_api_itemoperation_2 = ItemOperation()
    bars_api_itemoperation_2.transaction = bars_api_transaction_3
    bars_api_itemoperation_2.item = bars_api_item_2
    bars_api_itemoperation_2.delta = Decimal('-1.000')
    bars_api_itemoperation_2 = importer.save_or_locate(bars_api_itemoperation_2)

    bars_api_itemoperation_3 = ItemOperation()
    bars_api_itemoperation_3.transaction = bars_api_transaction_4
    bars_api_itemoperation_3.item = bars_api_item_1
    bars_api_itemoperation_3.delta = Decimal('-1.000')
    bars_api_itemoperation_3 = importer.save_or_locate(bars_api_itemoperation_3)

    bars_api_itemoperation_4 = ItemOperation()
    bars_api_itemoperation_4.transaction = bars_api_transaction_5
    bars_api_itemoperation_4.item = bars_api_item_2
    bars_api_itemoperation_4.delta = Decimal('-1.000')
    bars_api_itemoperation_4 = importer.save_or_locate(bars_api_itemoperation_4)

    bars_api_itemoperation_5 = ItemOperation()
    bars_api_itemoperation_5.transaction = bars_api_transaction_7
    bars_api_itemoperation_5.item = bars_api_item_2
    bars_api_itemoperation_5.delta = Decimal('-3.000')
    bars_api_itemoperation_5 = importer.save_or_locate(bars_api_itemoperation_5)

    bars_api_itemoperation_6 = ItemOperation()
    bars_api_itemoperation_6.transaction = bars_api_transaction_8
    bars_api_itemoperation_6.item = bars_api_item_1
    bars_api_itemoperation_6.delta = Decimal('-3.000')
    bars_api_itemoperation_6 = importer.save_or_locate(bars_api_itemoperation_6)

    # Processing model: TransactionData

    from bars_api.models import TransactionData

    bars_api_transactiondata_1 = TransactionData()
    bars_api_transactiondata_1.transaction = bars_api_transaction_9
    bars_api_transactiondata_1.label = u'motive'
    bars_api_transactiondata_1.data = u'TOS'
    bars_api_transactiondata_1 = importer.save_or_locate(bars_api_transactiondata_1)

