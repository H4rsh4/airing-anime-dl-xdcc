class Queries:
    current_watching_ids = '''
    query{
        MediaListCollection(userId:5540925, type:ANIME, status: CURRENT){
            lists{
            entries {
                media{
                id
                nextAiringEpisode {
                    id
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
