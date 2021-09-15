import json

from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

sparql = SPARQLWrapper("http://dbpedia.org/sparql")


def get_dbpedia_results(artistname):
    sparql.setQuery("""select distinct
    ?song
    (replace(?song_label ,"en","","") as ?song_label )
    (replace(?album_name_l ,"en","","") as ?album_name_l )
    (replace(?artist_l ,"en","","") as ?artist_l )
    (max(?releaseDate) as ?releaseDate)
    (GROUP_CONCAT( distinct ?genre_l;SEPARATOR=",") AS ?genre_l)
    (GROUP_CONCAT(?recordLabel_l;SEPARATOR=",") AS ?recordLabel_l)
    where
    {
    ?song a dbo:Single .
    ?song rdfs:label ?song_label.
    
    ?song dbo:album ?album_name.
    ?album_name rdfs:label ?album_name_l.
    
    ?song dbo:artist ?artist.
    ?artist rdfs:label ?artist_l.
    
    ?song dbo:genre ?genre.
    ?genre rdfs:label ?genre_l.
    
    ?song dbo:recordLabel ?recordLabel.
    ?recordLabel rdfs:label ?recordLabel_l.
    
    ?song dbo:releaseDate ?releaseDate.
    FILTER(langMatches(lang(?song_label),"en")).
    FILTER(langMatches(lang(?album_name_l),"en")).
    FILTER(langMatches(lang(?artist_l),"en")).
    FILTER(langMatches(lang(?genre_l),"en")).
    FILTER(langMatches(lang(?recordLabel_l),"en"))."""+
    "BIND( '" + str(artistname)+"'"+""" AS ?name)
    FILTER (strstarts(lcase(str(?artist_l)), lcase(str(?name))))
    }
    group by ?song ?song_label ?album_name_l ?artist_l ?releaseDate
    LIMIT 10""")

    sparql.setReturnFormat(JSON)
    query_response = sparql.query().convert()
    # print(query_response['results']['bindings'])

    df_results = pd.DataFrame(columns=['song_title', 'album', 'year', 'artist', 'label'])

    for result in query_response['results']['bindings']:
        series = pd.Series([result["song_label"]["value"], result["album_name_l"]["value"] , result["releaseDate"]["value"],
                            result["artist_l"]["value"], result["recordLabel_l"]["value"]], index = ['song_title', 'album', 'year', 'artist', 'label'] )
        df_results = df_results.append(series, ignore_index=True)

    return df_results

print(get_dbpedia_results("Blonde Redhead"))