import sentencepiece
from pathlib import Path
import shutil


BASE_DIR = Path("../NMT_input")
TOKEN_DIR = BASE_DIR / Path("tokenization")

TRAIN_AK = Path("train.ak")
TRAIN_TR = Path("train.tr")
TRAIN_EN = Path("train.en")
VALID_AK = Path("valid.ak")
VALID_TR = Path("valid.tr")
VALID_EN = Path("valid.en")
TEST_AK = Path("test.ak")
TEST_TR = Path("test.tr")
TEST_EN = Path("test.en")


def train_and_move(input_file, model_type, model_prefix, vocab_size):
    sentencepiece.SentencePieceTrainer.train(f'--input={input_file} --model_type={model_type} --model_prefix={model_prefix} --vocab_size={vocab_size}')

    f = model_prefix + ".model"
    shutil.move(f, TOKEN_DIR / f)
    f = model_prefix + ".vocab"
    shutil.move(f, TOKEN_DIR / f)


def train_tokenizer():
    train_and_move(BASE_DIR / TRAIN_AK, "char", "signs_char", 400)
    # train_and_move(BASE_DIR / TRAIN_AK, "bpe", "signs_bpe", 400)
    train_and_move(BASE_DIR / TRAIN_TR, "bpe", "transliteration_bpe", 1000)
    train_and_move(BASE_DIR / TRAIN_EN, "bpe", "translation_bpe", 10000)


def tokenize(model_prefix, file):
    sp = sentencepiece.SentencePieceProcessor()
    f = model_prefix + ".model"
    sp.load(str(TOKEN_DIR / f))

    with open(BASE_DIR / file, "r", encoding="utf8") as fin:
        data = fin.readlines()

    tokenized_data = [" ".join(sp.encode_as_pieces(line)) for line in data]
    #print('\n'.join(tokenized_data))

    with open(TOKEN_DIR / file, "w", encoding="utf8") as fout:
        for line in tokenized_data:
            fout.write(line + "\n")


def run_tokenizer():
    # TODO: Compare signs_chars to signs_bpe
    tokenize("signs_char", TRAIN_AK)
    tokenize("signs_char", VALID_AK)
    tokenize("signs_char", TEST_AK)

    tokenize("transliteration_bpe", TRAIN_TR)
    tokenize("transliteration_bpe", VALID_TR)
    tokenize("transliteration_bpe", TEST_TR)

    tokenize("translation_bpe", TRAIN_EN)
    tokenize("translation_bpe", VALID_EN)
    tokenize("translation_bpe", TEST_EN)


def main():
    train_tokenizer()
    run_tokenizer()


if __name__ == '__main__':
    main()
