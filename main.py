from kivy.app import App
from kivy.uix.gridlayout import GridLayout
import requests

APIKey = ""
url = f"https://api.spoonacular.com/recipes/findByIngredients"

def searchByIngredientsAPI(ingredients):
    print(ingredients)
    paramss = {
        "ingredients": ingredients,
        "number": 2,
        "apiKey": APIKey
    }
    data = requests.get(url, params=paramss)
    recipes = data.json()
    for recipe in recipes:
        print(recipe["title"])

class MainGrid(GridLayout):
    def search(self):
        searchByIngredientsAPI(self.ids.searchInput.text)



class FindMealsApp(App):
    def build(self):
        return MainGrid()
    
if __name__ == '__main__':
    FindMealsApp().run()