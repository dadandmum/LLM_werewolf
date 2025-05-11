

class LanguageDict:
    
    lang_dict={
        'EN':
            {
                'default':'',
                'at':'at',
                'say':'say',
            },
        'CN':
            {
                'default':'',
                'at':'在',
                'say':'说',
            }
    }
    
    
    @staticmethod
    def translate(word,to_lang):
        if not(to_lang in LanguageDict.lang_dict ):
            to_lang='EN'
        if not(word in LanguageDict.lang_dict[to_lang]):
            word='default'
        return LanguageDict.lang_dict[to_lang][word]