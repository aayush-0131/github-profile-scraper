import requests
from bs4 import BeautifulSoup

def scrape_github_profile(username):
    """
    Scrapes a GitHub profile for key information.
    """
    url = f"https://github.com/{username}"
    print(f"Fetching data from: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes

        print("Successfully fetched the page!")
        parse_html(response.text, username) # Pass username for context if needed

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error: Could not find user '{username}'. Please check the username and try again.")
    except requests.exceptions.RequestException as err:
        print(f"Network Error: An error occurred while fetching the page. {err}")

def parse_html(html_content, username):
    """
    Parses the HTML and extracts the required information.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # --- Data Extraction ---
    # We find elements by their HTML tags and CSS classes.
    # We add a .strip() to remove any leading/trailing whitespace.
    # We also include an 'if' check to prevent errors if an element isn't found.
    
    full_name_element = soup.find('span', {'class': 'p-name'})
    full_name = full_name_element.text.strip() if full_name_element else "Not provided"

    bio_element = soup.find('div', {'class': 'p-note', 'data-bio': 'true'})
    bio = bio_element.text.strip() if bio_element else "No bio provided."

    # Pinned repositories are a bit more complex, we find all of them
    pinned_repos_elements = soup.find_all('span', {'class': 'repo'})
    pinned_repos = [repo.text.strip() for repo in pinned_repos_elements]

    # --- Displaying the Data ---
    print("\n" + "="*40)
    print(f"Profile Information for: {username}")
    print("="*40)
    print(f"Full Name: {full_name}")
    print(f"Bio: {bio}")
    
    if pinned_repos:
        print("\nPinned Repositories:")
        for repo in pinned_repos:
            print(f"- {repo}")
    else:
        print("\nNo pinned repositories found.")
    print("="*40)


# Main execution block
if __name__ == "__main__":
    user_to_scrape = input("Enter the GitHub username to scrape: ")
    if user_to_scrape:
        scrape_github_profile(user_to_scrape)
    else:
        print("Username cannot be empty.")