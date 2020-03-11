# Search Engine

## The project for the Information Retrieval course

### Salo Maxim, 3rd year Bachelor

Application consist of 4 endpoints:
* GET `/search`, which takes `query` as a request parameter and perform the search
* POST `/songs`, which takes `song_url` as a request parameter and add new song to the search engine
* DELETE `/songs`, which takes `song_url` as a request parameter and remove the given song from the search engine
* PATCH `/index`, which merge the AUX index from the RAM with the in-disk index
