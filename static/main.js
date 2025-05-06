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
};

//fetch('/recipes?ingredients=chicken,rice')

function ingredientFormatter() {
  let ingredients = document.getElementById("searchQuery").value;
  if (ingredients == "" || ingredients == null) {
    alert("Please enter ingredients");
    return;
  }
  if (ingredients.includes(",")) {
    formattedIngredients = ingredients
      .split(",")
      .map((ingredient) => ingredient.trim())
      .join(",");
  } else {
    alert("Please enter more than one ingredient separated by commas");
  }
  ingredients = "";
  return formattedIngredients;
}

// <----------------------------------------------------------------> //

const getRecipes = () => {
  formattedIngredients = ingredientFormatter();
  if (formattedIngredients == "") {
    return;
  }
  fetch(`/recipes?ingredients=${formattedIngredients}`)
    .then((response) => response.json())
    .then((data) => {
      let mainContent = document.getElementById("main-content");
      mainContent.innerHTML = "";
      results.innerHTML = "";
      data.forEach((recipe) => {
        appendRecipeInfo(recipe);
      });
    })
    .catch((error) => {
      console.error("Error fetching recipes:", error);
    });
};

const getRecipeById = () => {
  const id = document.getElementById("id").value;
  console.log("log id: " + id);
  fetch(`/recipes/${id}`)
    .then((response) => response.json())
    .then((data) => {
      results.innerHTML = "";
      appendRecipeInfo(data);
    })
    .catch((error) => {
      console.error("Error fetching recipe by ID:", error);
    });
};

const saveRecipe = (id) => {
  fetch(`/recipes/save-recipe/${id}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ id }),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Recipe saved:", data);
    })
    .catch((error) => {
      console.error("Error saving recipe:", error);
    });
};

const deleteSavedRecipe = (id) => {
  console.log(id);
  fetch(`/recipes/delete-recipe/${id}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Recipe deleted:", data);
      window.location.reload();
    })
    .catch((error) => {
      console.error("Error deleting saved recipe:", error);
    });
};

// --------------------------------------------------- //

const fetchIngredients = () => {
  fetch("/ingredients")
    .then((response) => response.json())
    .then((data) => {
      if (data.length === 0) {
        alert("No ingredients found");
        return;
      }
      console.log(data);
      let ingredients = document.getElementById("ingredients");
      data.forEach((ingredient) => {
        let option = document.createElement("option");
        option.value = ingredient;
        ingredients.appendChild(option);
      });
    })
    .catch((error) => {
      console.error("Error fetching ingredients:", error);
    });
};

const removeIngredient = (ingredientId) => {
  fetchIngredients(`ingredients/remove/${ingredientId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => response.json());
};

const generateMealPlan = () => {
  fetch("/meal-plans", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => {
    if (response.ok) {
      return response.json();
    } else {
      throw new Error("Failed to generate meal plan");
    }
  }
)
}

const deleteMealPlan = (mealPlanId) => {
  fetch(`/meal-plan/delete/${mealPlanId}`, {
    method: "DELETE",
    headers: {
      "Content-Type": "application/json",
    },
  }).then((response) => response.json());
};
