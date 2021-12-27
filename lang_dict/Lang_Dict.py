import sqlite3
import os


class Lang_Dict:
    """We pass lang_chosen, which is the requested language for usage on the webpage.
    Can be "pt", "en", "es", for portuguese, english, spanish and so on..."""
    def __init__(self, lang_chosen):
        print(os.path.join("db.sqlite3"))
        con = sqlite3.connect("..\\db.sqlite3")
        cur = con.cursor()
        cur_tmp = con
        dictionary = {}
        """language -> language id
        page_field -> page_field id
        content -> text for web page"""
        for row in cur.execute(('select page_field, content from glossary_content, '
                                'glossary_language where glossary_language.language ="' + lang_chosen +
                                '" and glossary_language.language_id = glossary_content.language')):
            #print(row)
            #print(("select page_field from glossary_field where page_field=" + "'" + str(row[0]) + "';"))
            # Get code translation for the one obtained in cursor above. Translates for the page_field field
            page_field = cur_tmp.execute(("select page_field from glossary_field where field_id=" + "'" + str(row[0]) + "';"))
            page_field = page_field.fetchone()[0]
            dictionary[str(page_field)] = row[1]
        print(dictionary)
        self.current_dict = self.select_dict(lang_chosen)

    def select_dict(self, lang_chosen):
        glossary={"a": 2}
        return glossary


if __name__ == '__main__':
    ld = Lang_Dict("en")