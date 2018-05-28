import nltk
import zhenya
from ie import marks

from sklearn import svm
from nltk.classify.scikitlearn import SklearnClassifier


train_set = [([('Полянской', 'S'), ('Маргарите', 'S'), ('Игоревне', 'S')], True),
             ([('Бреславский', 'S'), ('Александр', 'S'), ('Алексеевич', 'S')], True),
             ([('Пьяных', 'S'), ('В.', 'S'), ('А.', 'S')], True),
             ([('Мятлев', 'S'), ('Е.', 'S'), ('А.', 'S')], True),
             ([('кадрам', 'S'), ('социальному', 'NNP'), ('развитию', 'S')], False),
             ([('действующего', 'JJ'), ('основании', 'S'), ('Устава', 'S')], False),
             ([('площадке', 'S'), ('Технологическая', 'S'), ('схема', 'S')], True),
             ([('Черемшанцева', 'S'), ('Леонида', 'S'), ('Дмитриевича', 'S')], True),
             ([('Лобачёв', 'S'), ('Н.', 'S'), ('В.', 'S')], True),
             ([('далее', 'JJ'), ('Заказчик', 'S'), ('лице', 'S')], False),
             ([('Кулешова', 'S'), ('Александра', 'S'), ('Петровича', 'S')], True),
             ([('Пономарева', 'S'), ('Дмитрия', 'S'), ('Николаевича', 'S')], True),
             ([('ПРОТОКОЛ', 'S'), ('РАЗНОГЛАСИЙ', 'S'), ('По', 'NN')], False),
             ([('Душко', 'S'), ('Владимира', 'S'), ('Владимировича', 'S')], True),
             ([('Иванова', 'S'), ('П.', 'S'), ('А.', 'S')], True),
             ([('№', 'RB'), ('000038715', 'CD'), ('21', 'CD')], False),
             ([('Договору', 'S'), ('№', 'NNP'), ('_______________________', 'NN')], False),
             ([('Прокофьевой', 'S'), ('И.', 'S'), ('В.', 'S')], True),
             ([('поставки', 'S'), ('№', 'CD'), ('СЗНРО/УНПОС-13-04-2018/001', 'JJ')], False),
             ([('А.', 'S'), ('П', 'INIT=abbr'), ('.', 'NONLEX')], False),
             ([('Исполнителя', 'S'), ('Все', 'S-PRO'), ('ранее', 'ADV')], False),
             ([('Кулешова', 'S'), ('Александра', 'S'), ('Петровича', 'S')], True),
             ([('М.', 'S'), ('П.', 'S'), ('М.', 'S')], False),
             ([('оплаты', 'S'), ('Покупателем', 'S'), ('Счет-договора', 'S')], False),
             ([('М.', 'S'), ('П.', 'S'), ('Приложение', 'S')], False),
             ([('Пьяных', 'A=pl'), ('Вячеслава', 'S'), ('Александровича', 'S')], True),
             ([('Ф.', 'S'), ('И.', 'S'), ('О.', 'S')], False)]


def num_wor(s):
    sum = 0
    for c in s:
        sum += ord(c)
    return  1/sum

def word_features(trig):
    return {'first_lett_up': 0 if (trig[0][0][0].isupper() ==
                             trig[1][0][0].isupper() == trig[2][0][0].isupper() == True) else 1,
            'is_all_noun': 0 if (trig[0][1] == trig[1][1] == trig[2][1] == 'S') else 1,
            'isUpper_1': 0 if trig[0][0][0].isupper() else 1,
            'isUpper_2': 0 if trig[1][0][0].isupper() else 1,
            'isUpper_3': 0 if trig[2][0][0].isupper() else 1,
            'isLower_1': 0 if trig[0][0][-1].islower() else 1,
            'isLower_2': 0 if trig[1][0][-1].islower() else 1,
            'isLower_3': 0 if trig[2][0][-1].islower() else 1,
            'isStr' : 0 if trig[0][0].isalpha() else 1,
            'word_w1':num_wor(trig[0][1]),
            'word_w2': num_wor(trig[1][1]),
            'word_w3': num_wor(trig[2][1]),
            }


def from_trigram_to_features(lst, labels=False):
    if labels:
        return [(word_features(trig), label) for (trig, label) in lst]
    return [word_features(trig) for trig in lst]


def extract_from_iter(it):
    final = []
    while True:
        try:
            final.append(next(it))
        except StopIteration:
            break
    return final


def list_of_res(lst, filename):
    return ['{0} {1} {2} {3}'.format(filename.lower() + ".txt",
                                    each[0][0].lower(),
                                    each[1][0].lower(),
                                    each[2][0].lower()) for each in lst]


if __name__ == '__main__':
    files = zhenya.get_files_name('txt')
    test_trigrams = from_trigram_to_features(train_set, True)
    clf = SklearnClassifier(svm.LinearSVC())
    clf.train(test_trigrams)
    full_res = []
    for filename in files:
        fulltext = ''
        f = open('txt/'+ filename + '.txt', 'r', encoding="utf8")
        for line in f:
            fulltext += line + '\n'
        fulltext = fulltext.replace('.', '. ')
        sentences = nltk.sent_tokenize(fulltext)
        tokenized_sentences = [nltk.word_tokenize(sentence) for sentence in sentences]
        tagged_sentences = [nltk.pos_tag(sentence,lang='rus') for sentence in tokenized_sentences]
        all_tokens = []
        for sentence in tagged_sentences:
            for tok in sentence:
                all_tokens.append(tok)
        trigr = nltk.trigrams(all_tokens)
        list_found_trigram = extract_from_iter(trigr)
        features_found = from_trigram_to_features(list_found_trigram)
        results = [list_found_trigram[i] for i in range(len(features_found)) if clf.classify(features_found[i])]
        full_res.extend(list_of_res(results, filename))
        print(filename + " ready")
    marks.countF(full_res,"Метод опорных векторов")
