import React, { useState } from "react";
import io from "socket.io-client";
import openSocket from "socket.io-client";
import "./App.css";

const socket = openSocket("http://localhost:5001");
function ab2str(buf) {
  return String.fromCharCode.apply(null, new Uint16Array(buf));
}

function App() {
  const [str, setStr] = useState("translate3d(30px,30px,0)");
  socket.on("message2", function (data) {
    let result = data.substring(2, data.length - 1);
    setStr(result);
  });
  return (
    <div className="App">
      <div className="shape" style={{ transform: str }}></div>
    </div>
  );
}

export default App;
