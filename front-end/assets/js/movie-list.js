"use strict";

import { api_key, fetchDataFromServer } from "./api.js";
import { createMovieCard } from "./movie-card.js";
import { search } from "./search.js";
import { generateSidebar } from "./sidebar.js";
import { showUsername } from "./login-display.js";

// collect genre, name & url paramenter from local storage
const genreName = window.localStorage.getItem("genreName");
const urlParam = window.localStorage.getItem("urlParam");
const pageContent = document.querySelector("[page-content]");
let sort_choice = localStorage.getItem("sort_choice") || "popularity.desc";
generateSidebar();
showUsername();

let currentPage = 1;
let totalPages = 0;
let voteRequired = (sort_choice === "vote_average.desc") ? 50 : 0;

fetchDataFromServer(
  `https://api.themoviedb.org/3/discover/movie?include_adult=false&api_key=${api_key}&sort_by=${sort_choice}&page=${currentPage}&${urlParam}&vote_count.gte=${voteRequired}&without_genres=10402'`,
  function ({ results: movieList, total_pages }) {
    totalPages = total_pages;

    document.title = `All ${genreName} movies - myMovie Super`;

    const movieListElem = document.createElement("section");
    movieListElem.classList.add("movie-list", "genre-list");
    movieListElem.ariaLabel = `${genreName} Movies`;

    movieListElem.innerHTML = `
      <div class="title-wrapper">
        <h1 class="heading">All ${genreName} Movies</h1>
      </div>
      <div class = "sort-choice">
        <label for="cars">Sorted by:</label>
        <select name="sortedBy" id="sort">
         <option value="popularity.desc">Overall Popularity</option>
          <option value="vote_average.desc">Rating</option>
         <option value="primary_release_date.desc">Primary Release Date</option>
         <option value="revenue.desc">Revenue</option>
        </select>
        <button class="btn submit" type="submit">Refresh</button>
        
      </div>
      <div class="grid-list"></div>

      <button class="btn load-more" load-more>Load More</button>
    `;

    /* ensure selction is same with sort_choice */
    movieListElem.querySelector("select#sort").value = sort_choice;

    /* add sorting algorithm js*/
    movieListElem
      .querySelector("button.submit")
      .addEventListener("click", function () {
        sort_choice = movieListElem.querySelector("select#sort").value;
        localStorage.setItem("sort_choice", sort_choice);
        window.location.reload();
      });
    /*
    Add movie card based on fetched item
    */
    for (const movie of movieList) {
      const movieCard = createMovieCard(movie);

      movieListElem.querySelector(".grid-list").appendChild(movieCard);
    }

    pageContent.appendChild(movieListElem);
    
    /*
    Load more button functionality
    */
    document
      .querySelector("[load-more]")
      .addEventListener("click", function () {
        if (currentPage >= totalPages) {
          this.style.display = "none"; //this == loading-btn
          return;
        }

        currentPage++;
        this.classList.add("loading"); //this == loading-btn

        fetchDataFromServer(
          `https://api.themoviedb.org/3/discover/movie?include_adult=false&api_key=${api_key}&sort_by=popularity.desc&page=${currentPage}&${urlParam}`,
          ({ results: movieList }) => {
            this.classList.remove("loading"); //this == loading-btn

            for (const movie of movieList) {
              const movieCard = createMovieCard(movie);

              movieListElem.querySelector(".grid-list").appendChild(movieCard);
            }
          }
        );
      });
  }
);

search();
