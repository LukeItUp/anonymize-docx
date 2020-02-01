import sys
import os
import subprocess
import stanfordnlp


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


def read_names(file):
    out = []
    with open(file, 'r') as f:
        for line in f:
            out.append(line.lower().strip())
    return out


def show(text):
    nlp = stanfordnlp.Pipeline(lang='sl', models_dir=".")
    doc = nlp(text)

    for sentence in doc.sentences:
        # sentence.print_dependencies()
        # sentence.print_words()
        print("Sentence:")

        for word in sentence.words:
            print("Word:       {0:s}".format(word.text))
            print("Lemma:      {0:s}".format(word.lemma))
            print("Dependency: {0:s}".format(word.dependency_relation))
            print("Features:   {0:s}".format(word.feats))
            print("pos:        {0:s}".format(word.pos))
            print("upos:       {0:s}".format(word.upos))
            print("xpos:       {0:s}".format(word.xpos))
            print("\n----")

        print("--------------------")


def anonymize(text, names):
    nlp = stanfordnlp.Pipeline(lang='sl', models_dir=".")
    doc = nlp(text)
    out = ""

    for sentence in doc.sentences:
        for word in sentence.words:
            lemma = word.lemma.strip().lower()
            if lemma in names:
                out += " <NAME {0:s}>".format(word.feats)
            else:
                out += " " + word.text

    print("Anonymized text:")
    print(out)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == "setup":
        print("\n-!!!- When asked, please install models in project directory (.) -!!!-")
        stanfordnlp.download("sl")
        sys.exit()

    if len(sys.argv) == 1:
        # Example
        print("Running example document.")
        docx_file = "./example/anonymization-example.docx"
        names = "./example/to-anonymize2.txt"
    else:
        docx_file = sys.argv[1]
        names = sys.argv[2]

        print("File to anonymize: {0:s}".format(docx_file))
        print("Names to anonymize: {0:s}".format(names))

    names = read_names(names)
    text = parse_docx(docx_file)

    anonymize(text, names)
