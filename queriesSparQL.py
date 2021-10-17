from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context()
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

sparql = SPARQLWrapper("http://dbpedia.org/sparql")


# Method for retrieve a Dataframe with songs of the artist given in input
# Query to DBpedia with SparqlQuery
def get_dbpedia_results(artistname, year=None, bef=False, aft=False):
    if year is None:
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
        FILTER(langMatches(lang(?recordLabel_l),"en")).
        """ +
                        "BIND( '" + str(artistname) + "'" + """ AS ?name)
        FILTER (strstarts(lcase(str(?artist_l)), lcase(str(?name))))
        }
        group by ?song ?song_label ?album_name_l ?artist_l ?releaseDate
        LIMIT 5""")

    elif year is not None and bef == True:
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
        FILTER(langMatches(lang(?recordLabel_l),"en")).""" +
                        'FILTER(?releaseDate < "' + str(year) + '-01-01"^^xsd:date) ' + """
        """ +
                        "BIND( '" + str(artistname) + "'" + """ AS ?name)
        FILTER (strstarts(lcase(str(?artist_l)), lcase(str(?name))))
        }
        group by ?song ?song_label ?album_name_l ?artist_l ?releaseDate
        LIMIT 5""")

    elif year is not None and aft == True:
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
            FILTER(langMatches(lang(?recordLabel_l),"en")).""" +
                        'FILTER(?releaseDate > "' + str(year) + '-01-01"^^xsd:date) ' + """
            """ +
                        "BIND( '" + str(artistname) + "'" + """ AS ?name)
            FILTER (strstarts(lcase(str(?artist_l)), lcase(str(?name))))
            }
            group by ?song ?song_label ?album_name_l ?artist_l ?releaseDate
            LIMIT 5""")

    elif year is not None and aft == False and bef == False:
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
                FILTER(langMatches(lang(?recordLabel_l),"en")).""" +
                        'FILTER(?releaseDate > "' + str(year) + '-01-01"^^xsd:date && ?releaseDate < "' + str(
            year) + '-12-31"^^xsd:date ) ' + """
                """ +
                        "BIND( '" + str(artistname) + "'" + """ AS ?name)
                FILTER (strstarts(lcase(str(?artist_l)), lcase(str(?name))))
                }
                group by ?song ?song_label ?album_name_l ?artist_l ?releaseDate
                LIMIT 5""")

    sparql.setReturnFormat(JSON)
    query_response = sparql.query().convert()
    # print(query_response['results']['bindings'])

    # Dataframe building
    df_results = pd.DataFrame(columns=['song_title', 'album', 'year', 'artist', 'label'])

    for result in query_response['results']['bindings']:
        series = pd.Series(
            [result["song_label"]["value"], result["album_name_l"]["value"], result["releaseDate"]["value"],
             result["artist_l"]["value"], result["recordLabel_l"]["value"]],
            index=['song_title', 'album', 'year', 'artist', 'label'])
        df_results = df_results.append(series, ignore_index=True)

    return df_results

