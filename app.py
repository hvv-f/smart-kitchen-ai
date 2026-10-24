from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

INGREDIENTS = {
    "egg": {"en": "Eggs", "ar": "بيض"},
    "milk": {"en": "Milk", "ar": "حليب"},
    "cheese": {"en": "Cheese", "ar": "جبن"},
    "tomato": {"en": "Tomatoes", "ar": "طماطم"},
    "onion": {"en": "Onion", "ar": "بصل"},
    "potato": {"en": "Potatoes", "ar": "بطاطا"},
    "rice": {"en": "Rice", "ar": "أرز"},
    "pasta": {"en": "Pasta", "ar": "مكرونة"},
    "chicken": {"en": "Chicken", "ar": "دجاج"},
    "tuna": {"en": "Tuna", "ar": "تونة"},
    "lentils": {"en": "Lentils", "ar": "عدس"},
    "carrot": {"en": "Carrot", "ar": "جزر"},
    "garlic": {"en": "Garlic", "ar": "ثوم"},
    "bread": {"en": "Bread", "ar": "خبز"},
    "flour": {"en": "Flour", "ar": "دقيق"},
    "sugar": {"en": "Sugar", "ar": "سكر"},
    "banana": {"en": "Banana", "ar": "موز"},
    "apple": {"en": "Apple", "ar": "تفاح"},
    "yogurt": {"en": "Yogurt", "ar": "زبادي"},
    "oats": {"en": "Oats", "ar": "شوفان"},
    "cocoa": {"en": "Cocoa powder", "ar": "كاكاو"},
    "lemon": {"en": "Lemon", "ar": "ليمون"},
    "oil": {"en": "Cooking oil", "ar": "زيت"},
    "salt": {"en": "Salt", "ar": "ملح"},
    "honey": {"en": "Honey", "ar": "عسل"},
    "coffee": {"en": "Coffee", "ar": "قهوة"},
    "tea": {"en": "Tea", "ar": "شاي"}
}

