import media
import fresh_tomatoes

toy_story = media.Movie("Toy Story",
                        "A story of a boy and his toys that come to life",
                        "http://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
                        "https://www.youtube.com/watch?v=KYz2wyBy3kc")
#print toy_story.storyline
avatar = media.Movie("Avatar",
                     "A marine on an alien planet",
                     r"https://en.wikipedia.org/wiki/Avatar_(2009_film)#/media/File:Avatar-Teaser-Poster.jpg",
                     r"https://www.youtube.com/watch?v=5PSNL1qE6VY")
print avatar.storyline
#avatar.show_trailer()
school_of_rock = media.Movie("School of Rock",
                             "Using rock music to learn",
                             "http://upload.wikimedia.org/wikipedia/en/1/11/School_of_Rock_Poster.jpg",
                             "https://www.youtube.com/watch?v=3PsUJFEBC74")
rataouille = media.Movie("Ratatouille",
                         "A rat is a chef in Paris",
                         "http://upload.wikimedia.org/wikipedia/en/5/50/RatatouillePoster.jpg",
                         "https://www.youtube.com/watch?v=c3sBBRxDAqk")
midnight_in_paris = media.Movie("Midnight in Paris",
                                "Going back in time to meet authors",
                                r"http://upload/wikimedia.org/wikipedia/en/9/9f/Midnight_in_Paris_Poster.jpg",
                                r"https://www.youtube.com/watch?v=atLg2wQQxvU")
hunger_games = media.Movie("Hunger Games",
                           "A really real reality show",
                           r"http://upload.wikimedia.org/wikipedia/en/4/42/HungerGamesPoster.jpg",
                           r"https://www.youtube.com/watch?v=PbA63a7H0bo")


# fresh_tomatoes.open_movies_page([toy_story,avatar,school_of_rock,
#                                 rataouille,midnight_in_paris,hunger_games])

print media.Movie.__name__
print media.Movie.__module__
print media.Movie.__doc__
