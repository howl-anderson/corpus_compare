import copy
from pathlib import Path
from typing import Tuple, List

from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.sequence import Sequence


def convert_to_md(doc) -> str:
    text_list = copy.deepcopy(doc.text)

    for span in doc.span_set:
        text_list[span.start] = "[" + text_list[span.start]
        text_list[span.end - 1] = text_list[span.end - 1] + "]({})".format(span.entity)

    return " ".join(text_list)


def write_compare_to_file(
    corpus_count: int,
    mismatch_count: int,
    mismatch_pair: List[Tuple[Document, Sequence]],
    output_file_without_ext: Path,
):
    output_file = output_file_without_ext.with_suffix(".txt")

    head_line = "语料数量：{}, 匹配数量：{}, 不匹配数量：{}, 不匹配比例：{}".format(
        corpus_count,
        corpus_count - mismatch_count,
        mismatch_count,
        mismatch_count / corpus_count,
    )

    row_head = ">>> 人工标记结果" + "\n" + ">>> 机器预测结果"

    row_string_list = []
    for gold_doc, predict_doc in mismatch_pair:
        row_string = "{!s}\n{!s}".format(
            gold_doc.convert_to_md(), convert_to_md(predict_doc)
        )
        row_string_list.append(row_string)

    with output_file.open("wt") as fd:
        fd.write("\n\n".join([head_line, row_head]))
        fd.write("\n\n")
        fd.write("\n\n".join(row_string_list))
