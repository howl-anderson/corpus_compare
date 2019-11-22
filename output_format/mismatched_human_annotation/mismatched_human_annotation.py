import copy
import csv
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
    output_file = output_file_without_ext.with_suffix(".csv")
    with output_file.open("wt") as fd:
        csv_writer = csv.writer(fd)

        for gold_doc, _ in mismatch_pair:
            csv_writer.writerow(["".join(gold_doc.text), gold_doc.function, gold_doc.intent, gold_doc.sub_function])
