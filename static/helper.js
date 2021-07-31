"use strict";

let COUNTER = 0;
let HIDDEN_INPUTS;

let fatTotal = 0;
let carbsTotal = 0;
let proteinTotal = 0;

// To initialize tooltips and define HIDDEN_INPUTS

$(document).ready(function() {
    $("body").tooltip({ selector: '[data-toggle=tooltip]' });
    HIDDEN_INPUTS = $("[type=hidden]");
});


// Behavior of recipe-select buttons 

let button = $(".recipe-select");
console.log("this is the counter before clicking: " + COUNTER);
// hold saved recipes in an object:
let dataObj = {
    "1": "",
    "2": "",
    "3": "",
    "4": "",
    "5": ""
};

function changeButton(evt) {
    console.log(this);
    if ($(this).html() === "Select") {
        COUNTER += 1;
        console.log("this is the counter after saving: " + COUNTER);
        $(this).removeClass("unsaved");
        $(this).addClass("saved");
        let buttonData = $(this).data();    // a dict
        fatTotal += $(this).data("fat");
        carbsTotal += $(this).data("carbs");
        proteinTotal += $(this).data("protein");

        for (let day in dataObj) {
            if (dataObj[day] === "") {
                dataObj[day] = JSON.stringify(buttonData);
                $(this).html("Saved for Day " + day);
                $(HIDDEN_INPUTS[day-1]).attr("value", dataObj[day]);
                break;
                }
            }
        } 

    else {
        let day = $(this).html()[$(this).html().length - 1]-1;
        $(HIDDEN_INPUTS[day]).attr("value", "");
        dataObj[day+1] = "";
        $(this).html("Select");
        $(this).removeClass("saved");
        $(this).addClass("unsaved");
        fatTotal -= $(this).data("fat");
        carbsTotal -= $(this).data("carbs");
        proteinTotal -= $(this).data("protein");
        COUNTER -= 1;
        console.log("this is the counter after unsaving: " + COUNTER);
        }

    if (COUNTER !== 0) {
        $(".progress-bar").html(COUNTER + " of 5");
    }
    else {
        $(".progress-bar").html("");
    }
    $(".progress-bar").css("width", COUNTER*20 + "%");
    $(".progress-bar").attr("aria-valuenow", COUNTER*20);

    if (COUNTER === 5) {
        $("#create").css("visibility", "visible");
        $(".unsaved").css("visibility", "hidden");
        $(".results-msg").css("visibility", "hidden");
        }
    else {
        $(".unsaved").css("visibility", "visible");
        $("#create").css("visibility", "hidden");
        $(".results-msg").css("visibility", "visible");
        }

    //make 3 tracker charts
    makeTracker();

}

button.on('click',changeButton);



// NUTRITION CHARTS

let options = {
    legend: {
            display: false
    }
};

function makeNutriDict(id, nutrient) {
    let button = $("#"+id);
    let percentOfDailyNeeds;

    if (nutrient === "Fat") {
        percentOfDailyNeeds = button.data("fat");
    }
    else if (nutrient === "Carbs") {
        percentOfDailyNeeds = button.data("carbs");
    }
    if (nutrient === "Protein") {
        percentOfDailyNeeds = button.data("protein");
    }

    // if (percentOfDailyNeeds > 100) {
    //     percentOfDailyNeeds = 100;
    // }

    let data_dict = {
                "labels": [
                    nutrient,
                    "remainder"
                ],
                "datasets": [
                    {
                        "data": [percentOfDailyNeeds, 100-percentOfDailyNeeds],
                        "backgroundColor": [
                            "#4A7E13",
                            "gray"
                        ],
                        "hoverBackgroundColor": [
                            "#4A7E13",
                            "gray"
                        ]
                    }]
            };

    return data_dict;
}

function makeFatChart(data, chart) {
      options["title"] = {
            display: true,
            text: 'Fat'
        };
      let fatChart = new Chart(chart, {
                                              type: 'doughnut',
                                              data: data,
                                              options: options
                                            });
    }

function makeCarbsChart(data, chart) {
      options["title"] = {
            display: true,
            text: 'Carbs'
        };
      let carbsChart = new Chart(chart, {
                                              type: 'doughnut',
                                              data: data,
                                              options: options
                                            });
    }

function makeProteinChart(data, chart) {
      options["title"] = {
            display: true,
            text: 'Protein'
        };
      let proteinChart = new Chart(chart, {
                                              type: 'doughnut',
                                              data: data,
                                              options: options
                                            });
    }

function makeCharts() {
    let id = this.id;
    let fat = makeNutriDict(id, "Fat");
    let carbs = makeNutriDict(id, "Carbs");
    let protein = makeNutriDict(id, "Protein");

    let ctx_donut1 = $("#donutChart1").get(0).getContext("2d");
    let ctx_donut2 = $("#donutChart2").get(0).getContext("2d");
    let ctx_donut3 = $("#donutChart3").get(0).getContext("2d");

    makeFatChart(fat, ctx_donut1);
    makeCarbsChart(carbs, ctx_donut2);
    makeProteinChart(protein, ctx_donut3);

    $(".hide").css("visibility", "visible");
}


function makeNutriDictForTracker(nutrient) {
    let percentOfWeeklyNeeds;
    let color = "#4A7E13";

    if (nutrient === "Fat") {
        percentOfWeeklyNeeds = (fatTotal * 3) / 5;
    }
    else if (nutrient === "Carbs") {
        percentOfWeeklyNeeds = (carbsTotal * 3) / 5;
    }
    if (nutrient === "Protein") {
        percentOfWeeklyNeeds = (proteinTotal * 3) / 5;
    }

    if (percentOfWeeklyNeeds > 100) {
        percentOfWeeklyNeeds = 100;
        color = "#dd3c45";
    }

    let data_dict = {
                "labels": [
                    nutrient,
                    "remainder"
                ],
                "datasets": [
                    {
                        "data": [percentOfWeeklyNeeds, 100-percentOfWeeklyNeeds],
                        "backgroundColor": [
                            color,
                            "gray"
                        ],
                        "hoverBackgroundColor": [
                            color,
                            "gray"
                        ]
                    }]
            };

    return data_dict;
}

