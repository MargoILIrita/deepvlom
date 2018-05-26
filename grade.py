labels = ['SPEC','ANK', 'DOG', 'TREB']

right_labels = {'s1':'SPEC','s2':'SPEC', 's3':'SPEC',
                    's4':'SPEC', 's5':'SPEC', 's6':'SPEC',
                    's7':'SPEC', 's8':'SPEC', 's9':'SPEC','a1':'ANK',
                    'd1':'DOG', 'd2':'DOG', 'd3':'DOG', 'd4':'DOG', 'd5':'DOG',
                    'd6':'DOG', 'd7':'DOG', 'd8':'DOG', 'd9':'DOG', 'd10':'DOG',  't1':'TREB'}


def set_of_label(label, dict):
    result = set()
    for key, value in dict.items():
        if value == label: result.add(key)
    return result


def counF(file_names, pred, namemethod):
    print('\n\nРезультаты ' + namemethod)
    nn_labels = {file_names[i]: pred[i] for i in range(len(file_names))}
    for label in labels:
        print(label)
        set_right = set_of_label(label, right_labels)
        print('Правильный {0}'.format(set_right))
        set_clf = set_of_label(label, nn_labels)
        print('Классифицированный {0}'.format(set_clf))
        common_set = set_right.intersection(set_clf)
        print('Пересечение {0}'.format(common_set))
        try:
            r = len(common_set)/len(set_right)
            p = len(common_set)/len(set_clf)
            f = 2*p*r/(p+r)
            print('F мера для {0} = {1}\n'.format(label, f))
        except ZeroDivisionError:
            print("Метрика не распознана")

