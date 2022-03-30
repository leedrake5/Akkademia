from translate_common import translation, detokenize_translation
from translate_from_transliteration import translate_transliteration_base


def translate_transliteration(sentence):
    with open("transliteration.tmp", encoding='utf-8') as f:
        f.write(sentence)
        raw_result = translate_transliteration_base(f, True).stdout

    output = ""
    for line in raw_result.decode().split('\n'):
        if translation(line):
            output += detokenize_translation(line)

    return output


if __name__ == '__main__':
    sentence = input("Please enter a transliteration sentence for translation\n")
    print(translate_transliteration(sentence))
