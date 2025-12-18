"use strict";

/*----- Add event on multiple elements ------*/
const addEventOnElements = function (elements, eventType, callback) {
  for (const elem of elements) {
    elem.addEventListener(eventType, callback);
  }
};

/*----- Toggle search box in mobile device ------*/
const searchBox = document.querySelector("[search-box]");
const searchTogglers = document.querySelectorAll("[search-toggler]");

addEventOnElements(searchTogglers, "click", function () {
  searchBox.classList.toggle("active");
});

/*
Store MovieId in Local Storage when I click any movie card
.*/
const getMovieDetail = function (movieId) {
  window.localStorage.setItem("movieId", String(movieId));
};

const getMovieList = function (urlParam, genreName) {
  window.localStorage.setItem("urlParam", urlParam);
  window.localStorage.setItem("genreName", genreName);
};

/* ----- Horizontal scroll transformation with border considered------*/
function transformScroll(event) {
  if (!event.deltaY) {
    return;
  }
  if (event.currentTarget.scrollLeft === 0 && event.deltaY < 0) return;  
  if (event.currentTarget.scrollLeft + event.currentTarget.clientWidth >= event.currentTarget.scrollWidth && event.deltaY > 0) {
    return;
  } 
  event.currentTarget.scrollLeft += event.deltaY + event.deltaX;
  event.preventDefault();
  
}

function toLogin() {
  // Save current page before redirecting
  localStorage.setItem('loginRedirect', window.location.href);
  window.location.href = './login.html';
}

