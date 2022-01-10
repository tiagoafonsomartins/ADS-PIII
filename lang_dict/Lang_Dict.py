import sqlite3
import os
from ads_app.models import *
from django_ads.wsgi import *
from . import *
class Lang_Dict:
    '''
    Object used to retrieve information about the HTML fields in the current language
    We filter the contents by language and create a dictionary based on this result
    Then, we place said dictionary as an attribute of the object Lang_Dict so as to access it later
    '''
    def __init__(self, lang_chosen):
        # ID of given language, if it exists. If not, default to English
        try:
            lang = GlossaryLanguage.objects.get(language=lang_chosen).id
        except:
            lang = GlossaryLanguage.objects.get(language="en").id

        # Retrieve information about fields, filtered by the given language
        gloss = GlossaryContent.objects.filter(language=lang)
        dictionary = {}
        for query in gloss:
            # Get field from the resulting list of Content and add to dictionary
            field_tmp = GlossaryField.objects.get(id=query.page_field).page_field
            dictionary[field_tmp] = query.content
        self.dictionary = dictionary

''' LEGACY VERSION - Initial concept
# Here we used direct SQL commands to execute onto the DB. We noticed this didn't work,
# So the alternative was the construction of models, in ads_app/models.py, and we use them here
# Creating QuerySets of the objects we want
    def __init__(self, lang_chosen):
        gloss = GlossaryContent.objects.filter(id=1)
        print(gloss)
        print("CONTENTE" + gloss[0].content)
        print(os.path.join("db.sqlite3"))
        con = sqlite3.connect("..\\db.sqlite3")
        print(con)
        cur = con.cursor()
        cur_tmp = con
        dictionary = {}

        """language -> language id
        page_field -> page_field id
        content -> text for web page"""
        for row in cur.execute(('select page_field, content from glossary_content, '
                                'glossary_language where glossary_language.language ="' + lang_chosen +
                                '" and glossary_language.id = glossary_content.language')):
            #print(row)
            #print(("select page_field from glossary_field where page_field=" + "'" + str(row[0]) + "';"))
            # Get code translation for the one obtained in cursor above. Translates for the page_field field
            page_field = cur_tmp.execute(("select page_field from glossary_field where glossary_field.id=" + "'" + str(row[0]) + "';"))
            page_field = page_field.fetchone()[0]
            dictionary[str(page_field)] = row[1]
        print(dictionary)
        self.current_dict = self.select_dict(lang_chosen)

    def select_dict(self, lang_chosen):
        glossary={"a": 2}
        return glossary
'''

'''if __name__ == '__main__':
    ld = Lang_Dict("pt")'''