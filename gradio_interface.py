import gradio as gr
from interactive_search import perform_similarity_search
from advanced_search import perform_filtered_similarity_search
from enhanced_rag_chatbot import generate_llm_rag_response, prepare_context_for_llm, handle_enhanced_comparison_mode
from shared_functions import load_food_data, create_similarity_search_collection, populate_similarity_collection

# Load food data and create collections
food_items = load_food_data('./FoodDataSet.json')
interactive_collection = create_similarity_search_collection("gradio_interactive")
advanced_collection = create_similarity_search_collection("gradio_advanced")
rag_collection = create_similarity_search_collection("gradio_rag")
populate_similarity_collection(interactive_collection, food_items)
populate_similarity_collection(advanced_collection, food_items)
populate_similarity_collection(rag_collection, food_items)

def search_food_system(query, mode, cuisine="", max_calories="", compare_mode=False, query2=""):
    try:
        max_cal = int(max_calories) if max_calories.isdigit() else None
        
        if compare_mode:
            # RAG-style comparison
            results1 = perform_similarity_search(rag_collection, query, 3)
            results2 = perform_similarity_search(rag_collection, query2, 3)
            response = generate_llm_rag_response(query, results1) + "\n\n"
            response += generate_llm_rag_response(query2, results2)
            return response
        
        if mode == "Basic Search":
            results = perform_similarity_search(interactive_collection, query, 5)
        elif mode == "Cuisine Filter":
            results = perform_filtered_similarity_search(advanced_collection, query, cuisine_filter=cuisine, n_results=5)
        elif mode == "Calorie Filter":
            results = perform_filtered_similarity_search(advanced_collection, query, max_calories=max_cal, n_results=5)
        elif mode == "Combined Filters":
            results = perform_filtered_similarity_search(advanced_collection, query, cuisine_filter=cuisine, max_calories=max_cal, n_results=5)
        elif mode == "Demonstration Mode":
            results = perform_filtered_similarity_search(advanced_collection, "chocolate dessert", n_results=3)
        elif mode == "Help Menu":
            return ("Commands:\n"
                    "- help: Show help menu\n"
                    "- compare: Compare two queries\n"
                    "- quit: Exit\n\n"
                    "Example Queries:\n"
                    "'I want something healthy and light for lunch'\n"
                    "'What Italian comfort food do you recommend?'")
        elif mode == "Quit":
            return "Exiting the system..."
        else:
            results = perform_similarity_search(interactive_collection, query, 5)
        
        if not results:
            return "❌ No matching results found."
        
        # Format output nicely
        output_text = ""
        for i, r in enumerate(results, 1):
            output_text += f"{i}. {r['food_name']} ({r['cuisine_type']}, {r['food_calories_per_serving']} cal) - Match: {r['similarity_score']*100:.1f}%\n"
            output_text += f"   Description: {r['food_description']}\n\n"
        
        # Add RAG response if mode is not basic/help
        if mode in ["Cuisine Filter", "Calorie Filter", "Combined Filters", "Demonstration Mode"]:
            rag_response = generate_llm_rag_response(query, results)
            output_text += f"🤖 AI Recommendation:\n{rag_response}\n"
        
        return output_text
    
    except Exception as e:
        return f"❌ Error: {e}"

# Gradio Interface
with gr.Blocks() as interface:
    gr.Markdown("## 🍽️ Food Recommendation System")
    gr.Markdown("Select a mode, enter your query, optional cuisine/calorie filters, and see results!")

    with gr.Row():
        query_input = gr.Textbox(label="Enter your food query")
        mode_input = gr.Dropdown(choices=[
            "Basic Search",
            "Cuisine Filter",
            "Calorie Filter",
            "Combined Filters",
            "Demonstration Mode",
            "Help Menu",
            "Quit"
        ], label="Search Mode", value="Basic Search")
    
    with gr.Row():
        cuisine_input = gr.Textbox(label="Cuisine (optional)")
        max_calories_input = gr.Textbox(label="Maximum Calories (optional)")
    
    with gr.Row():
        compare_toggle = gr.Checkbox(label="Enable Comparison Mode")
        query2_input = gr.Textbox(label="Second query (for comparison)")
    
    output_box = gr.Textbox(label="Results", lines=20)
    
    submit_btn = gr.Button("Search")
    submit_btn.click(
        search_food_system,
        inputs=[query_input, mode_input, cuisine_input, max_calories_input, compare_toggle, query2_input],
        outputs=output_box
    )

interface.launch(share=True)
