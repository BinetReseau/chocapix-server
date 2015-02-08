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

import sys, os
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
    # Processing model: Bar

    from bars_core.models.bar import Bar

    bars_api_bar_1 = Bar()
    bars_api_bar_1.id = u'avironjone'
    bars_api_bar_1.name = u'Aviron J\xf4ne'
    bars_api_bar_1 = importer.save_or_locate(bars_api_bar_1)

    bars_api_bar_2 = Bar()
    bars_api_bar_2.id = u'footrouje'
    bars_api_bar_2.name = u'Foot Rouje'
    bars_api_bar_2 = importer.save_or_locate(bars_api_bar_2)

    bars_api_bar_3 = Bar()
    bars_api_bar_3.id = u'natationjone'
    bars_api_bar_3.name = u'Natation J\xf4ne'
    bars_api_bar_3 = importer.save_or_locate(bars_api_bar_3)

    # Processing model: User

    from bars_core.models.user import User

    bars_api_user_1 = User()
    bars_api_user_1.username = u'nadri'
    bars_api_user_1.set_password('nadri')
    bars_api_user_1.full_name = u'Nadrieril'
    bars_api_user_1.pseudo = u'Nadri'
    bars_api_user_1 = importer.save_or_locate(bars_api_user_1)

    bars_api_user_2 = User()
    bars_api_user_2.username = u'ntag'
    bars_api_user_2.set_password('ntag')
    bars_api_user_2.full_name = u'Basile Bruneau'
    bars_api_user_2.pseudo = u'NTag'
    bars_api_user_2 = importer.save_or_locate(bars_api_user_2)

    bars_api_user_3 = User()
    bars_api_user_3.username = u'tizot'
    bars_api_user_3.set_password('tizot')
    bars_api_user_3.full_name = u'Camille Masset'
    bars_api_user_3.pseudo = u'Tizot'
    bars_api_user_3 = importer.save_or_locate(bars_api_user_3)

    bars_api_user_4 = User()
    bars_api_user_4.username = u'denis'
    bars_api_user_4.set_password('denis')
    bars_api_user_4.full_name = u'Denis M\xe9rigoux'
    bars_api_user_4.pseudo = u''
    bars_api_user_4 = importer.save_or_locate(bars_api_user_4)


    # Processing model: Account

    from bars_base.models.account import Account

    bars_api_account_1 = Account()
    bars_api_account_1.bar = bars_api_bar_1
    bars_api_account_1.owner = bars_api_user_1
    bars_api_account_1 = importer.save_or_locate(bars_api_account_1)

    bars_api_account_2 = Account()
    bars_api_account_2.bar = bars_api_bar_1
    bars_api_account_2.owner = bars_api_user_2
    bars_api_account_2 = importer.save_or_locate(bars_api_account_2)

    bars_api_account_3 = Account()
    bars_api_account_3.bar = bars_api_bar_1
    bars_api_account_3.owner = bars_api_user_3
    bars_api_account_3 = importer.save_or_locate(bars_api_account_3)

    bars_api_account_4 = Account()
    bars_api_account_4.bar = bars_api_bar_1
    bars_api_account_4.owner = bars_api_user_4
    bars_api_account_4 = importer.save_or_locate(bars_api_account_4)

    bars_api_account_5 = Account()
    bars_api_account_5.bar = bars_api_bar_3
    bars_api_account_5.owner = bars_api_user_2
    bars_api_account_5 = importer.save_or_locate(bars_api_account_5)

    # Processing model: Item

    from bars_base.models.item import Item

    bars_api_item_1 = Item()
    bars_api_item_1.bar = bars_api_bar_1
    bars_api_item_1.name = u'Chocolat'
    bars_api_item_1.keywords = u''
    bars_api_item_1.unit = u''
    bars_api_item_1.unit_value = 1.0
    bars_api_item_1.buy_unit = u''
    bars_api_item_1.buy_unit_value = 1.0
    bars_api_item_1.price = 1.0
    bars_api_item_1.buy_price = 1.0
    bars_api_item_1 = importer.save_or_locate(bars_api_item_1)

    bars_api_item_2 = Item()
    bars_api_item_2.bar = bars_api_bar_1
    bars_api_item_2.name = u'Pizza'
    bars_api_item_2.keywords = u''
    bars_api_item_2.unit = u''
    bars_api_item_2.unit_value = 1.0
    bars_api_item_2.buy_unit = u''
    bars_api_item_2.buy_unit_value = 1.0
    bars_api_item_2.price = 2.0
    bars_api_item_2.buy_price = 1.0
    bars_api_item_2 = importer.save_or_locate(bars_api_item_2)

    bars_api_item_3 = Item()
    bars_api_item_3.bar = bars_api_bar_1
    bars_api_item_3.name = u'Tomates'
    bars_api_item_3.keywords = u'tomates'
    bars_api_item_3.unit = u''
    bars_api_item_3.unit_value = 1.0
    bars_api_item_3.buy_unit = u''
    bars_api_item_3.buy_unit_value = 1.0
    bars_api_item_3.price = 1.5
    bars_api_item_3.buy_price = 1.0
    bars_api_item_3 = importer.save_or_locate(bars_api_item_3)

    bars_api_item_4 = Item()
    bars_api_item_4.bar = bars_api_bar_1
    bars_api_item_4.name = u'Nutella'
    bars_api_item_4.keywords = u'nutella tartiner'
    bars_api_item_4.unit = u'g'
    bars_api_item_4.unit_value = 0.00158730159
    bars_api_item_4.buy_unit = u'pot'
    bars_api_item_4.buy_unit_value = 1.0
    bars_api_item_4.price = 8.0
    bars_api_item_4.buy_price = 8.0
    bars_api_item_4 = importer.save_or_locate(bars_api_item_4)

    bars_api_item_5 = Item()
    bars_api_item_5.bar = bars_api_bar_1
    bars_api_item_5.name = u'Spaghetti'
    bars_api_item_5.keywords = u'pates italie'
    bars_api_item_5.unit = u'g'
    bars_api_item_5.unit_value = 1000.0
    bars_api_item_5.buy_unit = u'kg'
    bars_api_item_5.buy_unit_value = 1.0
    bars_api_item_5.price = 1e-06
    bars_api_item_5.buy_price = 1.0
    bars_api_item_5 = importer.save_or_locate(bars_api_item_5)

    bars_api_item_6 = Item()
    bars_api_item_6.bar = bars_api_bar_1
    bars_api_item_6.name = u'Dosette Nespresso'
    bars_api_item_6.keywords = u'caf\xe9'
    bars_api_item_6.unit = u''
    bars_api_item_6.unit_value = 1.0
    bars_api_item_6.buy_unit = u''
    bars_api_item_6.buy_unit_value = 1.0
    bars_api_item_6.price = 0.48
    bars_api_item_6.buy_price = 1.0
    bars_api_item_6 = importer.save_or_locate(bars_api_item_6)

    bars_api_item_7 = Item()
    bars_api_item_7.bar = bars_api_bar_1
    bars_api_item_7.name = u'1664'
    bars_api_item_7.keywords = u'bi\xe8re'
    bars_api_item_7.unit = u''
    bars_api_item_7.unit_value = 1.0
    bars_api_item_7.buy_unit = u'Pack'
    bars_api_item_7.buy_unit_value = 20.0
    bars_api_item_7.price = 1.2
    bars_api_item_7.buy_price = 1.0
    bars_api_item_7 = importer.save_or_locate(bars_api_item_7)

    bars_api_item_8 = Item()
    bars_api_item_8.bar = bars_api_bar_1
    bars_api_item_8.name = u'Pizza 4 fromages'
    bars_api_item_8.keywords = u'pizza'
    bars_api_item_8.unit = u''
    bars_api_item_8.unit_value = 1.0
    bars_api_item_8.buy_unit = u''
    bars_api_item_8.buy_unit_value = 1.0
    bars_api_item_8.price = 3.4
    bars_api_item_8.buy_price = 1.0
    bars_api_item_8 = importer.save_or_locate(bars_api_item_8)

    bars_api_item_9 = Item()
    bars_api_item_9.bar = bars_api_bar_1
    bars_api_item_9.name = u'Pizza bolognaise'
    bars_api_item_9.keywords = u'pizza'
    bars_api_item_9.unit = u''
    bars_api_item_9.unit_value = 1.0
    bars_api_item_9.buy_unit = u''
    bars_api_item_9.buy_unit_value = 1.0
    bars_api_item_9.price = 3.1
    bars_api_item_9.buy_price = 1.0
    bars_api_item_9 = importer.save_or_locate(bars_api_item_9)

    bars_api_item_10 = Item()
    bars_api_item_10.bar = bars_api_bar_1
    bars_api_item_10.name = u'Margharitta'
    bars_api_item_10.keywords = u'pizza'
    bars_api_item_10.unit = u''
    bars_api_item_10.unit_value = 1.0
    bars_api_item_10.buy_unit = u''
    bars_api_item_10.buy_unit_value = 1.0
    bars_api_item_10.price = 2.8
    bars_api_item_10.buy_price = 1.0
    bars_api_item_10 = importer.save_or_locate(bars_api_item_10)

    bars_api_item_11 = Item()
    bars_api_item_11.bar = bars_api_bar_1
    bars_api_item_11.name = u'Radis'
    bars_api_item_11.keywords = u'l\xe9gume'
    bars_api_item_11.unit = u'g'
    bars_api_item_11.unit_value = 0.001
    bars_api_item_11.buy_unit = u'kg'
    bars_api_item_11.buy_unit_value = 1.0
    bars_api_item_11.price = 8.0
    bars_api_item_11.buy_price = 1.0
    bars_api_item_11 = importer.save_or_locate(bars_api_item_11)

    bars_api_item_12 = Item()
    bars_api_item_12.bar = bars_api_bar_1
    bars_api_item_12.name = u'Galette'
    bars_api_item_12.keywords = u'sarazin'
    bars_api_item_12.unit = u''
    bars_api_item_12.unit_value = 0.166666666666667
    bars_api_item_12.buy_unit = u'paquet de 6'
    bars_api_item_12.buy_unit_value = 1.0
    bars_api_item_12.price = 3.5
    bars_api_item_12.buy_price = 1.0
    bars_api_item_12 = importer.save_or_locate(bars_api_item_12)

    bars_api_item_13 = Item()
    bars_api_item_13.bar = bars_api_bar_1
    bars_api_item_13.name = u'Jambon'
    bars_api_item_13.keywords = u'charcuterie'
    bars_api_item_13.unit = u'tranche'
    bars_api_item_13.unit_value = 0.166666666666667
    bars_api_item_13.buy_unit = u'paquet'
    bars_api_item_13.buy_unit_value = 1.0
    bars_api_item_13.price = 2.67
    bars_api_item_13.buy_price = 1.0
    bars_api_item_13 = importer.save_or_locate(bars_api_item_13)

    bars_api_item_14 = Item()
    bars_api_item_14.bar = bars_api_bar_1
    bars_api_item_14.name = u'Emmental rap\xe9'
    bars_api_item_14.keywords = u'fromage'
    bars_api_item_14.unit = u'g'
    bars_api_item_14.unit_value = 0.002
    bars_api_item_14.buy_unit = u'paquet de 500g'
    bars_api_item_14.buy_unit_value = 1.0
    bars_api_item_14.price = 6.3
    bars_api_item_14.buy_price = 1.0
    bars_api_item_14 = importer.save_or_locate(bars_api_item_14)

    bars_api_item_15 = Item()
    bars_api_item_15.bar = bars_api_bar_1
    bars_api_item_15.name = u'Pain de mie'
    bars_api_item_15.keywords = u'd\xe9jeuner'
    bars_api_item_15.unit = u'tranche'
    bars_api_item_15.unit_value = 0.0476190476190476
    bars_api_item_15.buy_unit = u'paquet de 21'
    bars_api_item_15.buy_unit_value = 1.0
    bars_api_item_15.price = 4.12
    bars_api_item_15.buy_price = 1.0
    bars_api_item_15 = importer.save_or_locate(bars_api_item_15)

    bars_api_item_16 = Item()
    bars_api_item_16.bar = bars_api_bar_1
    bars_api_item_16.name = u'Canette de coca'
    bars_api_item_16.keywords = u'boisson'
    bars_api_item_16.unit = u''
    bars_api_item_16.unit_value = 0.1
    bars_api_item_16.buy_unit = u'pack de 10'
    bars_api_item_16.buy_unit_value = 1.0
    bars_api_item_16.price = 5.6
    bars_api_item_16.buy_price = 1.0
    bars_api_item_16 = importer.save_or_locate(bars_api_item_16)

    bars_api_item_17 = Item()
    bars_api_item_17.bar = bars_api_bar_1
    bars_api_item_17.name = u'Iced tea'
    bars_api_item_17.keywords = u'boire'
    bars_api_item_17.unit = u'verre'
    bars_api_item_17.unit_value = 0.1
    bars_api_item_17.buy_unit = u'bouteille de 2l'
    bars_api_item_17.buy_unit_value = 1.0
    bars_api_item_17.price = 2.2
    bars_api_item_17.buy_price = 1.0
    bars_api_item_17 = importer.save_or_locate(bars_api_item_17)

    bars_api_item_18 = Item()
    bars_api_item_18.bar = bars_api_bar_1
    bars_api_item_18.name = u"Jus d'orange"
    bars_api_item_18.keywords = u'd\xe9jeuner'
    bars_api_item_18.unit = u'verre'
    bars_api_item_18.unit_value = 0.2
    bars_api_item_18.buy_unit = u'l'
    bars_api_item_18.buy_unit_value = 1.0
    bars_api_item_18.price = 3.2
    bars_api_item_18.buy_price = 1.0
    bars_api_item_18 = importer.save_or_locate(bars_api_item_18)

    bars_api_item_19 = Item()
    bars_api_item_19.bar = bars_api_bar_1
    bars_api_item_19.name = u'Pizza mozarella'
    bars_api_item_19.keywords = u'fromage'
    bars_api_item_19.unit = u''
    bars_api_item_19.unit_value = 1.0
    bars_api_item_19.buy_unit = u''
    bars_api_item_19.buy_unit_value = 1.0
    bars_api_item_19.price = 3.2
    bars_api_item_19.buy_price = 1.0
    bars_api_item_19 = importer.save_or_locate(bars_api_item_19)

    # Processing model: News

    from bars_news.models import News

    bars_api_news_1 = News()
    bars_api_news_1.bar = bars_api_bar_1
    bars_api_news_1.author = bars_api_user_3
    bars_api_news_1.name = u"C'est du propre !"
    bars_api_news_1.text = u"Bar d'\xe9tage d\xe9guelasse !! Faites votre vaisselle bande de p**** !"
    bars_api_news_1.timestamp = dateutil.parser.parse("2015-01-30T02:37:14+00:00")
    bars_api_news_1 = importer.save_or_locate(bars_api_news_1)

    bars_api_news_2 = News()
    bars_api_news_2.bar = bars_api_bar_1
    bars_api_news_2.author = bars_api_user_3
    bars_api_news_2.name = u'Merci pour les photos'
    bars_api_news_2.text = u"Bravo \xe0 Yoann qui a pris le temps de mettre toutes les photos sur les murs du bar d'\xe9tage !"
    bars_api_news_2.timestamp = dateutil.parser.parse("2015-01-30T02:37:14+00:00")
    bars_api_news_2 = importer.save_or_locate(bars_api_news_2)

    # Processing model: Transaction

    from bars_transactions.models import Transaction
    from bars_transactions.models import AccountOperation
    from bars_transactions.models import ItemOperation

    for i in range(30):
        t = Transaction()
        t.bar = bars_api_bar_1
        t.author = bars_api_user_2
        t.type = u'buy'
        t = importer.save_or_locate(t)

        ao = AccountOperation()
        ao.transaction = t
        ao.fixed = False
        ao.delta = -2
        ao.target = bars_api_account_2
        ao = importer.save_or_locate(ao)

        io = ItemOperation()
        io.transaction = t
        io.delta = -1.0
        io.target = bars_api_item_2
        io = importer.save_or_locate(io)
