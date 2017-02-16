# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sqlite3 as lite
con = None


class StoreInDBPipeline(object):

    def __init__(self):
        self.setupDBCon()
        self.droptestTable()
        self.createtestTable()

    def process_item(self, item, spider):
        self.storeindb(item)
        return item

    def storeindb(self, item):
        self.cur.execute("INSERT INTO test(\
        price, \
        street, \
        suburb, \
        state, \
        postcode, \
        bedroom, \
        bathroom, \
        garage, \
        land, \
        pid, \
        typeof, \
        url, \
        day, \
        lat, \
        lng \
        ) \
        VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
        item['price'],
        item['street'],
        item['suburb'],
        item['state'],
        item['postcode'],
        item['bedroom'],
        item['bathroom'],
        item['garage'],
        item['land'],
        item['pid'],
        item['typeof'],
        item['url'],
        item['day'],
        item['lat'],
        item['lng']
        ))
        self.con.commit()

    def setupDBCon(self):
        self.con = lite.connect('test.db')
        self.cur = self.con.cursor()

    def __del__(self):
        self.closeDB()

    def createtestTable(self):
        self.cur.execute("CREATE TABLE IF NOT EXISTS test(price TEXT, \
        street TEXT, \
        suburb TEXT, \
        state TEXT, \
        postcode TEXT, \
        bedroom TEXT, \
        bathroom INT, \
        garage TEXT, \
        land TEXT, \
        pid TEXT, \
        typeof TEXT, \
        url TEXT, \
        day TEXT, \
        lat TEXT, \
        lng TEXT \
        )")

    def droptestTable(self):
        self.cur.execute("DROP TABLE IF EXISTS test")

    def closeDB(self):
        self.con.close()



