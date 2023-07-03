import re
import string

remove_nota = u'[’·°–!"#$%&\'()*+,-./:;<=>?@，。?★、…【】（）《》？“”‘’！[\\]^_`{|}~]+'
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def filter_str(sentence):
    sentence = re.sub(remove_nota, '', sentence)
    sentence = sentence.translate(remove_punctuation_map)
    return sentence.strip()


# 判断中日韩英
def judge_language(s):
    # s = unicode(s)   # python2需要将字符串转换为unicode编码，python3不需要
    s = filter_str(s)
    result = []
    s = re.sub('[0-9]', '', s).strip()
    # unicode english
    re_words = re.compile(u"[a-zA-Z]")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub('[a-zA-Z]', '', s).strip()
    if len(res) > 0:
        result.append("English")
    if len(res2) <= 0:
        return "English"


    # unicode chinese
    re_words = re.compile(u"[\u4e00-\u9fa5]+")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub(u"[\u4e00-\u9fa5]+", '', s).strip()
    if len(res) > 0:
        result.append("Chinese")
    if len(res2) <= 0:
        return "Chinese"

    # unicode korean
    re_words = re.compile(u"[\uac00-\ud7ff]+")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub(u"[\uac00-\ud7ff]+", '', s).strip()
    if len(res) > 0:
        result.append("Korean")
    if len(res2) <= 0:
        return "Korean"

    # unicode japanese katakana and unicode japanese hiragana
    re_words = re.compile(u"[\u30a0-\u30ff\u3040-\u309f]+")
    res = re.findall(re_words, s)  # 查询出所有的匹配字符串
    res2 = re.sub(u"[\u30a0-\u30ff\u3040-\u309f]+", '', s).strip()
    if len(res) > 0:
        result.append("Japanese")
    if len(res2) <= 0:
        return "Japanese"
    return ','.join(result)

# s1 = "汉语是世界上最优美的语言，正则表达式是一个很有用的工具"
# s2 = "正規表現は非常に役に立つツールテキストを操作することです"
# s3 = "あアいイうウえエおオ"
# s4 = "정규 표현식은 매우 유용한 도구 텍스트를 조작하는 것입니다"
# s5 = "Regular expression is a powerful tool for manipulating text."
# s6 = "Regular expression 正则表达式 あアいイうウえエおオ 정규 표현식은"
# print(judge_language(s1))
# print(judge_language(s2))
# print(judge_language(s3))
# print(judge_language(s4))
# print(judge_language(s5))
# print(judge_language(s6))