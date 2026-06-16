# CuisineQuest-AI 🍽️

A conversational AI chatbot that helps users discover restaurants and book a table through natural language. CuisineQuest-AI is built with the [Rasa](https://rasa.com/) open-source framework and backed by a MongoDB database of Bangalore restaurants (Zomato dataset). It ships with a lightweight web chat widget so you can talk to the assistant straight from your browser.

## Features

- **Book a table** — A guided conversational form collects your name, restaurant, date, time, email, and phone number, with validation at every step and a confirmation summary.
- **Restaurant recommendations by cuisine** — Ask for a cuisine (e.g. *Italian*, *Chinese*) and get the top-rated matches.
- **Restaurant recommendations by location** — Find the best-rated restaurants in a given Bangalore neighbourhood.
- **Restaurant info lookup** — Ask about a specific restaurant and get its address, cuisines, cost for two, ordering/booking options, type, location, and phone number. Uses fuzzy matching so minor spelling mistakes still resolve.
- **Surprise me** — Get a random restaurant suggestion when you can't decide.
- **Cancel a reservation** — Cancel an in-progress booking.
- **Small talk** — Greetings, goodbyes, current time, and a few fun extras.

## Tech Stack

- **[Rasa](https://rasa.com/)** — NLU + dialogue management (intents, entities, slots, forms, rules, stories).
- **Rasa SDK** — Custom Python actions (the action server).
- **MongoDB** — Stores the restaurant dataset (`Restaurants` database, `Zomato` collection).
- **Python libraries** — `pymongo`, `fuzzywuzzy`, `parsedatetime`.
- **Frontend** — Plain HTML / CSS / JavaScript chat widget (`index.html`, `styles.css`, `script.js`).

## Project Structure

```
CuisineQuest-AI/
├── actions/
│   └── actions.py          # Custom action server (recommendations, bookings, info lookup)
├── data/
│   ├── nlu.yml             # Training examples for intents & entities
│   ├── rules.yml           # Conversation rules
│   └── stories.yml         # Conversation stories
├── tests/
│   └── test_stories.yml    # Test conversations
├── models/                 # Trained Rasa models
├── config.yml              # NLU pipeline & dialogue policies
├── domain.yml              # Intents, entities, slots, forms, responses
├── endpoints.yml           # Action server & other endpoints
├── credentials.yml         # Channel credentials (REST channel)
├── index.html              # Web chat widget
├── styles.css              # Widget styling
└── script.js               # Widget logic (talks to the REST webhook)
```

## Prerequisites

- Python 3.8–3.10 (recommended for Rasa)
- [MongoDB](https://www.mongodb.com/) running locally on the default port (`mongodb://localhost:27017/`)
- A `Restaurants` database with a `Zomato` collection populated with restaurant documents (the [Zomato Bangalore Restaurants](https://www.kaggle.com/datasets/himanshupoddar/zomato-bangalore-restaurants) dataset). Each document is expected to contain fields such as `name`, `address`, `cuisines`, `location`, `rate`, `votes`, `online_order`, `book_table`, `rest_type`, `phone`, and `approx_cost(for two people)`.

## Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/sakshyam-patro/cuisinequest-ai.git
   cd cuisinequest-ai
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install rasa rasa-sdk pymongo fuzzywuzzy python-Levenshtein parsedatetime
   ```

4. **Start MongoDB** and make sure the `Restaurants.Zomato` collection is populated.

## Running the Bot

The bot has three moving parts: the Rasa server, the action server, and the web widget.

1. **Train a model** (only needed after changing `nlu.yml`, `stories.yml`, `rules.yml`, `domain.yml`, or `config.yml`):

   ```bash
   rasa train
   ```

2. **Start the action server** (runs the custom Python actions):

   ```bash
   rasa run actions
   ```

3. **Start the Rasa server with the REST API + CORS enabled** (in a separate terminal):

   ```bash
   rasa run --enable-api --cors "*"
   ```

   The REST webhook will be available at `http://localhost:5005/webhooks/rest/webhook`.

4. **Open the web widget** — open `index.html` in your browser (e.g. with a simple static server or by opening the file directly). Click the **Chat** button to start talking to the assistant.

### Try it in the terminal

You can also chat without the web widget:

```bash
rasa shell
```

(Make sure the action server is running in another terminal.)

## Example Conversations

- *"I want to book a table"* → starts the booking form
- *"Show me restaurants in Koramangala"* → top-rated restaurants in that area
- *"I'm in the mood for Chinese"* → top Chinese restaurants
- *"Tell me about Truffles"* → details for that restaurant
- *"Surprise me"* → a random restaurant suggestion
- *"What time is it?"* → the current time

## Configuration Notes

- The MongoDB connection string, database, and collection names are set near the top of `actions/actions.py`. Update them if your setup differs.
- The action server endpoint is configured in `endpoints.yml` (`http://localhost:5055/webhook` by default).
- The web widget points at `http://localhost:5005/webhooks/rest/webhook` in `script.js`; change this if you host Rasa elsewhere.

## License

This project is provided for educational purposes. Add a license of your choice before distribution.
