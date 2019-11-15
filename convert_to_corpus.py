from pathlib import Path

import jsonlines

from tokenizer_tools.tagset.offset.corpus import Corpus
from tokenizer_tools.tagset.offset.document import Document
from tokenizer_tools.tagset.offset.span import Span
from tokenizer_tools.tagset.offset.span_set import SpanSet


def read_data(data_path):
    data_path = Path(data_path)

    doc_list = []

    for data_file in data_path.glob("*.json"):
        with jsonlines.open(str(data_file)) as reader:
            for obj in reader:
                text = [i for i in obj["content"]]
                doc = Document(text)
                doc.sub_function = obj["childFunction"]
                doc.domain = obj["domain"]
                doc.function = obj["function"]
                doc.intent = obj["intent"]

                span_list = []
                for entity in obj["marked"]:
                    record = entity["record"]
                    if not record:
                        continue

                    start = int(record[0])
                    end = int(record[-1]) + 1
                    entity_type = entity["titleIndex"]

                    span = Span(start, end, entity_type)

                    span_list.append(span)

                entities = SpanSet(span_list)

                doc.entities = entities

                doc_list.append(doc)

    corpus = Corpus(doc_list)
    corpus.write_to_file("data.conllx")


if __name__ == "__main__":
    read_data("./data")
