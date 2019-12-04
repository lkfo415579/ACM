import sys
#import xlrd
import re
import pkuseg
import glob

seg = pkuseg.pkuseg()
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr|Prof|No)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu)"


def token_en(sent):
    text = nlp(sent.strip())
    tokens = [tok.text for tok in text]
    return ' '.join(tokens)

def token_zh(sent):
    tokens = seg.cut(sent)
    return ' '.join(tokens)


def cut_sent_zh(para):
    para = re.sub('([。！？；;\?])([^”’])', r"\1\n\2", para)
    # para = re.sub(r'(\:)(\s*\d)', r"\1\n\2", para)
    para = re.sub('(\.{6})([^”’])', r"\1\n\2", para)
    para = re.sub('(\…{2})([^”’])', r"\1\n\2", para)
    para = re.sub('([。！；;\！？\?][”’])([^，。！？\?])', r'\1\n\2', para)
    para = para.rstrip()
    return re.split("\n+",para)

def cut_sent_en(text):

    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    text = text.replace("i.e.", "i<prd>e<prd>")
    text = text.replace("e.g.", "e<prd>g<prd>")
    # text = text.replace("etc.", "etc<prd>")
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    if "..." in text: text = text.replace("...", "<prd><prd><prd>")
    text = re.sub(r'(\d)(\.)(\d)', "\\1<prd>\\3", text)
    text = re.sub(r'(\s\d{,2}\s*)(\.)([^\d])', "\\1<prd>\\3", text)
    #text = re.sub(r'([\s\d{,2}|^\d{,2}]\s*)(\.)([^\d])', "\\1<prd>\\3", text)
    # text = re.sub(r'(\:)(\s*1\s*<prd>)', "\\1<stop>\\2", text)

    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace(";",";<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences



def read_excel(f_xlsx):
    workbook = xlrd.open_workbook(f_xlsx)
    worksheet = workbook.sheet_by_index(0)  # 第1个表
    col1 = []
    col2 = []
    for row in range(1, worksheet.nrows):
        col1.append((worksheet.cell_value(row, 2)))  # 第3列
        col2.append((worksheet.cell_value(row, 3)))  # 第4列
    # print(len(col1))
    # print(len(col2))
    assert (len(col1) == len(col2))
    return col1, col2
def read_txt(text1, text2):
    col1 = open(text1, 'r', encoding='utf-8').readlines()
    col2 = open(text2, 'r', encoding='utf-8').readlines()
    # print(len(col1))
    # print(len(col2))
    assert len(col1) == len(col2)
    return col1, col2

def processing_zh(doc, typ):
    doc = re.sub('\r', '', doc)
    # tmp_zh = '\n'.join(para)
    #print(doc)
    #if '.docx' in typ:
    paras = re.split(r'\n{1,}', doc)
    #else:
    #    paras = re.split(r'\n{2,}', doc)
    print(len(paras))
    result = []
    for para in paras:
        para = re.sub(r'\n', ' ', para)
        para = para.strip()
        if para == '':
            continue
        lines = cut_sent_zh(para)
        for sen in lines:
            result.append(token_zh(sen) + '\n')
    return result

def processing_en(doc, typ):
    #if '.docx' in typ:
    doc = re.sub('\r', '', doc)
    paras = re.split(r'\n{1,}', doc)
    #else:
    #    paras = re.split(r'\n{2,}', doc)
    # lines = tmp_en.split('\n')
    print(len(paras))
    result = []
    for para in paras:
        para = re.sub(r'\n', ' ', para)
        para = para.strip()
        #print(para)
        #print('--------')
        if para == '':
            continue
        lines = cut_sent_en(para)
        for sen in lines:
            result.append(sen + '\n')
    return result

if __name__ == '__main__':
    files = glob.glob(sys.argv[1] + '/*.txt')
    lang = sys.argv[2]
    for ele in files:
        print(ele)
        tmp = open(ele, 'r', encoding='utf-8').read()
        if lang == 'zh':
            out = open(ele.split('_')[0] + '_' + lang +'.snt', 'w', encoding='utf-8')
            result = processing_zh(tmp, ele)
            out.writelines(result)
            out.close()
        elif lang == 'en':
            out = open(ele.split('_')[0] + '_' + lang, 'w', encoding='utf-8')
            result = processing_en(tmp, ele)
            out.writelines(result)
            out.close()

