  // ################################
  // SOCKETIO BROWSER COMMANDS (SEND)
  // ################################

  $( "#btnBrowserBack" ).click(function() {
    socket.emit('remote', {
        cmd: "browser_back"
    })
  });

  $( "#btnBrowserForward" ).click(function() {
    socket.emit('remote', {
        cmd: "browser_forward"
    })
  });

  $( ".btnPlayMovie" ).click(function(e) {
    e.preventDefault();
    filename = $(this).text();
    console.log(filename);
    socket.emit('remote', {
        cmd: "play_movie",
        movie: filename
    })
  });

  $( "#btnNightmode" ).click(function() {
    socket.emit('remote', {
        cmd: "night_mode"
    })
  });

  var socket = io.connect();
  
  // on_connect (when browser connects to server)
  socket.on('connect', function(data){
    console.log("Remote connected to server!")
  })

  // Logs commands in console to show that they were received
  socket.on('cmdlog', function(data){
    console.log("Server received: " + data.data);
  })

  // ################################
  // SOCKETIO BROWSER COMMANDS (RECEIVE)
  // ################################

  socket.on('browser_back', function(){
    console.log("execute browser_back");
    // If we don't check for the video_id/player
    // the remote page also navigates because it inherits base.html
    if ($("#video_id").length) {
      window.history.back();
    }
  })
  socket.on('browser_forward', function(){
    console.log("execute browser_forward");
    if ($("#video_id").length) {
      window.history.forward();
    }
  })
  socket.on('play_movie', function(movie){
    console.log("execute play_movie");
    console.log("Play movie file: " + movie);
    var remoteUrl = window.location.href + "lazy";
    // Make sure we're on page with video_id before we
    // redirect, this makes sure that the lazy/remote page
    // isn't redirected also.
    if ($("#video_id").length){
      window.location.replace("/" + movie);
    }else if($(".isindex").length){
      // quick check to see if we're on index page
      window.location.replace("/" + movie);
    }
  })
  socket.on('night_mode', function(data){
    console.log("execute night_mode");
    $("body").toggleClass("nightmode");
  })