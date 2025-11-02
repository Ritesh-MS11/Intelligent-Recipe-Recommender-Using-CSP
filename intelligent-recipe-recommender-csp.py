
RECIPES = [
    {"id": 1, "name": "Mediterranean Chickpea Salad", 
     "ingredients": ["chickpeas", "cucumber", "tomato", "olive oil", "lemon", "feta cheese", "red onion", "parsley"],
     "dietary": ["vegetarian", "gluten-free"], "time": 15, "difficulty": "Easy", "cuisine": "Mediterranean", "calories": 320, "protein": 12},
    
    {"id": 2, "name": "Quinoa Buddha Bowl",
     "ingredients": ["quinoa", "chickpeas", "avocado", "spinach", "carrot", "tahini", "lemon", "sesame seeds"],
     "dietary": ["vegan", "gluten-free"], "time": 30, "difficulty": "Easy", "cuisine": "Modern Fusion", "calories": 450, "protein": 15},
    
    {"id": 3, "name": "Classic Chicken Stir Fry",
     "ingredients": ["chicken", "soy sauce", "ginger", "garlic", "broccoli", "carrot", "bell pepper", "rice"],
     "dietary": ["non-vegetarian", "dairy-free"], "time": 25, "difficulty": "Medium", "cuisine": "Asian", "calories": 480, "protein": 35},
    
    {"id": 4, "name": "Vegetable Pasta Primavera",
     "ingredients": ["pasta", "tomato", "onion", "garlic", "olive oil", "basil", "bell pepper", "zucchini", "parmesan"],
     "dietary": ["vegetarian"], "time": 30, "difficulty": "Easy", "cuisine": "Italian", "calories": 380, "protein": 11},
    
    {"id": 5, "name": "Spicy Lentil Curry",
     "ingredients": ["lentils", "onion", "tomato", "cumin", "garlic", "coconut milk", "turmeric", "spinach", "ginger"],
     "dietary": ["vegan", "gluten-free"], "time": 40, "difficulty": "Medium", "cuisine": "Indian", "calories": 340, "protein": 18},
    
    {"id": 6, "name": "Grilled Salmon with Vegetables",
     "ingredients": ["salmon", "lemon", "olive oil", "asparagus", "garlic", "dill", "tomato", "black pepper"],
     "dietary": ["non-vegetarian", "gluten-free"], "time": 20, "difficulty": "Medium", "cuisine": "Contemporary", "calories": 420, "protein": 40},
    
    {"id": 7, "name": "Black Bean Tacos",
     "ingredients": ["black beans", "tortilla", "avocado", "lime", "cilantro", "onion", "tomato", "cumin", "lettuce"],
     "dietary": ["vegan", "vegetarian"], "time": 20, "difficulty": "Easy", "cuisine": "Mexican", "calories": 360, "protein": 13},
    
    {"id": 8, "name": "Mushroom Risotto",
     "ingredients": ["rice", "mushroom", "onion", "butter", "parmesan", "white wine", "vegetable broth", "thyme"],
     "dietary": ["vegetarian"], "time": 45, "difficulty": "Hard", "cuisine": "Italian", "calories": 440, "protein": 12},
    
    {"id": 9, "name": "Thai Green Curry",
     "ingredients": ["chicken", "coconut milk", "green curry paste", "bamboo shoots", "bell pepper", "basil", "fish sauce", "lime"],
     "dietary": ["non-vegetarian", "gluten-free"], "time": 35, "difficulty": "Hard", "cuisine": "Thai", "calories": 520, "protein": 32},
    
    {"id": 10, "name": "Caprese Salad",
     "ingredients": ["tomato", "mozzarella", "basil", "olive oil", "balsamic vinegar", "salt", "black pepper"],
     "dietary": ["vegetarian", "gluten-free"], "time": 10, "difficulty": "Easy", "cuisine": "Italian", "calories": 280, "protein": 14},
]

class RecipeRecommender:
    """
    CSP-based recipe recommender using forward checking algorithm.
    CSP = (Variables, Domains, Constraints) - Russell & Norvig Ch.6
    """
    
    def __init__(self):
        self.recipes = RECIPES
        self.constraints = {}
    
    def set_constraints(self, ingredients, dietary, max_time=None, difficulty=None, min_match=50):
        """Set user constraints (hard and soft)"""
        self.constraints = {
            'ingredients': [i.lower().strip() for i in ingredients],
            'dietary': [d.lower().strip() for d in dietary],
            'max_time': max_time,
            'difficulty': difficulty,
            'min_match': min_match
        }
    
    def check_constraints(self, recipe):
        """Check all hard constraints - forward checking (Aberg 2006)"""
        # Dietary constraint
        if self.constraints['dietary']:
            if not any(d in recipe['dietary'] for d in self.constraints['dietary']):
                return False, 0, [], []
        
        # Time constraint
        if self.constraints['max_time'] and recipe['time'] > self.constraints['max_time']:
            return False, 0, [], []
        
        # Difficulty constraint
        if self.constraints['difficulty'] and recipe['difficulty'] != self.constraints['difficulty']:
            return False, 0, [], []
        
        # Soft constraint: ingredient matching
        match_pct, matched, missing = self.calculate_match(recipe)
        
        # Threshold check
        if match_pct < self.constraints['min_match']:
            return False, match_pct, matched, missing
        
        return True, match_pct, matched, missing
    
    def calculate_match(self, recipe):
        """Calculate ingredient match percentage - soft constraint optimization"""
        if not self.constraints['ingredients']:
            return 100.0, [], recipe['ingredients']
        
        user_ings = self.constraints['ingredients']
        recipe_ings = [i.lower() for i in recipe['ingredients']]
        
        # Find matches (partial matching supported)
        matched = [r_ing for r_ing in recipe_ings 
                   if any(u_ing in r_ing or r_ing in u_ing for u_ing in user_ings)]
        missing = [i for i in recipe_ings if i not in matched]
        
        match_pct = (len(matched) / len(recipe_ings)) * 100
        return round(match_pct, 1), matched, missing
    
    def recommend(self, top_n=5):
        """Solve CSP and return top N recommendations"""
        candidates = []
        
        # Forward checking: check constraints and prune early
        for recipe in self.recipes:
            valid, match_pct, matched, missing = self.check_constraints(recipe)
            
            if valid:
                candidates.append({
                    'recipe': recipe,
                    'match_pct': match_pct,
                    'matched': matched,
                    'missing': missing
                })
        
        # Multi-criteria optimization (Aberg 2006)
        candidates.sort(key=lambda x: (-x['match_pct'], len(x['missing']), x['recipe']['time']))
        
        return candidates[:top_n]



