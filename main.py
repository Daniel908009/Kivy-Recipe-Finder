from kivy.uix.image import AsyncImage
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
import requests

APIKey = ""
url = f"https://api.spoonacular.com/recipes/findByIngredients"
NRecipes = 20
IgnP = True

def searchByIngredientsAPI(ingredients):
    #print(ingredients)
    paramss = {
        "ingredients": ingredients,
        "number": NRecipes,
        "ranking": 1,
        "ignorePantry": IgnP,
        "apiKey": APIKey
    }
    data = requests.get(url, params=paramss)
    recipes = data.json()
    if data.status_code == 200:
        #for recipe in recipes:
            #print(recipe["title"])
            #print(recipe["usedIngredientCount"])
        return recipes
    else:
        print("Error")
        return None
    
class RecipePopup(Popup):
    def __init__(self, recipe):
        super(RecipePopup, self).__init__()
        self.recipe = recipe
        print(recipe["image"])
        self.ids.ImageR.add_widget(AsyncImage(source=recipe["image"]))

class RecipeWidget(GridLayout):
    def __init__(self, recipe):
        super(RecipeWidget, self).__init__()
        self.recipe = recipe
        title = recipe["title"]
        if len(title) > 20:
            title = title[:20] + "..."
        self.ids.recipeName.text = title
        self.ids.ingredients.text = str(recipe["usedIngredientCount"]) + '/' + str(recipe["missedIngredientCount"] + recipe["usedIngredientCount"])
    def view(self):
        popup = RecipePopup(self.recipe)
        popup.open()

class SettingsPopup(Popup):
    def __init__(self, caller):
        global APIKey, NRecipes, IgnP
        super(SettingsPopup, self).__init__()
        self.caller = caller
        self.ids.apiKeyInput.text = APIKey
        self.ids.numRecipesInput.text = str(NRecipes)
        self.ids.ignorePantry.active = IgnP
    def save(self):
        global APIKey, NRecipes, IgnP
        if self.ids.apiKeyInput.text != "":
            APIKey = self.ids.apiKeyInput.text
        if self.ids.numRecipesInput.text != "":
            NRecipes = int(self.ids.numRecipesInput.text)
        IgnP = self.ids.ignorePantry.active
        self.dismiss()

class InfoWidget(GridLayout):
    pass

class MainGrid(GridLayout):
    def search(self):
        self.recipes = searchByIngredientsAPI(self.ids.searchInput.text)
        if self.recipes != None:
            self.ids.mealList.clear_widgets()
            self.ids.mealList.height = 60
            self.ids.mealList.add_widget(InfoWidget())
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