#!/usr/bin/env python2

class Finding():

    def __init__(self, description, entity, callback, callback_args, level, questions):
        self.description = description
        self.level = level
        self.entity = entity
        self.callback = callback
        self.callback_args = callback_args
        self.level = level
        self.questions = questions
        self.items = []
        self.macro_items = []

    def addItem(self, item, macro_item = None):
        self.items.append(item);
        if macro_item:
            self.macro_items.append(macro_item);

    def removeItem(self, item, macro_item = None):
        try:
            target = self.items.index(item)
            del self.items[target]
            if macro_item:
                del self.macro_items[target]
        except Exception, e:
            print e
            pass

    # arg0: limit
    # arg1: object attribute to count
    # arg2: condition attribute
    # arg3: condition value
    def hasMoreThan(self, key, obj):
        limit = self.callback_args[0]
        attribute = self.callback_args[1]
        condition_attr = self.callback_args[2]
        condition_val = self.callback_args[3]
        found_objects = [o for o in obj[attribute] if o[condition_attr] == condition_val]
        if len(found_objects) > int(limit):
            self.addItem(key)

    # arg0: object attribute to check
    def isNotNull(self, key, obj):
        attribute = self.callback_args[0]
        if attribute in obj:
            if obj[attribute]:
                self.addItem(key)
