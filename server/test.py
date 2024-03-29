# import requests
# import json
# import os

# base_url = "https://www.googleapis.com/books/v1/volumes"

# # Function to fetch cover image for a book
# def get_cover_image(book_title):
#         params = {"q": book_title}
#         response = requests.get(base_url, params=params)
#         data = response.json()
#         if "items" in data:
#             for item in data["items"]:
#                 volume_info = item.get("volumeInfo", {})
#                 image_links = volume_info.get("imageLinks", {})
#                 thumbnail = image_links.get("thumbnail")
#                 if thumbnail:
#                     return thumbnail
#         return None
    
# def download_cover_image(url, filename):
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(filename, 'wb') as f:
#             f.write(response.content)
#         print(f"Cover image downloaded: {filename}")
#     else:
#         print(f"Failed to download cover image: {filename}")    

# # Example usage
# def main():
#     with open('server/books.json', 'r') as file:
#       books = json.load(file)
#     img_dir = "client/img"
#     if not os.path.exists(img_dir):
#         os.makedirs(img_dir)

#     for book in books:
#         title = book["title"]
#         author = book["author"]
#         cover_image_url = get_cover_image(f"{title} {author}")
#         if cover_image_url:
#             # Extract filename from URL
#             filename = os.path.join(img_dir, f"{title}_{author}.jpg")
#             download_cover_image(cover_image_url, filename)
#         else:
#             print(f"No cover image found for '{title}' by {author}")
            
# if __name__ == "__main__":
#     main()            

import os
import json

# Function to add cover image filename for each book
def add_cover_image_filenames(books):
    img_dir = "client/img"  # Assuming the images are in this directory
    for book in books:
        title = book["title"]
        author = book["author"]
        # Assuming the image filenames are formatted as "{title}_{author}.jpg"
        image_filename = f"{title}_{author}.jpg"
        # Check if the image file exists in the directory
        if os.path.exists(os.path.join(img_dir, image_filename)):
            book["cover_image_filename"] = image_filename

# Read books list from JSON file
def read_books_from_json(json_file):
    with open(json_file, 'r') as file:
        books = json.load(file)
    return books

# Store modified list back to the JSON file
def store_books_to_json(books, json_file):
    with open(json_file, 'w') as file:
        json.dump(books, file, indent=4)

# Main function
def main():
    json_file = "server/books.json"  # Path to your JSON file containing books data
    books = read_books_from_json(json_file)
    add_cover_image_filenames(books)
    store_books_to_json(books, json_file)
    print("Cover image filenames added and stored to the JSON file.")

if __name__ == "__main__":
    main()