$(document).ready(() => {
  // Creating movie cards
  var moviesList = [];
  const MakeMovieCards = () => {
    for(var i in data){
      moviesList.push(
        <div className="movie-card" style={{ backgroundImage: `url(${data[i]["img"]})` }} key={data[i]["title"]} id={data[i]["title"]} movie={data[i]["movie"]}>
          <div className="title">
            <input type="hidden"></input>
          </div>
        </div>
      );
    }
    return(moviesList)
  };
  ReactDOM.render(<MakeMovieCards />, document.getElementById("movies"));
  // Play movie when clicking on movie cards
  var movies = document.getElementsByClassName("movie-card");
  for (var n in movies){
    if (typeof movies[n] === "object"){
      movies[n].onclick = (e) => {
        var movie = e.target.getAttribute("movie");
        const modal = document.getElementsByClassName("modal")[0];
        modal.style.display = "block";
        const MovieControls = () => {
          return(
            <div className="movie-controls">
              <i className="fas fa-times"/>
              <h5>{e.target.id}</h5>
              <video controls>
                <source src={movie+"#t=0.5"}/>
              </video>
            </div>
          )
        };
        setTimeout(() => {
          ReactDOM.render(<MovieControls/>,modal);
          document.getElementsByClassName("fas fa-times")[0].onclick = () => {
            document.getElementsByTagName("video")[0].pause();
            modal.style.display = "none";
          }
        },10)
      };
    }
  }
})