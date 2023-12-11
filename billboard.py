from bs4 import BeautifulSoup
import requests

class BillBoard:
    def __init__(self):
        self.BILLBOARD_URL = "https://www.billboard.com/charts/hot-100/"

    def get_songs(self, time):
        """
        Retrieves the top 100 songs from a specified time on the Billboard website.

        Args:
            time (str): The time parameter used to construct the URL for the Billboard website.

        Returns:
            dict: A dictionary containing the track names as keys and corresponding artist names as values.

        """
        # Construct the URL using the provided time parameter
        url = self.BILLBOARD_URL + time

        # Send a GET request to the URL and retrieve the HTML content
        response = requests.get(url)
        website_html = response.text

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(website_html, "html.parser")

        # Find all list items with the class name "o-chart-results-list__item"
        top_100 = soup.find_all("li", class_="o-chart-results-list__item")

        # Initialize an empty dictionary to store the track names and artist names
        track_list = {}

        # Iterate through each item in the top 100 list
        for item in top_100:
            # Find the <h3> and <span> elements within the item
            h3_element = item.find("h3")
            span_element = item.find("span")

            # Check if the <h3> element exists,
            # because there are some list items that are not on the 100 list.
            if h3_element is not None:
                # Extract the artist name from the <span> element
                artist = span_element.get_text().strip()

                # Remove "Featuring" from the artist name if present and additional artists after "&" if present
                # This is done because the artists are separated by comma in spotify and if searched with
                # featuring & it does not find anything
                if "Featuring" in artist:
                    artist = artist.split("Featuring")[0]
                elif "&" in artist:
                    artist = artist.split("&")[0]

                # Extract the track name from the <h3> element
                track = h3_element.get_text().strip()
                # Add the track name and artist name to the track_list dictionary
                track_list[track] = artist
        # Print the number of songs in the list
        print(f"there are {len(track_list)} songs in the list")
        # Print the track list dictionary
        print(track_list)

        # Return the track_list dictionary
        return track_list
