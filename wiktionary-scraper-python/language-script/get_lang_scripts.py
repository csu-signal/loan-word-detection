import requests
from bs4 import BeautifulSoup


class LScript:
    def __init__(self, script_name):
        self.script = script_name
        self.langs = list()

    def add_lang(self, lang):
        self.langs.append(lang)


def get_langs_scripts(link):
    lang_scripts = []
    try:
        # get list of words
        page = requests.get(link)
        soup = BeautifulSoup(page.content, 'html.parser')
        h2s = soup.find_all('h2')

        for idx, h2 in enumerate(h2s):
            h2span = h2.find('span', class_="mw-headline")
            if h2span is None:
                continue
            # elif h2span.a is None:
            #     continue
            # lang_scripts.append(h2span.a.text)
            if h2span.text == "References":
                continue
            if h2span.a is None:
                lscript_ins = LScript(h2span.text)
            else:
                lscript_ins = LScript(h2span.a.text)
            gone_to_h3 = False
            for sib in h2.find_next_siblings():
                if sib.name == 'h2':
                    break
                elif sib.name == 'h3':
                    del lscript_ins
                    h3span = sib.find('span', class_="mw-headline")
                    lscript_ins = LScript(h3span.a.text)
                    for sib_h3 in sib.find_next_siblings():
                        if sib_h3.name == 'h3' or sib_h3.name == 'h2':
                            break
                        elif sib_h3.name == 'ul':
                            lis_h3 = sib_h3.find_all('li')
                            for li_h3 in lis_h3:
                                lscript_ins.add_lang(li_h3.a.text)
                            # print("adding h3 ul languages finished for ", h3span.a.text)
                    lang_scripts.append(lscript_ins)
                    gone_to_h3 = True
                elif sib.name == 'ul' and gone_to_h3 is False:
                    lis = sib.find_all('li')
                    for li in lis:
                        lscript_ins.add_lang(li.a.text)
                    #new add
                    sibsib = sib.find_next_sibling()
                    if sibsib.name == 'h3':
                        lang_scripts.append(lscript_ins)
            if gone_to_h3 is False:
                lang_scripts.append(lscript_ins)
    except Exception as e:
        # errors can be due to timeouts/connections refused due to rate limiting. can be fixed via proxies/vpns/timeouts
        print("Error: ", e)#, " Happened for: ", h2span.a.text)
        return lang_scripts

    return lang_scripts


if __name__ == '__main__':
    wiki_link = 'https://en.wikipedia.org/wiki/List_of_languages_by_writing_system'
    l_s = get_langs_scripts(wiki_link)
    for i in l_s:
        print(i.script)
        print(len(i.langs), i.langs)

    out_file = open('language_scripts.csv', 'w')
    out_file.write("language, script\n")
    for i in l_s:
        for j in i.langs:
            out_file.write(str(j) + ', ' + str(i.script)+'\n')
