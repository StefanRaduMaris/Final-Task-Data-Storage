#import libraries

import pandas as pd
import requests
from pprint import pprint 
from time import *
#creatin a function that will make request with the info that we need

def searching_information_in_api(title,year,plot='full'):


    apikey='265f92cf'
    search_parameters = {
        't':title,
        'y':year
    }
    #making the url how we need
    url = f'http://www.omdbapi.com/?apikey={apikey}&{search_parameters}'
    
    #the next part is E from ETL we need to extract the info and to found solution for the errors
    try:
        reponse = requests.get(url,params=search_parameters)
        #print(reponse.status_code)
        informatie_api = reponse.json()
        
        # print(type(informatie_api))
        #print(informatie_api.keys())
        # print(type(informatie_api['imdbRating']))

        if reponse.status_code != 200:
            print(f'Error , {reponse.status_code}')

        elif reponse.status_code == 200:
            
           
            actors_found = ''
            rating_found = ''
            votes_found = '' 

            if "Actors" in informatie_api:
                actors_found = informatie_api["Actors"]
            else:
                actors_found=''

            if "imdbRating" in informatie_api:
                rating_found = informatie_api["imdbRating"]
            else:
                rating_found = ''

            if "imdbVotes" in informatie_api:
                votes_found = informatie_api["imdbVotes"]
            else:
                votes_found=''

            # print('[Info] We have the info ')
            
#             pprint(f'''Actors : {actors_found}
#                       Rating : {rating_found}
#                       Votes : {votes_found}

#  ''')     
            return {
                'actors_found':actors_found,
                'rating_found':rating_found,
                'votes_found':votes_found
                }
        
        else :
            print('Movie not found')
            return {
                'actors_found':"We don`t have this information",
                'rating_found':"We don`t have this inforation",
                'votes_found':"We don`t have this inforation"
                }
            

    except requests.exceptions.ConnectionError:

        print("Error: The server is unavailable or the URL is invalid.")

    except requests.exceptions.Timeout:
 
        print("Error: The request has timed out.")

    except requests.exceptions.RequestException as e:

        print(f"Request error: {e}")

    except Exception as e:

        print(f"Unexpected error:: {e}")
    #using panda we are reading the csv file that we have , we need to convert our data to get the right info
d =pd.read_csv('movies.csv')
#first we have to create d['Actors]
d['Actors'] = ''
#and after that we can convert it how we need
d['Actors']=d['Actors'].astype(str)
d['Rating']=''
d['Rating'] =d['Rating'].astype(str)
d['Votes']=''
d['Votes'] = d['Votes'].astype(str)

# print(d.keys())
# print(d.dtypes)

for index,row in d.iterrows():
    data_receive_from_api = searching_information_in_api(str(row['title']).strip(),row['release_year'])
    if data_receive_from_api['actors_found'] is not None:
        d.at[index,'Actors']=data_receive_from_api['actors_found']
    else:
        d.at[index,'Actors'] = " "
    if data_receive_from_api['rating_found'] is not None:
        d.at[index,'Rating'] = data_receive_from_api['rating_found']
    else:
        d.at[index,'Rating'] = ' '
    if data_receive_from_api['votes_found'] is not None:
        d.at[index,'Votes'] = data_receive_from_api['votes_found']
    else:
        d.at[index,'Votes'] = ' '
d.to_xml('Movies.xml', parser='etree', row_name='Movie', index=True,
          elem_cols=['title', 'release_year', 'genre', 'director', 'country', 'duration','Actors', 'Rating', 'Votes'])