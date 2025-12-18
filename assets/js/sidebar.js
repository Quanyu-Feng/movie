"use strict";

import { api_key, fetchDataFromServer } from "./api.js";

export function generateSidebar() {
  /*------
  From array of objects to a dictionary
  Fetch all genres eg: [{ "id": "123", "name": "Action" }]
  then change genre formate eg: { 123: "Action" }
  -------*/
  const genreList = {};

  fetchDataFromServer(
    `https://api.themoviedb.org/3/genre/movie/list?api_key=${api_key}`,
    function ({ genres }) {
      for (const { id, name } of genres) {
        genreList[id] = name;
      }

      genreLink();
    }
  );

  const sidebarInner = document.createElement("div");
  sidebarInner.classList.add("sidebar-inner");

  sidebarInner.innerHTML = `
    <div class="sidebar-list">
      <p class="title">Genre</p>
    </div>

    <div class="sidebar-list">
      <p class="title">Language</p>
      
      <a
        href="./movie-list.html"
        menu-close
        class="sidebar-link"
        onClick='getMovieList("language=zh-CN&region=CN&with_origin_country=CN&with_original_language=zh", "China")'
        >China / 中国电影 </a>
      <a
        href="./movie-list.html"
        menu-close
        class="sidebar-link"
        onClick='getMovieList("with_original_language=en", "English")'
        >English </a>
      <a
        href="./movie-list.html"
        menu-close
        class="sidebar-link"
        onClick='getMovieList("language=zh-HK&region=HK&with_origin_country=HK", "Hong Kong")'
        >Hong Kong / 港產片 </a>
      

        

    </div>

    <div class="sidebar-footer">
      <p class="copyright">
        Wong Chun Kin (23022252g) <br>
        Feng Quanyu (25061357g) <br>
        For COMP5322 Project
      </p>

      <p class="copyright">
      Powered by TMDB
      <img
        src="./assets/images/tmdb-logo.svg"
        width="130"
        height="17"
        alt="the movie database logo"
      />
      </p>
    </div>
  `;

  const genreLink = function () {
    for (const [genreId, genreName] of Object.entries(genreList)) {
      const link = document.createElement("a");
      link.classList.add("sidebar-link");
      link.setAttribute("href", "./movie-list.html");
      link.setAttribute("menu-close", "");
      link.setAttribute(
        "onClick",
        `getMovieList("with_genres=${genreId}", "${genreName}")`
      );
      link.textContent = genreName;

      sidebarInner.querySelectorAll(".sidebar-list")[0].appendChild(link);
    }

    const sidebar = document.querySelector("[sidebar]");
    sidebar.appendChild(sidebarInner);
    toggleSidebar(sidebar);
  };

  //   Toggle sidebar in mobile screen
  const toggleSidebar = function (sidebar) {
    const sidebarBtn = document.querySelector("[menu-btn]");
    const sidebarTogglers = document.querySelectorAll("[menu-toggler]");
    const sidebarClose = document.querySelectorAll("[menu-close]");
    const overlay = document.querySelector("[overlay]");

    addEventOnElements(sidebarTogglers, "click", function () {
      sidebar.classList.toggle("active");
      sidebarBtn.classList.toggle("active");
      overlay.classList.toggle("active");
    });

    addEventOnElements(sidebarClose, "click", function () {
      sidebar.classList.remove("active");
      sidebarBtn.classList.remove("active");
      overlay.classList.remove("active");
    });
  };
}
