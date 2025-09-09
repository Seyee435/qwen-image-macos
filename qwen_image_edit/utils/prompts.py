"""
Smart prompt suggestions for image editing.
"""

from typing import List, Dict
import random

# Popular editing patterns that work well with Qwen Image Edit
PROMPT_SUGGESTIONS = {
    "style_transfer": [
        "Make this image look like a Studio Ghibli animation",
        "Transform this into a oil painting style", 
        "Convert this to a watercolor painting",
        "Make this look like a vintage photograph from the 1970s",
        "Give this image a cyberpunk aesthetic with neon colors",
        "Transform this into a minimalist line drawing",
    ],
    
    "object_modification": [
        "Change the color of the {object} to {color}",
        "Remove the {object} from the image",
        "Add a {object} to the scene",
        "Make the {object} larger and more prominent",
        "Replace the {object} with a {replacement}",
    ],
    
    "lighting_weather": [
        "Change the lighting to golden hour sunset",
        "Add dramatic storm clouds in the sky",
        "Make it look like it's snowing",
        "Change the time of day to nighttime with street lights",
        "Add warm, cozy indoor lighting",
        "Make the scene look foggy and mysterious",
    ],
    
    "clothing_fashion": [
        "Change the sweater to be blue with white text",
        "Add a stylish jacket to the person",
        "Change the outfit to formal business attire",
        "Give the person a vintage 1950s style dress",
        "Add fashionable sunglasses",
        "Change the shoes to sneakers",
    ],
    
    "background_scenery": [
        "Change the background to a beautiful mountain landscape",
        "Replace the background with a modern city skyline",
        "Add a tropical beach background",
        "Change the setting to a cozy coffee shop interior",
        "Replace the background with a futuristic sci-fi environment",
    ],
}

# Common objects users might want to edit
COMMON_OBJECTS = [
    "shirt", "sweater", "jacket", "hat", "glasses", "shoes",
    "car", "building", "tree", "flowers", "sky", "clouds",
    "hair", "eyes", "smile", "background", "lighting"
]

# Common colors for replacements
COMMON_COLORS = [
    "red", "blue", "green", "yellow", "purple", "orange", 
    "pink", "black", "white", "gray", "brown", "gold"
]


def get_random_suggestions(category: str = None, count: int = 3) -> List[str]:
    """Get random prompt suggestions."""
    if category and category in PROMPT_SUGGESTIONS:
        suggestions = PROMPT_SUGGESTIONS[category]
    else:
        # Get suggestions from all categories
        all_suggestions = []
        for category_suggestions in PROMPT_SUGGESTIONS.values():
            all_suggestions.extend(category_suggestions)
        suggestions = all_suggestions
    
    return random.sample(suggestions, min(count, len(suggestions)))


def get_suggestions_for_object(object_name: str) -> List[str]:
    """Get suggestions for editing a specific object."""
    suggestions = []
    
    # Color changes
    for color in random.sample(COMMON_COLORS, 3):
        suggestions.append(f"Change the color of the {object_name} to {color}")
    
    # Style changes  
    suggestions.extend([
        f"Make the {object_name} look more vintage",
        f"Give the {object_name} a modern, sleek appearance",
        f"Add decorative patterns to the {object_name}",
    ])
    
    return suggestions


def improve_prompt(user_prompt: str) -> Dict[str, str]:
    """Suggest improvements to user's prompt."""
    improvements = {}
    prompt_lower = user_prompt.lower()
    
    # Check if prompt could be more specific
    if len(user_prompt.split()) < 5:
        improvements["specificity"] = "Consider adding more detail about style, color, or mood"
    
    # Suggest adding style if missing
    style_keywords = ["style", "look like", "aesthetic", "vintage", "modern"]
    if not any(keyword in prompt_lower for keyword in style_keywords):
        improvements["style"] = "Try adding a style: 'make it look like...', 'in vintage style', etc."
    
    # Suggest being more specific about changes
    vague_words = ["better", "nicer", "different", "change"]
    if any(word in prompt_lower for word in vague_words):
        improvements["precision"] = "Be more specific about what you want changed (color, size, style, etc.)"
    
    return improvements


def show_prompt_help() -> str:
    """Show helpful prompt examples."""
    examples = []
    
    # Get examples from each category
    for category, suggestions in PROMPT_SUGGESTIONS.items():
        category_name = category.replace("_", " ").title()
        examples.append(f"**{category_name}:**")
        for suggestion in suggestions[:2]:  # Show 2 examples per category
            examples.append(f"  • {suggestion}")
        examples.append("")
    
    return "\n".join(examples)
