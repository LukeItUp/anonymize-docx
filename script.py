
import sys
import os
import subprocess
import stanfordnlp


documents = ["./example/anonymization-example.docx"]  # Example


def parse_docx(document):
    tmp = "{0:s}.txt".format(document[:-5])
    subprocess.run(["docx2txt", document])

    with open(tmp) as f:
        lines = f.readlines()
    os.remove(tmp)

    output_str = ""
    for line in lines:
        output_str += line.strip()
    return output_str


def anonymize(text):
    nlp = stanfordnlp.Pipeline(lang='sl', models_dir=".")
    doc = nlp(text)
    
    for sentence in doc.sentences:
        # sentence.print_dependencies()
        # sentence.print_words()
        print("Sentence:")

        for word in sentence.words:
            print("Word:       {0:s}".format( word.text ))
            print("Lemma:      {0:s}".format( word.lemma ))
            print("Dependency: {0:s}".format( word.dependency_relation ))
            print("Features:   {0:s}".format( word.feats ))
            print("pos:        {0:s}".format( word.pos ))
            print("upos:       {0:s}".format( word.upos ))
            print("xpos:       {0:s}".format( word.xpos ))
            print("\n----")

        print("--------------------")


if __name__ == '__main__':
    if sys.argv[1] == "setup":
        print("Please install models in project directory.")
        stanfordnlp.download("sl")

    if len(sys.argv) == 1:
        print("Running example document")
    else:
        documents = sys.argv[1:]

    for doc in documents:
        print("File:", doc)

        print("Parsing docx")
        text = parse_docx(doc)

        print("Anonymize")
        anonymize(text)

        