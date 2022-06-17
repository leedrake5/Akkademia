import subprocess
from pathlib import Path
from translation_tokenize import tokenize
from translate_common import source, translation, detokenize_transliteration, detokenize_translation


def organize_transliteration_line(line):
    return line


def organize_transliteration_input(file):
    tmp_file_name = "tmp_" + file
    tmp_file = open(tmp_file_name, "w", encoding="utf8")

    with open(file, "r", encoding="utf8"):
        for line in file:
            tmp_file.write(organize_transliteration_line(line))

    tmp_file.close()
    return tmp_file_name


def translate_transliteration_base(file, capture_output=False):
    tmp_file = organize_transliteration_input(file)
    tokenize("transliteration_bpe", tmp_file, False, Path("NMT_input/tokenization"), Path(""), Path("/tmp"))
    cmd = "../fairseq/fairseq_cli/interactive.py " \
          "data-bin-transliteration/ " \
          "--path trans_result.LR_0.1.MAX_TOKENS_4000/checkpoint_best.pt " \
          "--beam 5 " \
          "--input /tmp/" + tmp_file

    if capture_output:
        return subprocess.run(cmd.split(), capture_output=True)
    return subprocess.run(cmd.split())


def translate_transliteration_raw(file):
    translate_transliteration_base(file)


def translate_transliteration_file(file):
    raw_result = translate_transliteration_base(file, True).stdout
    for line in raw_result.decode().split('\n'):
        if source(line):
            print(detokenize_transliteration(line))
        if translation(line):
            print(detokenize_translation(line, True) + "\n")


if __name__ == '__main__':
    transliteration_file = input("Please enter the name of the transliteration file for translation\n")
    translate_transliteration_file(transliteration_file)