function makeTracker() {
    let fat = makeNutriDictForTracker("Fat");
    let carbs = makeNutriDictForTracker("Carbs");
    let protein = makeNutriDictForTracker("Protein");

    let ctx_donut4 = $("#fatTracker").get(0).getContext("2d");
    let ctx_donut5 = $("#carbsTracker").get(0).getContext("2d");
    let ctx_donut6 = $("#proteinTracker").get(0).getContext("2d");

    makeFatChart(fat, ctx_donut4);
    makeCarbsChart(carbs, ctx_donut5);
    makeProteinChart(protein, ctx_donut6);

}


// To initialize popovers


$('[data-toggle="popover"]').popover({
  html: true,
  content: '<canvas id="donutChart1" width="25" height="25"></canvas><canvas id="donutChart2" width="25" height="25"></canvas><canvas id="donutChart3" width="25" height="25"></canvas>',
}).on('shown.bs.popover', makeCharts);


$('.popover-dismiss').popover({
  trigger: 'focus'
});



// More button

let clicks = 0;

function showResults(results) {
    let recipes = results["results"];
    console.log("Recipes:" + recipes);
    let remainder = results["remainder"];
    console.log("Remainder:" + remainder);
    let clickCount = results.clicks;
    console.log("Clicks:" + clickCount);

    for (let i = 0; i < recipes.length; i++) {
        let content = '<div class="col-md-4 col-sm-3 col-xs-2" id="more-' + clickCount + '"> \
                        <div class="card mb-4" id=' + recipes[i]["id"] + '> \
                          <a href=' + recipes[i]["url"] + ' target="_blank"><img class="card-img-top" src=' + recipes[i]["image"] + '></a> \
                          <div class="card-body"> \
                            <h5 class="card-title">' + recipes[i]["title"] + '</h5> \
                            <p class="card-text">Prep time: ' + recipes[i]["readyInMinutes"] + ' min</p>' +           
                            '<button type="button" class="btn btn-danger more-recipe-select unsaved" id="button-' + (i + (clickCount*12)) + '" data-id=' + recipes[i]["id"] + ' data-title="' + recipes[i]["title"] + '" data-url=' + recipes[i]["url"] + ' data-image=' + recipes[i]["image"] + ' data-prep-time=' + recipes[i]["readyInMinutes"] + ' data-fat=' + recipes[i]["nutrition"][1]["percentOfDailyNeeds"] + ' data-carbs=' + recipes[i]["nutrition"][3]["percentOfDailyNeeds"] + ' data-protein=' + recipes[i]["nutrition"][7]["percentOfDailyNeeds"] + '>Select</button> \
                            <a tabindex="0" class="btn btn-outline-danger nutrition" id="btn-' + (i + (clickCount*12)) + '" role="button" data-toggle="popover" data-trigger="focus" data-html="true" data-fat=' + recipes[i]["nutrition"][1]["percentOfDailyNeeds"] + ' data-carbs=' + recipes[i]["nutrition"][3]["percentOfDailyNeeds"] + ' data-protein=' + recipes[i]["nutrition"][7]["percentOfDailyNeeds"] + ' title="Daily Intake">Nutrition</a> \
                          </div> \
                        </div> \
                      </div>';
        $(".results").append(content);
    }
    
    // event handlers for select and nutrition buttons
    $(".more-recipe-select").on('click',changeButton);

    $('[data-toggle="popover"]').popover({
      html: true,
      content: '<canvas id="donutChart1" width="25" height="25"></canvas><canvas id="donutChart2" width="25" height="25"></canvas><canvas id="donutChart3" width="25" height="25"></canvas>',
    }).on('shown.bs.popover', makeCharts);


    $('.popover-dismiss').popover({
      trigger: 'focus'
    });

    // use remainder to hide "more" button
    if (remainder === 0) {
        $("#more").css("visibility", "hidden");
    }

    // scroll to new results
    $('html, body').animate({ scrollTop: $("#more-" + clickCount).offset().top }, 800);
}


function getMoreResults(evt) {
    // make cuisine inputs into an array
    let cuisines = $(".cuisines");
    let cuisinesArray = [];
    for (let i=0; i < cuisines.length; i++) {
        let cuisineType = cuisines[i].dataset.cuisine;
        cuisinesArray.push(cuisineType);
    }

    // make intolerant inputs into an array
    let intolerant = $(".intolerant");
    let intolerantArray = [];
    for (let i=0; i < intolerant.length; i++) {
        let intolerantType = intolerant[i].dataset.intolerant;
        intolerantArray.push(intolerantType);
    } 
    
    clicks += 1

    let formInputs = {
        "cuisines": cuisinesArray,
        "exclude": $("#exclude").val(),
        "intolerant": intolerantArray,
        "clicks": clicks 
    };
    console.log("Cuisines:" + formInputs.cuisines);
    console.log("Exclude:" + formInputs.exclude);
    console.log("Intolerant:" + formInputs.intolerant);
    console.log("Clicks in formInputs:" + formInputs.clicks);

    $.get("/more-results.json", formInputs, showResults);
}

$("#more").on("click", getMoreResults);


// Loading message

$(document).on({
    ajaxStart: function() { $('.loading').css("visibility", "visible"); },
     ajaxStop: function() { $('.loading').css("visibility", "hidden"); }    
});
