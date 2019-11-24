# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb

class PdffindPipeline(object):
        def __init__(self):
            print("Opening MySQL connection")
            self.conn = MySQLdb.connect('host', 'user', 'pass',
                                        'DB',charset="utf8",use_unicode=True)
            self.cursor = self.conn.cursor()

        def process_item(self, item, spider):
            try:
                self.cursor.execute("""INSERT INTO PAGINAS(TEXTO) VALUES (%s);""",(item['edicto'],))
                self.conn.commit()
                self.cursor.execute("""CALL `LEER`()""")
                self.conn.commit()
                self.cursor.execute("""INSERT INTO BOT.PAGINAS(TEXTO) VALUES (%s);""",(item['edicto'],))
                self.conn.commit()
            except MySQLdb.Error:
                e = sys.exc_info()[1]
            return item

