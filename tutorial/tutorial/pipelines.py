# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from scrapy.exceptions import DropItem
from tutorial.models import AppMetadata, db_connect, create_table
import logging
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
"""
Pipeline to save item to database

"""
class SaveAppPipeline(object):
    def __init__(self):
        """
        Initializes database connection and sessionmaker
        Creates App Metadata table
        """
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)
    
    def process_item(self, item, spider):
        """
        Save app Metadata to the database
        This method is called for every item pipeline component
        """
        session = self.Session()
        app = AppMetadata()
        app.url = item['link'][0]
        app.titleXpath = item['path_title'][0]
        app.title = item['title'][0]
        app.developer = item['developer'][0]
        try:
            if len(app.title):
                logging.info("Adding App")
                session.add(app)
                session.commit()
                logging.info("App Added")
            else:
                DropItem("This is not an app")
        except:
            raise DropItem("Can't add item")
        