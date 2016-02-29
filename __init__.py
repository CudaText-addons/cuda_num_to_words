import os
import string
from cudatext import *
from .word_proc import *
from .num2words import num2words, CONVERTER_CLASSES as langs

ini_fn = 'cuda_numtowords.ini'
ini_section = 'op'
ini_key_lang = 'lang'


def do_num_words(mode):
    x0, y0, nlen, text = get_word_info()
    if not text:
        msg_status('Place caret under number')
        return
                   
    try:            
        num = int(text)
    except:
        try:
            text = text.replace(',', '.')
            num = float(text)
        except:
            msg_status('Place caret under number')
            return

    lang = ini_read(ini_fn, ini_section, ini_key_lang, 'en')

    text = num2words(num, lang=lang)
    if not text: return

    if mode=='newtab':
        file_open('')
        ed.insert(0, 0, text)
    elif mode=='replace':
        ed.set_caret(x0, y0)
        ed.delete(x0, y0, x0+nlen, y0)
        ed.insert(x0, y0, text)
    else:
        raise Exception('Mode?')
            

class Command:
    def num_new_tab(self):
        do_num_words('newtab')
    def num_replace(self):
        do_num_words('replace')

    def langs(self):
        items = sorted(list(langs.keys()))
        n = dlg_menu(MENU_LIST, '\n'.join(items))
        if n is None: return
        ini_write(ini_fn, ini_section, ini_key_lang, items[n])
