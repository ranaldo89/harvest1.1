"use strict";

// new account form - validate password match

function passwordMatch() {
    let pw = $("#pw").val();
    let confirmPw = $("#confirm_pw").val();

    if (pw !== confirmPw) {
        $("#pw-msg").html("Passwords must match!");
        $("#pw").addClass("error");
    }
    else {
        $("#pw-msg").html("Success");
        $("#pw").removeClass("error");
    }
}

$("#confirm_pw").keyup(passwordMatch);


// new account form - check for unique email address

function showEmailValidation(results) {

    if (!results) {
        $("#email-msg").html("That email is already registered! Try another.");
        $("#email").addClass("error");
    }
    else {
        $("#email-msg").html("");
        $("#email").removeClass("error");
    }
}

function checkEmailExistence(evt) {
    $.get("/emails-from-db", {"email": $("#email").val()}, showEmailValidation);

}

$("#email").blur(checkEmailExistence);


// new account form - disable submit button if errors present

function checkErrors(evt) {
    if ($("#pw").hasClass("error") || $("#email").hasClass("error")) {
        evt.preventDefault();
    }
    else {
        return true;
    }
}

$("#newAccountSubmit").on("click", checkErrors);


// sign in form - validate user credentials

function processCredentials(results) {
    if (!results) {
        $("#signin-error").html("Incorrect email/password.");
    }
    else {
        $("#si-form").trigger("submit");
    }
}

function checkCredentials(evt) {
    evt.preventDefault();

    let formInputs = {
        "email": $("#si-email").val(),
        "pw": $("#si-pw").val()
    };

    $.get("/check-credentials", formInputs, processCredentials);
}

$("#si-submit").on("click", checkCredentials);


// validate email address format on new account form

$(function () {
    $("input[name=email]").on("invalid", function () {
        this.setCustomValidity("Please enter a valid email address.");
    });
});

