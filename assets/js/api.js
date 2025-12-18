"use strict";

const api_key = "ad59ab19c532565377c9244bd9b406e6";  /* TMDB API Key */
const imageBaseURL = "http://image.tmdb.org/t/p/";

/*--------- 
Fetch data from a server using the 'url' and passes the result in JSON data to a 'callback' function, along with an optional parameter if has 'optionalParam'.
----------*/

const fetchDataFromServer = function (url, callback, optionalParam) {
  fetch(url)
    .then((response) => response.json())
    .then((data) => callback(data, optionalParam));
};

export { imageBaseURL, api_key, fetchDataFromServer };
