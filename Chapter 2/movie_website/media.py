import webbrowser
class Movie():
    """This is a test"""
    def __init__(self,movie_title,movie_storyline,poster_image,trailer_youtube):
        """This is the constructor of Movie"""
        self.title = movie_title
        self.storyline = movie_storyline
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    def show_trailer(self):
        """This function is used to open a web browser page to play the current Movie instance's trailor"""
        wb = webbrowser.get("Safari")
        wb.open(self.trailer_youtube_url,new=2)