The Food Recommendation System using ChromaDB, RAG and, LLM.

About the Project

This project is a smart food recommendation system that helps users find dishes based on what they like, their dietary preferences, and calorie limits. It combines three ways to explore food:

Interactive Search – Type keywords and get quick results.

Advanced Search – Filter results by cuisine, calories, or both.

RAG Chatbot – Ask in natural language, and the AI gives helpful recommendations with context and explanations.

It’s designed to make searching for meals easy, fun, and personalized.

Key Features

Quick keyword-based searches for fast results.

Filters for cuisine, calories, or combined criteria.

Conversational AI chatbot for natural queries.

Compare two different queries and see AI’s suggestions.

Demo mode to explore system capabilities easily.

Displays nutrition, cooking methods, and health benefits for each dish

Tech Used

Python 3.11

ChromaDB – For storing and searching food data efficiently.

IBM watsonx.ai (Granite LLM) – Powers the chatbot responses.

Gradio – Interactive web interface.

JSON – Stores food data.

Project Files

shared_functions.py – Helper functions for loading data, searching, and AI integration.

interactive_search.py – Command-line interactive search.

advanced_search.py – Advanced search with filters.

enhanced_rag_chatbot.py – AI chatbot system.

system_comparison.py – Compare all three search systems.

gradio_interface.py – Web interface for easier access.

FoodDataSet.json – Food dataset.

How to Use

Clone the repo:

git clone <your-repo-url>
cd <repo-folder>


Install dependencies:

pip install -r requirements.txt


Run any module you want. Examples:

python interactive_search.py
python gradio_interface.py


Try different queries, filters, or chat with the AI.

Example Queries

"chocolate dessert"

"Italian food under 400 calories"

"Protein-rich breakfast options"

Compare "chocolate dessert" with "healthy breakfast"

License

This project is open source under the MIT License.
