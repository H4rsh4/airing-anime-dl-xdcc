class Queries:
    #queries season and year in addition to everything from the current_watching query
    current_watching_anime = '''
    query($userId: Int){
        MediaListCollection(userId: $userId, type: ANIME, status: CURRENT) {
            lists {
                name
                status
                entries {
                    status
                    media{
                        id
                        title {romaji}
                        season
                        seasonYear
                        episodes
                        status
                        nextAiringEpisode {
                            episode
                        }
                    }
                }
            }
        }
    }

    '''
    current_watching = '''
    query($userId: Int){
        MediaListCollection(userId:$userId, type:ANIME, status: CURRENT){
            lists{
                name
                status
                entries {
                status
                media{
                    id
                    title{
                    romaji
                    }
                    
                    status
                    nextAiringEpisode {
                    episode
                    
                    }
                }
                }
            }
        
        }
    }
  '''
