import sparql
from SPARQLWrapper import SPARQLWrapper, JSON
s = SPARQLWrapper("http://dbpedia.org/sparql")

def queryMeth():
    sparql.setQuery("""
        PREFIX dbpedia: <http://dbpedia.org/resource/>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX dc: <http://purl.org/dc/elements/1.1/>
        PREFIX mo: <http://purl.org/ontology/mo/>
        SELECT ?label
        WHERE { <http://dbpedia.org/resource/Asturias> rdfs:label ?label }
    
    """)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()

    for result in results["results"]["bindings"]:
        print(result["label"]["value"])