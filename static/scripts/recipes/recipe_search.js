let searchDiv = document.getElementById("recipe_search_div");
let searchBox = document.getElementById("recipe_search");
let searchAddItemButton = document.getElementById("recipe_search_add");
let searchAddItemDiv = document.getElementById("recipe_search_add_item_div");
let searchAddItemSearchBox = document.getElementById("recipe_item_search_text_box");
let searchAddItemSearchAddButton = document.getElementById("recipe_search_add");
let searchAddItemSearchAvoidButton = document.getElementById("recipe_search_avoid");
let searchConfirmButton = document.getElementById("recipe_search_button");
let searchResults = document.getElementById("drop_down_content");

function replaceAll(data, value, replacement){
    while (data.includes(value)){
        data = data.replace(value, replacement);
    }
    return data;
}

function showErrorMessage(message, parentElement){
    errorMessage = document.getElementById("error_message");
    if (errorMessage === null){
        errorMessage = document.createElement("p");
        errorMessage.id = "error_message";
        errorMessage.style.color = "red";
        errorMessage.innerHTML = message;
        parentElement.appendChild(errorMessage);
    }
    else{
        errorMessage.innerHTML = message;
    }
}

function addIngredient(avoid){
    console.log(searchBox.value.length);
    if (searchAddItemSearchBox.value.length < 1){
        return;
    }
    //Check here if the ingredient is valid, if not, don't add it.
    if (avoid === true){
        console.log("Woah");
        if (searchBox.value.length > 0){
            searchBox.value = searchBox.value + " " + searchAddItemSearchBox.value;
        }
        else{
            searchBox.value = searchAddItemSearchBox.value;
        }
    }
    else{
        if (searchBox.value.length > 0){
            searchBox.value = searchBox.value + " -" + searchAddItemSearchBox.value;
        }
        else{
            searchBox.value = "-" + searchAddItemSearchBox.value;
        }
    }
    searchAddItemSearchBox.value = "";
}

function getClosestName(){
    $.ajax({
        type: "GET",
        url: "/database/searchnames/search=" + searchAddItemSearchBox.value.replaceAll(" ", "_"),
        success: function(response){
            if (searchResults.hasChildNodes()){
                searchResults.innerHTML = "";
            }
            var split_response = [];
            split_response = response.split("|");
            if (split_response.length < 1 || response === "" || this.status !== "200"){
                split_response = ["no results"];
            }
            for (var i = 0; i < split_response.length; i++){
                if (split_response[i] !== "DELETED"){
                    var searchOption = document.createElement("a");
                    searchOption.innerHTML = replaceAll(split_response[i], "_", " ");
                    if (split_response[i] !== "no results"){
                        searchOption.id = split_response[i];
                    }
                    else{
                        searchOption.id = "invalid";
                    }
                    searchOption.className = "drop_down_content_item";
                    searchResults.appendChild(searchOption);
                }
            }
            searchResults.style.display = "block";
            var searchRectangle = searchBox.getBoundingClientRect();
            searchResults.style.left = (searchRectangle.x);
            searchResults.style.top = ((searchRectangle.y) + searchRectangle.height);
            for (var i = 0; i < searchResults.childNodes.length; i++){
                searchResults.childNodes[i].addEventListener("click", function(event){
                    searchAddItemSearchBox.value = event.target.id;
                    searchResults.innerHTML = "";
                });
            }
        },
        error: function(){
            searchResults.innerHTML = "";
            var searchOption = document.createElement("a");
            searchOption.innerHTML = "no results";
            searchOption.id = "invalid";
            searchOption.className = "drop_down_content_item";
            searchResults.appendChild(searchOption);
            searchResults.style.display = "block";
            var searchRectangle = searchBox.getBoundingClientRect();
            searchResults.style.left = (searchRectangle.x);
            searchResults.style.top = ((searchRectangle.y) + searchRectangle.height);
        }
    });
}

//Event Listeners
searchAddItemSearchAddButton.addEventListener("click", function (event){ event.preventDefault(); addIngredient(true); });
searchAddItemSearchAvoidButton.addEventListener("click", function (event){ event.preventDefault(); addIngredient(false); });
searchAddItemSearchBox.addEventListener("keyup", function (event){
    if (searchAddItemSearchBox.value.length > 2){
        getClosestName();
    }
    else{
        if (searchResults.hasChildNodes()){
            searchResults.innerHTML = "";
        }
    }
});