# La funcion tiene como objetivo limpiar algunas cuestiones del texto.
# Tambien genera el formato de tipeo a tipo "Camello"
# Si hubiese una convencion para los nombre, de tablas, variables, etc. Aqui se puede incluir el formato
# Otro tema importante es el enconding del texto, aqui para generalizar esta en utf-8 pero sin acentos y si la virgulilla de la ñ

def transform(word=None, upFLetter=None, isCamel=None):
    if not isCamel:
        word = word.lower().strip()
    else:
        word = word.strip()
    word = word.replace('.', '')
    intab = "áéíóúñÁÉÍÓÚÑ"
    outtab = "aeiounAEIOUN"
    trantab = str.maketrans(intab, outtab)
    word = word.translate(trantab)
    # Convierto a camel Tiping si es posible
    if len(word.split()):
        compWord = word.split()
        if upFLetter:
            newCompWord = [compWord[0].capitalize()]
        else:
            newCompWord = [compWord[0]]
        for w in compWord[1:]:
            w = w.capitalize()
            newCompWord.append(w)
        word = ''.join([x for x in newCompWord])
    # Si upFLetter es True, convierto la primera letra a mayuscula
    elif upFLetter:
        wL = [x for x in word]
        wL[0] = wL[0].upper()
        word = ''.join([l for l in wL])
    return word

def reverseDict(d = None, retRep = False):
    if not d:
        return False
    elif type(d) != dict:
        return False
    revDic = dict()
    if retRep:
        retRep = list()
        for i in d.items():
            if i[1] in revDic:
                retRep.append(i)
                continue
            revDic.update({i[1]:i[0]})
        return (revDic, retRep)
    else:
        for i in d.items():
            revDic.update({i[1]:i[0]})
        return revDic


