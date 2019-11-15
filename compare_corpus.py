import copy
import os
from pathlib import Path

from tokenizer_tools.tagset.offset.corpus import Corpus
from deliverable_model.serving import SimpleModelInference

smi = SimpleModelInference("./model/deliverable_model")


def convert_to_md(doc) -> str:
    text_list = copy.deepcopy(doc.text)

    for span in doc.span_set:
        text_list[span.start] = "[" + text_list[span.start]
        text_list[span.end - 1] = text_list[span.end - 1] + "]({})".format(
            span.entity
        )

    return " ".join(text_list)


def corpus_compare(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    for corpus_file in input_dir.glob("*.conllx"):
        output_file_basename = os.path.splitext(corpus_file.parts[-1])[0] + ".txt"
        output_file = output_dir / output_file_basename

        corpus = Corpus.read_from_file(corpus_file)

        corpus_count = len(corpus)
        mismatch_count = 0
        mismatch_pair = []

        predict_info_list = list(smi.parse(["".join(i.text) for i in corpus]))

        doc_list = [i.sequence for i in predict_info_list]

        predict_corpus = Corpus(doc_list)
        for gold_doc, predict_doc in zip(corpus, predict_corpus):
            if gold_doc.compare_entities(predict_doc):
                continue

            mismatch_count += 1

            mismatch_pair.append((gold_doc, predict_doc))

        head_line = "语料数量：{}, 匹配数量：{}, 不匹配数量：{}, 不匹配比例：{}".format(
            corpus_count,
            corpus_count - mismatch_count,
            mismatch_count,
            mismatch_count / corpus_count,
        )

        row_head = ">>> 人工标记结果" + "\n" + ">>> 机器预测结果"

        row_string_list = []
        for gold_doc, predict_doc in mismatch_pair:
            row_string = "{!s}\n{!s}".format(gold_doc.convert_to_md(), convert_to_md(predict_doc))
            row_string_list.append(row_string)

        with output_file.open("wt") as fd:
            fd.write("\n\n".join([head_line, row_head]))
            fd.write("\n\n")
            fd.write("\n\n".join(row_string_list))


if __name__ == "__main__":
    corpus_compare("./domain_data", "./report")
