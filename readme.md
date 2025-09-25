jspsearch - Multi-Platform Search Interface
A simple, clean, and modern single-page web application that allows you to search across multiple platforms from one unified search bar. This project fetches real-time results from the Wikipedia API and demonstrates how to integrate other sources with a mock DuckDuckGo API.

Live Demo: Link to your GitHub Pages URL here

Features
Unified Search: Enter a query once to get results from multiple sources.

Modern UI: A beautiful and responsive interface built with Tailwind CSS and Google Fonts.

Wikipedia Integration: Fetches live search results directly from the Wikipedia API.

Asynchronous Fetching: Uses modern JavaScript (async/await and Promise.all) to fetch data from different sources concurrently for a faster experience.

Dynamic Results: The page dynamically renders loading states, error messages, and search results without needing a refresh.

Smooth Animations: Subtle fade-in animations for search results provide a polished user experience.

Self-Contained: Everything is in a single HTML file, making it easy to deploy and host on services like GitHub Pages.

Technologies Used
HTML5: For the basic structure of the web page.

Tailwind CSS: For styling the user interface with a utility-first approach.

JavaScript (ES6+): For handling the form submission, API calls, and dynamically rendering the content.

Wikipedia API: To fetch live search results.

How to Use
No complex setup is required! You can run this project in two simple steps:

Clone the repository:

git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git)

Open the file:
Navigate to the project directory and open the jsps.html file in your favorite web browser.

How It Works
The core logic is handled by the JavaScript code embedded within the jsps.html file.

Event Listener: An event listener is attached to the search form's submit event.

API Calls: When a user submits a query, the script makes two concurrent API calls using Promise.all:

fetchWikipedia(query): Constructs a URL and fetches search results from the public Wikipedia API. It then makes a second call to get page summaries.

fetchDuckDuckGoMock(query): This function simulates a network request to another search provider, demonstrating how easily the application can be extended.

Rendering States:

While the data is being fetched, a loading spinner is displayed.

If any of the API calls fail, a user-friendly error message is shown.

Once the data is successfully retrieved, the renderResults function dynamically creates the HTML to display the results, separated by their source (Wikipedia and DuckDuckGo).

Author
Jacob Santhosh

GitHub

LinkedIn
