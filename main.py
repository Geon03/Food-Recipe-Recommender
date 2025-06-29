import streamlit as st
import cv2
import numpy as np
from PIL import Image
import requests
import json
from typing import List, Dict
import random

# Configure the page
st.set_page_config(
    page_title="Smart Fridge Food Recommender",
    page_icon="🍽️",
    layout="wide"
)

# Recipe database with ingredients and instructions
RECIPE_DATABASE = {
    "tomato": [
        {
            "name": "Tomato Pasta",
            "ingredients": ["tomato", "pasta", "garlic", "olive oil"],
            "instructions": "Cook pasta, sauté garlic, add tomatoes, mix with pasta",
            "prep_time": "20 mins",
            "difficulty": "Easy"
        },
        {
            "name": "Tomato Salad",
            "ingredients": ["tomato", "onion", "cucumber"],
            "instructions": "Chop vegetables, mix with dressing",
            "prep_time": "10 mins",
            "difficulty": "Easy"
        }
    ],
    "chicken": [
        {
            "name": "Grilled Chicken",
            "ingredients": ["chicken", "herbs", "olive oil"],
            "instructions": "Marinate chicken, grill until cooked through",
            "prep_time": "30 mins",
            "difficulty": "Medium"
        },
        {
            "name": "Chicken Curry",
            "ingredients": ["chicken", "onion", "tomato", "spices"],
            "instructions": "Cook onions, add chicken and spices, simmer",
            "prep_time": "45 mins",
            "difficulty": "Medium"
        }
    ],
    "egg": [
        {
            "name": "Scrambled Eggs",
            "ingredients": ["egg", "butter", "salt"],
            "instructions": "Beat eggs, cook in butter until fluffy",
            "prep_time": "5 mins",
            "difficulty": "Easy"
        },
        {
            "name": "Egg Fried Rice",
            "ingredients": ["egg", "rice", "vegetables"],
            "instructions": "Cook rice, scramble eggs, mix together",
            "prep_time": "15 mins",
            "difficulty": "Easy"
        }
    ],
    "carrot": [
        {
            "name": "Carrot Soup",
            "ingredients": ["carrot", "onion", "broth"],
            "instructions": "Cook carrots and onions, blend with broth",
            "prep_time": "25 mins",
            "difficulty": "Easy"
        }
    ],
    "potato": [
        {
            "name": "Mashed Potatoes",
            "ingredients": ["potato", "butter", "milk"],
            "instructions": "Boil potatoes, mash with butter and milk",
            "prep_time": "20 mins",
            "difficulty": "Easy"
        },
        {
            "name": "French Fries",
            "ingredients": ["potato", "oil"],
            "instructions": "Cut potatoes, fry until golden",
            "prep_time": "15 mins",
            "difficulty": "Easy"
        }
    ],
    "onion": [
        {
            "name": "Onion Rings",
            "ingredients": ["onion", "flour", "oil"],
            "instructions": "Slice onions, coat in batter, fry",
            "prep_time": "20 mins",
            "difficulty": "Medium"
        }
    ],
    "cheese": [
        {
            "name": "Grilled Cheese",
            "ingredients": ["cheese", "bread", "butter"],
            "instructions": "Butter bread, add cheese, grill until golden",
            "prep_time": "10 mins",
            "difficulty": "Easy"
        }
    ],
    "bread": [
        {
            "name": "Toast",
            "ingredients": ["bread", "butter"],
            "instructions": "Toast bread, spread with butter",
            "prep_time": "3 mins",
            "difficulty": "Easy"
        }
    ],
    "milk": [
        {
            "name": "Milkshake",
            "ingredients": ["milk", "ice cream", "sugar"],
            "instructions": "Blend milk with ice cream and sugar",
            "prep_time": "5 mins",
            "difficulty": "Easy"
        }
    ],
    "apple": [
        {
            "name": "Apple Pie",
            "ingredients": ["apple", "sugar", "flour", "butter"],
            "instructions": "Make pastry, fill with apples, bake",
            "prep_time": "60 mins",
            "difficulty": "Hard"
        }
    ]
}

# Common food items that might be detected in a fridge
COMMON_FOOD_ITEMS = [
    "tomato", "potato", "onion", "carrot", "bell pepper", "cucumber", 
    "lettuce", "spinach", "broccoli", "cauliflower", "chicken", "beef",
    "fish", "egg", "milk", "cheese", "yogurt", "butter", "bread",
    "apple", "banana", "orange", "lemon", "garlic", "ginger"
]

def detect_ingredients_mock(image) -> List[str]:
    """
    Mock ingredient detection function.
    In a real implementation, this would use a trained computer vision model
    like YOLO, or a service like Google Vision API or Amazon Rekognition.
    """
    # Simulate ingredient detection with random items
    detected_items = random.sample(COMMON_FOOD_ITEMS, random.randint(3, 8))
    return detected_items

