from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import requests

APIKey = ""
url = f"https://api.spoonacular.com/recipes/findByIngredients"

def searchByIngredientsAPI(ingredients):
    print(ingredients)
    paramss = {
        "ingredients": ingredients,
        "number": 20,
        "ranking": 1,
        "ignorePantry": True,
        "apiKey": APIKey
    }
    data = requests.get(url, params=paramss)
    recipes = data.json()
    if data.status_code == 200:
        for recipe in recipes:
            print(recipe["title"])
        return recipes
    else:
        print("Error")
        return None
    
class RecipePopup(Popup):
    pass

class RecipeWidget(GridLayout):
    def __init__(self, recipe):
        super(RecipeWidget, self).__init__()
        self.recipe = recipe
        self.ids.recipeName.text = recipe["title"]
    def view(self):
        popup = RecipePopup(self.recipe)
        popup.open()

class SettingsPopup(Popup):
    def __init__(self, caller):
        super(SettingsPopup, self).__init__()
        self.caller = caller

class MainGrid(GridLayout):
    def search(self):
        self.recipes = searchByIngredientsAPI(self.ids.searchInput.text)
        if self.recipes != None:
            self.ids.mealList.clear_widgets()
            for recipe in self.recipes:
                self.ids.mealList.height += 50
                self.ids.mealList.add_widget(RecipeWidget(recipe))
    def settings(self):
        popup = SettingsPopup(self)
        popup.open()

class FindMealsApp(App):
    def build(self):
        return MainGrid()
    
if __name__ == '__main__':
    FindMealsApp().run()