RECIPES = [
    {
        "name_en": "Cheese Omelette",
        "name_ar": "عجة بالجبن",
        "type": "meal",
        "ingredients": ["egg", "cheese", "salt", "oil"],
        "time": 10,
        "steps_en": [
            "Beat the eggs.",
            "Heat a little oil in a pan.",
            "Add the eggs and cheese.",
            "Cook thoroughly and serve."
        ],
        "steps_ar": [
            "اخفقي البيض.",
            "سخني قليلًا من الزيت في مقلاة.",
            "أضيفي البيض والجبن.",
            "اطهي الخليط جيدًا ثم قدميه."
        ],
        "video": "cheese omelette recipe"
    },
    {
        "name_en": "Tomato Pasta",
        "name_ar": "مكرونة بالطماطم",
        "type": "meal",
        "ingredients": ["pasta", "tomato", "onion", "oil", "salt"],
        "time": 25,
        "steps_en": [
            "Boil the pasta.",
            "Chop the tomatoes and onion.",
            "Cook the vegetables in oil.",
            "Mix the sauce with the pasta."
        ],
        "steps_ar": [
            "اسلقي المكرونة.",
            "قطعي الطماطم والبصل.",
            "اطهي الخضروات في الزيت.",
            "اخلطي الصلصة مع المكرونة."
        ],
        "video": "tomato pasta recipe"
    },
    {
        "name_en": "Lentil Soup",
        "name_ar": "شوربة العدس",
        "type": "meal",
        "ingredients": ["lentils", "onion", "carrot", "salt"],
        "time": 35,
        "steps_en": [
            "Wash the lentils.",
            "Chop the onion and carrot.",
            "Add water and cook until soft.",
            "Season and serve hot."
        ],
        "steps_ar": [
            "اغسلي العدس.",
            "قطعي البصل والجزر.",
            "أضيفي الماء واطهي المكونات حتى تلين.",
            "أضيفي التوابل وقدمي الشوربة ساخنة."
        ],
        "video": "lentil soup recipe"
    },
    {
        "name_en": "Banana Oat Pancakes",
        "name_ar": "بان كيك الموز والشوفان",
        "type": "dessert",
        "ingredients": ["banana", "egg", "oats"],
        "time": 15,
        "steps_en": [
            "Mash the banana.",
            "Mix with egg and oats.",
            "Cook small portions in a pan.",
            "Serve with honey if available."
        ],
        "steps_ar": [
            "اهرسي الموز.",
            "اخلطيه مع البيض والشوفان.",
            "اطهي كميات صغيرة في مقلاة.",
            "قدميها مع العسل إذا توفر."
        ],
        "video": "banana oat pancakes recipe"
    },
    {
        "name_en": "Hot Cocoa",
        "name_ar": "كاكاو ساخن",
        "type": "drink",
        "ingredients": ["milk", "cocoa", "sugar"],
        "time": 7,
        "steps_en": [
            "Warm the milk.",
            "Add cocoa and sugar.",
            "Stir until smooth.",
            "Serve warm."
        ],
        "steps_ar": [
            "سخني الحليب.",
            "أضيفي الكاكاو والسكر.",
            "حركي حتى يذوب الخليط.",
            "قدميه دافئًا."
        ],
        "video": "homemade hot cocoa"
    },
    {
        "name_en": "Banana Smoothie",
        "name_ar": "سموذي الموز",
        "type": "drink",
        "ingredients": ["banana", "milk"],
        "time": 5,
        "steps_en": [
            "Slice the banana.",
            "Blend it with milk.",
            "Blend until smooth.",
            "Serve immediately."
        ],
        "steps_ar": [
            "قطعي الموز.",
            "ضعيه في الخلاط مع الحليب.",
            "اخلطي حتى يصبح القوام ناعمًا.",
            "قدميه مباشرة."
        ],
        "video": "banana smoothie recipe"
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/ingredients")
def get_ingredients():
    lang = request.args.get("lang", "en")
    return jsonify([
        {
            "id": key,
            "name": value["ar"] if lang == "ar" else value["en"]
        }
        for key, value in INGREDIENTS.items()
    ])

@app.route("/api/recipes", methods=["POST"])
def get_recipes():
    data = request.get_json(silent=True) or {}
    selected = set(data.get("ingredients", []))
    kind = data.get("kind", "all")
    lang = data.get("lang", "en")
    strict = data.get("strict", False)

    results = []

    for recipe in RECIPES:
        if kind != "all" and recipe["type"] != kind:
            continue

        required = set(recipe["ingredients"])
        matched = required & selected
        missing = required - selected

        if strict and missing:
            continue

        if not matched:
            continue

        results.append({
            "name": recipe["name_ar"] if lang == "ar"
                    else recipe["name_en"],
            "time": recipe["time"],
            "score": round(100 * len(matched) / len(required)),
            "missing": [
                INGREDIENTS[x][lang]
                if x in INGREDIENTS else x
                for x in recipe["ingredients"] if x in missing
            ],
            "steps": recipe["steps_ar"] if lang == "ar"
                     else recipe["steps_en"],
            "video": "https://www.youtube.com/results?search_query="
                     + recipe["video"].replace(" ", "+")
        })

    results.sort(key=lambda r: (-r["score"], r["time"]))

    return jsonify({"recipes": results})

@app.route("/api/assistant", methods=["POST"])
def assistant():
    data = request.get_json(silent=True) or {}
    lang = data.get("lang", "en")
    message = data.get("message", "").strip()

    if lang == "ar":
        answer = (
            "أهلًا بك في Smart Kitchen AI! اختاري المكونات "
            "المتوفرة لديك ثم اضغطي على اقتراح الوصفات. "
            "يمكنك مشاهدة خطوات التحضير والبحث عن فيديو للطبق."
        )
    else:
        answer = (
            "Welcome to Smart Kitchen AI! Select the ingredients "
            "you have and click Find Recipes. You can view cooking "
            "steps and search for a recipe video."
        )

    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
