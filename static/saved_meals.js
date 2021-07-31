"use strict";

let CUISINE_COUNT = 0;

// Cuisine input logic

console.log("this is CUISINE_COUNT before selecting: " + CUISINE_COUNT);
$(".cuisine").on("click", function() {
    if ($(this).hasClass("not")) {
        CUISINE_COUNT += 1;
        $(this).removeClass("not");
        $(this).addClass("selected");
        console.log("this is CUISINE_COUNT after selecting: " + CUISINE_COUNT);
    }
        
    else {
        CUISINE_COUNT -= 1;
        $(this).removeClass("selected");
        $(this).addClass("not");
        console.log("this is CUISINE_COUNT after unselecting: " + CUISINE_COUNT);
    }

    if (CUISINE_COUNT >= 3) {
        $(".not").attr("disabled", "");
        console.log("this is CUISINE_COUNT after disabling: " + CUISINE_COUNT);
    }

    else {
        $(".not").removeAttr("disabled");
    }

});


// To make cuisine input required

function checkCuisineInput(evt) {
  if ($('div.checkbox-group :checkbox:checked').length === 0) {
      evt.preventDefault();
      $("#cuisine-error").html("Select at least one cuisine.");
  }
  else {
      $("#cuisine-error").html("");
      return true;   
  }  
}

$("#mealPlanSubmit").on("click", checkCuisineInput);


// To initialize tooltip in modal

$(document).ready(function() {
    $("body").tooltip({ selector: '[data-toggle=tooltip]' });
});



// Nutrition charts for saved recipes


let ctx_donut7 = $("#fatTotal").get(0).getContext("2d");
let ctx_donut8 = $("#carbsTotal").get(0).getContext("2d");
let ctx_donut9 = $("#proteinTotal").get(0).getContext("2d");

$.get("/fat-data.json", function(data) {
    let fatTotalChart = new Chart(ctx_donut7, {
                            type: "doughnut",
                            data: data,
                            options: {
                                        legend: {
                                                display: false
                                        },
                                        title: {
                                                display: true,
                                                text: 'Fat'
                                            },
                                        responsive: true
                                    }
    });
});

$.get("/carbs-data.json", function(data) {
    let carbsTotalChart = new Chart(ctx_donut8, {
                            type: "doughnut",
                            data: data,
                            options: {
                                        legend: {
                                                display: false
                                        },
                                        title: {
                                                display: true,
                                                text: 'Carbs'
                                            },
                                        responsive: true
                                    }
    });
});

$.get("/protein-data.json", function(data) {
    let proteinTotalChart = new Chart(ctx_donut9, {
                            type: "doughnut",
                            data: data,
                            options: {
                                        legend: {
                                                display: false
                                        },
                                        title: {
                                                display: true,
                                                text: 'Protein'
                                            },
                                        responsive: true
                                    }
    });
});