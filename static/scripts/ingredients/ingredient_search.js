ingredientSearchBox = document.getElementById("ingredient_search");
searchDiv = document.getElementById("recipe_search_div");
searchButton = document.getElementById("ingredient_search_button");
errorMessage = null;

function showErrorMessage(message){
    errorMessage = document.getElementById("error_message");
    if (errorMessage === null){
        errorMessage = document.createElement("p");
        errorMessage.id = "error_message";
        errorMessage.style.color = "red";
        errorMessage.innerHTML = message;
        searchDiv.appendChild(errorMessage);
    }
    else{
        errorMessage.innerHTML = message;
    }
}

function submitSearch(event){
    event.preventDefault();
    var search = ingredientSearchBox.value;
    if (search.length === 0){
        search = "/ingredients/pid=0";
        window.location.replace(search);
    }
    else{
        search = "/ingredients/pid=0&search=" + search;
        window.location.replace(search);
    }
}

searchButton.addEventListener("click", submitSearch);
window.addEventListener("keypress", function(event){
    if (event.key === "Enter"){
        searchButton.click();
    }
});