def print_header():
    print("\n" + "="*80)
    print(" "*20 + "INTELLIGENT RECIPE RECOMMENDER")
    print(" "*18 + "Constraint Satisfaction Problem Solver")
    print("="*80)
    print("\nResearch-Based: Russell & Norvig (CSP), Aberg (2006), Tran et al. (2017)")
    print("="*80 + "\n")


def get_input():
    """Get user constraints"""
    print("📋 INGREDIENTS: Enter available ingredients (comma-separated)")
    print("   Example: tomato, onion, garlic, chicken, olive oil")
    ingredients = [i.strip() for i in input("   ➤ ").split(",") if i.strip()]
    
    print("\n🥗 DIETARY: Options: vegetarian, vegan, non-vegetarian, gluten-free")
    print("   (Leave empty for no restriction)")
    dietary = [d.strip() for d in input("   ➤ ").split(",") if d.strip()]
    
    print("\n⏱️  MAX TIME: Maximum cooking time in minutes (press Enter to skip)")
    time_input = input("   ➤ ").strip()
    max_time = int(time_input) if time_input else None
    
    print("\n🎯 DIFFICULTY: Easy, Medium, Hard (press Enter for any)")
    difficulty = input("   ➤ ").strip() or None
    
    print("\n📊 THRESHOLD: Minimum match percentage 0-100 [default: 50]")
    threshold = input("   ➤ ").strip()
    threshold = int(threshold) if threshold else 50
    
    return ingredients, dietary, max_time, difficulty, threshold


def display_results(recommendations):
    """Display recommendations"""
    if not recommendations:
        print("\n" + "="*80)
        print("❌ NO RECIPES FOUND")
        print("\n💡 Try: Lower threshold, add ingredients, or broaden dietary preferences")
        print("="*80 + "\n")
        return
    
    print("\n" + "="*80)
    print(f"🍳 RECOMMENDED RECIPES ({len(recommendations)} found)")
    print("="*80 + "\n")
    
    for idx, rec in enumerate(recommendations, 1):
        r = rec['recipe']
        print(f"#{idx}. {r['name']}")
        print("─"*78)
        print(f"   ✅ Match: {rec['match_pct']}% | ⏱️  {r['time']}min | 🎯 {r['difficulty']}")
        print(f"   🌍 {r['cuisine']} | 🥗 {', '.join(r['dietary'])}")
        print(f"   📊 {r['calories']}kcal | {r['protein']}g protein")
        
        if rec['matched']:
            print(f"\n   ✓ You have ({len(rec['matched'])}): {', '.join(rec['matched'])}")
        
        if rec['missing']:
            print(f"   ✗ Missing ({len(rec['missing'])}): {', '.join(rec['missing'])}")
        else:
            print(f"   🎉 Perfect Match! All ingredients available!")
        print()
    
    print("="*80)


def display_stats(recommendations, constraints):
    """Display statistics"""
    print("\n📊 STATISTICS")
    print("─"*80)
    print(f"Total recipes: {len(RECIPES)} | Matches: {len(recommendations)}")
    print(f"Ingredients: {len(constraints['ingredients'])} | Threshold: {constraints['min_match']}%")
    if constraints['dietary']:
        print(f"Dietary: {', '.join(constraints['dietary'])}")
    if constraints['max_time']:
        print(f"Max time: {constraints['max_time']} minutes")
    print("="*80 + "\n")

    
def main():
    print_header()
    
    # Initialize recommender
    recommender = RecipeRecommender()
    
    # Get constraints
    ingredients, dietary, max_time, difficulty, threshold = get_input()
    
    # Set constraints
    recommender.set_constraints(ingredients, dietary, max_time, difficulty, threshold)
    
    # Get recommendations
    print("\n⏳ Solving CSP with forward checking algorithm...")
    results = recommender.recommend(top_n=5)
    
    # Display results
    display_results(results)
    display_stats(results, recommender.constraints)
    
    # Run again?
    if input("Search again? (y/n): ").lower() == 'y':
        main()
    else:
        print("\nThank you! 👋\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")