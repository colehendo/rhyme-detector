# rhyme-detector

## Description
This rhyme detector is built based on Genius Lyrics' [Check the Rhyme](https://genius.com/shows/ctr), and leverages their API for lyrics. The code retrieves the lyrics of a specified song, detects the rhymes within based on the [CMU Pronouncing Dictionary](https://en.wikipedia.org/wiki/CMU_Pronouncing_Dictionary), and outputs a highlighted rhyming pattern.


## Usage
### Install Necessary Packages
```
pip install -r requirements.txt
```

### Run the Rhyme Detector
Note, results are more accurate if an artist is provided.

Example 1:
```
python main.py --song 'bohemian rhapsody'
```

Example 2:
```
python main.py --song 'hey jude' --artist 'the beatles'
```


## Future Improvements
* Replace text ingestion with audio
    * Many rhyme schemes are aided by specific pronunciations and cadances. Dissecting a rhyme scheme by ingesting an audio file of the song instead of a text file of its lyrics will allow for much more accurate rhyme detection, allowing this tool to match the accuracy of Genius Lyrics' [Check the Rhyme](https://genius.com/shows/ctr)
* Improve song search results
    * Genius Lyrics' API results are flimsy at best when requesting a song. A proper search tool needs to be built around 
* Separate verses from choruses
    * This will speed up processing time, as well as improve accuracy of rhyme schemes by virtue of section separation as intended by the artist
* Remove non-rhyming sections such as intros and outros
    * Although these should be included in outputted lyrics, they should not be considered a part of the rhyme scheme
