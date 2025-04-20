const results = document.getElementById("results");

const submit = document.getElementById("submit");

const id = document.getElementById("id");


const appendRecipeInfo = (recipe) => {
    let recipeDiv = document.createElement("div");
    recipeDiv.className = "recipe";
    recipeDiv.innerHTML = `
        <h2>${recipe.title}</h2>
        <img src="${recipe.image}" alt="${recipe.title}">
        <a href="${recipe.id}" target="_blank">View Recipe</a>
    `;
    results.appendChild(recipeDiv);
}

//fetch('/recipes?ingredients=chicken,rice')

function ingredientFormatter(){
    let ingredients = document.getElementById("ingredients").value
    if (ingredients == "" || ingredients == null) {
        alert("Please enter ingredients");
        return;
    }
    if (ingredients.includes(",")) {
        formattedIngredients = ingredients.split(",").map(ingredient => ingredient.trim()).join(",");
    } else {
        alert("Please enter more than one ingredient separated by commas");
    }
    ingredients = ""
    return formattedIngredients
}

function storeRecipesInLocalStorage(recipes) {
    localStorage.setItem("recipes", JSON.stringify(recipes));
}

function getRecipesFromLocalStorage() {
    const recipes = localStorage.getItem("recipes");
    return recipes ? JSON.parse(recipes) : [];
}

// <----------------------------------------------------------------> //


const getRecipes = () => {
    formattedIngredients = ingredientFormatter()
    if (formattedIngredients == "") {
        return;
    }
    fetch(`/recipes?ingredients=${'chicken,rice'}`)
        .then((response) => response.json())
        .then((data) => {
            storeRecipesInLocalStorage(data);
            results.innerHTML = "";
            data.forEach(recipe => {
                appendRecipeInfo(recipe);
            });
        })
        .catch((error) => {
            console.error("Error fetching recipes:", error);
        });
}

const getRecipeById = () => {
    const id = document.getElementById("id").value;
    console.log('log id: ' + id)
    fetch(`/recipes/${id}`)
        .then((response) => response.json())
        .then((data) => {
            results.innerHTML = "";
            appendRecipeInfo(data);
        })
        .catch((error) => {
            console.error("Error fetching recipe by ID:", error);
        })}

const saveRecipe = (id) => {
    fetch(`/recipes/save-recipe${id}`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ id })
    })
    .then((response) => response.json())
    .then((data) => {
        console.log("Recipe saved:", data);
    })
    .catch((error) => {
        console.error("Error saving recipe:", error);
    });
}

const getSavedRecipes = () => {
    fetch("/saved-recipes")
    .then((response) => response.json())
    .then((data) => {
        results.innerHTML = "";
        data.forEach(recipe => {
            appendRecipeInfo(recipe);
        });
    })
    .catch((error) => {
        console.error("Error fetching saved recipes:", error);
    });
}

const deleteSavedRecipe = (id) => {
    fetch(`/saved-recipes/${id}`, {
        method: "DELETE",
        headers: {
            "Content-Type": "application/json"
        }
    })
    .then((response) => response.json())
    .then((data) => {
        console.log("Recipe deleted:", data);
        getSavedRecipes();
    })
    .catch((error) => {
        console.error("Error deleting saved recipe:", error);
    });
}


// --------------------------------------------------- //

const fetchIngredients = () => {
    fetch('/ingredients')
        .then((response) => response.json())
        .then((data) => {
            if (data.length === 0) {
                alert("No ingredients found");
                return;
            }
            console.log(data);
            let ingredients = document.getElementById("ingredients");
            data.forEach(ingredient => {
                let option = document.createElement("option");
                option.value = ingredient;
                ingredients.appendChild(option);
            });
        })
        .catch((error) => {
            console.error("Error fetching ingredients:", error);
        });
}

