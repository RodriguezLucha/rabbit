import { render } from "react-dom";
import React, { useState }from "react";
import clamp from "lodash-es/clamp";
import { useSpring, animated } from "react-spring";
import { useGesture } from "react-with-gesture";
import "./App.css";
import openSocket from "socket.io-client";

const socket = openSocket("http://localhost:5000");

function App() {
  const [{ xy }, set] = useSpring(() => ({ xy: [0, 0] }));
  const bind = useGesture(({ down, delta, velocity }) => {
    velocity = clamp(velocity, 1, 8);
    set({
      xy: down ? delta : [0, 0],
      config: { mass: velocity, tension: 500 * velocity, friction: 50 },
    });
  });
  return (
    <animated.div
      {...bind()}
      style={{
        transform: xy.interpolate((x, y) => {
          let string = `translate3d(${x}px,${y}px,0)`;
          socket.emit("message", string);
          return string;
        }),
      }}
    />
  );
}

export default App;
