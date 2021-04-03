"""Example of using stanza model."""
import spacy
import stanza
from TRUNAJOD.entity_grid import EntityGrid
from TRUNAJOD.ttr import lexical_diversity_mtld
from TRUNAJOD.ttr import one_side_lexical_diversity_mtld

# Load spaCy model
nlp = spacy.load("es_core_news_sm")

# Load stanza model
nlp_s = stanza.Pipeline("es", use_gpu=False)

# Example
example_text = (
    "El espectáculo del cielo nocturno cautiva la mirada y suscita preguntas"
    "sobre el universo, su origen y su funcionamiento. No es sorprendente que "
    "todas las civilizaciones y culturas hayan formado sus propias "
    "cosmologías. Unas relatan, por ejemplo, que el universo ha"
    "sido siempre tal como es, con ciclos que inmutablemente se repiten; "
    "otras explican que este universo ha tenido un principio, "
    "que ha aparecido por obra creadora de una divinidad."
)

# Create Doc
doc = nlp(example_text)
doc_s = nlp_s(example_text)

# TTR Check - change TTR import to test
print("spacy result: ", lexical_diversity_mtld(doc))
# or
# print("spacy result: ", lexical_diversity_mtld(doc, model_name="spacy"))
print("stanza result: ", lexical_diversity_mtld(doc_s, model_name="stanza"))

# Entity Grid Check
egrid = EntityGrid(doc)
egrid_s = EntityGrid(doc_s, model_name="stanza")

print("spacy Entity grid:")
print(egrid.get_egrid())

print("stanza Entity grid:")
print(egrid_s.get_egrid())
