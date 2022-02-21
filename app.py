from flask import Flask, render_template, request, redirect, flash
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = '12345'

#home page shows all recipe
@app.route('/')
def home():
    
    with open('data.json') as json_file:
        data = json.load(json_file)
    return render_template('home.html', data = data)

@app.route('/names', methods = ['GET'])
def rec_names():
    with open('data.json') as json_file:
        data = json.load(json_file)
    return render_template('names.html', data = data)            


@app.route('/details/<name>', methods = ['GET'])
def detail(name):
    rec = False
    with open('data.json') as json_file:
        data = json.load(json_file)
        for item in data:
           args = name
           if item['name'] == str(args) :
                rec = True
                ing = item["ingredients"]
                return render_template('detail.html', data = data, args = args, ing = ing)
        if rec == False:
            return render_template('home.html', data = data)

@app.route('/addrecipe')
def to_add_recipe():
        with open('data.json') as json_file:
            data = json.load(json_file)
        return render_template('recipe.html', data = data)


@app.route('/addname', methods = ['POST'])
def add_recipe_name():
    rec_name = False
    with open('data.json') as json_file:
        data = json.load(json_file)
        
        for item in data:
           args = f"{request.form.get('name')}"
           if item['name'] == str(args) :
               rec_name = True
               flash("Recipe already exists")
               return render_template('recipe.html', data = data)
        
        if rec_name == False:
            data.append({
                        "name": f"{request.form.get('name')}",
                        "ingredients": [],
                        "instructions": []
                        })

            with open('data.json', 'w') as file:
                json.dump(data, file, indent= 2)
            return render_template('recipe.html', data = data) 

@app.route('/addingredient', methods = ['POST'])
def add_recipe_ingredients():
    with open('data.json') as json_file:
        data = json.load(json_file)
        data[len(data)-1]["ingredients"].append(f"{request.form.get('ingredient')}")
        with open('data.json', 'w') as file:
            json.dump(data, file, indent= 2)
        return render_template('recipe.html', data = data) 

@app.route('/addinstruction', methods = ['POST'])
def add_recipe_instruction():
    with open('data.json') as json_file:
        data = json.load(json_file)
        data[len(data)-1]["instructions"].append(f"{request.form.get('instruction')}")
        with open('data.json', 'w') as file:
            json.dump(data, file, indent= 2)
        return render_template('recipe.html', data = data) 