def get_color_analysis(image):
    """Analyze image colors to help with mock detection"""
    img_array = np.array(image)
    
    # Calculate average colors
    avg_colors = np.mean(img_array, axis=(0, 1))
    
    # Mock detection based on color analysis
    detected = []
    
    # Simple color-based heuristics (very basic)
    if avg_colors[0] > avg_colors[1] and avg_colors[0] > avg_colors[2]:  # More red
        detected.extend(["tomato", "apple"])
    if avg_colors[1] > avg_colors[0] and avg_colors[1] > avg_colors[2]:  # More green
        detected.extend(["lettuce", "cucumber", "broccoli"])
    if avg_colors[2] > avg_colors[0] and avg_colors[2] > avg_colors[1]:  # More blue
        detected.extend(["milk", "cheese"])
    
    # Add some common items
    detected.extend(["egg", "chicken", "onion"])
    
    return list(set(detected))[:6]  # Return unique items, max 6

def get_recipe_recommendations(ingredients: List[str]) -> List[Dict]:
    """Get recipe recommendations based on detected ingredients"""
    recommendations = []
    
    for ingredient in ingredients:
        if ingredient.lower() in RECIPE_DATABASE:
            recipes = RECIPE_DATABASE[ingredient.lower()]
            recommendations.extend(recipes)
    
    # Remove duplicates and limit results
    seen_recipes = set()
    unique_recommendations = []
    for recipe in recommendations:
        if recipe['name'] not in seen_recipes:
            unique_recommendations.append(recipe)
            seen_recipes.add(recipe['name'])
    
    return unique_recommendations[:8]  # Return max 8 recipes

def main():
    st.title("🍽️ Smart Fridge Food Recommender")
    st.markdown("Upload a photo of your refrigerator and get personalized recipe recommendations!")
    
    # Sidebar with information
    with st.sidebar:
        st.header("How it works")
        st.markdown("""
        1. **Upload** a clear photo of your refrigerator
        2. **AI Detection** identifies ingredients in the image
        3. **Get Recommendations** for recipes you can make
        4. **Cook** and enjoy your meal!
        """)
        
        st.header("Tips for better results")
        st.markdown("""
        - Ensure good lighting
        - Keep items visible
        - Avoid cluttered shots
        - Include fresh ingredients
        """)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📸 Upload Your Fridge Photo")
        
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg'],
            help="Upload a clear photo of your refrigerator contents"
        )
        
        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Fridge Photo", use_column_width=True)
            
            # Add a button to analyze
            if st.button("🔍 Analyze Ingredients", type="primary"):
                with st.spinner("Analyzing your fridge contents..."):
                    # Simulate processing time
                    import time
                    time.sleep(2)
                    
                    # Detect ingredients (mock function)
                    detected_ingredients = get_color_analysis(image)
                    
                    # Store in session state
                    st.session_state.ingredients = detected_ingredients
                    st.session_state.recipes = get_recipe_recommendations(detected_ingredients)
    
    with col2:
        st.header("🥘 Recipe Recommendations")
        
        if hasattr(st.session_state, 'ingredients') and st.session_state.ingredients:
            # Display detected ingredients
            st.subheader("🥬 Detected Ingredients")
            
            # Create ingredient tags
            ingredient_cols = st.columns(3)
            for i, ingredient in enumerate(st.session_state.ingredients):
                with ingredient_cols[i % 3]:
                    st.success(f"✓ {ingredient.title()}")
            
            st.divider()
            
            # Display recipe recommendations
            st.subheader("👨‍🍳 Recommended Recipes")
            
            if st.session_state.recipes:
                for recipe in st.session_state.recipes:
                    with st.expander(f"🍽️ {recipe['name']} ({recipe['difficulty']})"):
                        col_a, col_b = st.columns([2, 1])
                        
                        with col_a:
                            st.write("**Ingredients needed:**")
                            st.write(", ".join(recipe['ingredients']))
                            
                            st.write("**Instructions:**")
                            st.write(recipe['instructions'])
                        
                        with col_b:
                            st.metric("Prep Time", recipe['prep_time'])
                            st.metric("Difficulty", recipe['difficulty'])
                            
                            # Check if user has ingredients
                            user_has = len(set(recipe['ingredients']) & set(st.session_state.ingredients))
                            total_needed = len(recipe['ingredients'])
                            
                            if user_has == total_needed:
                                st.success("✅ You have all ingredients!")
                            else:
                                missing = total_needed - user_has
                                st.info(f"📝 Need {missing} more ingredient(s)")
            else:
                st.info("No recipes found for the detected ingredients. Try uploading a different image!")
        
        else:
            st.info("👆 Upload and analyze a fridge photo to see recipe recommendations!")
            
            # Show example recipes
            st.subheader("🌟 Popular Recipes")
            example_recipes = [
                {"name": "Quick Scrambled Eggs", "time": "5 mins", "difficulty": "Easy"},
                {"name": "Tomato Pasta", "time": "20 mins", "difficulty": "Easy"},
                {"name": "Grilled Chicken", "time": "30 mins", "difficulty": "Medium"},
            ]
            
            for recipe in example_recipes:
                st.write(f"• **{recipe['name']}** - {recipe['time']} ({recipe['difficulty']})")

    # Footer
    st.divider()
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🤖 Powered by AI Computer Vision | Made with Streamlit</p>
        <p><em>Note: This is a demo app. In production, it would use advanced computer vision models for accurate ingredient detection.</em></p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
