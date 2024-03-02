# The Monkey Run Story

## Inspiration
Monkey Run was conceived on the idea of joining exercise and gaming together. There has been more evidence than ever for the health benefits of consistent exercising. For those who lack motivation to exercise, this game provides a fun & unique way to exercise! 

## What it does
In this endless-runner game, the goal is to keep the monkey alive for as long as possible. The player can make the monkey move by moving in real life. With a camera set up to track the player’s movement, the monkey can either jump, duck or swing. The monkey has to avoid all kinds of obstacles that appear at random, such as crocodiles, eagles, or sharp spikes. This encourages players to do exercises while both staying engaged and having fun!

## How we built it
We used mediapipe which uses opencv on the backend to detect the movement of the player, each body part (head, shoulders, hands, etc..) was tracked to detect movements such as jumping, ducking, or swinging. To build the game itself, we used godot to program the game mechanics and integrate textures.

## Challenges we ran into
One of the most prominent challenges we ran into was creating a bridge that links movement detection via mediapipe to the game we built with godot. Having to trigger an event in the game after detecting a motion from the player was a problem with no clear solution. We started by researching online how to achieve this functionality….

## Accomplishments that we're proud of
We managed to detect different types of motion from the player by tracking the location of different body parts and how they are positioned with respect to each other. In addition, the movements automatically scale based on how close the player is to the camera. 

## What we learned
This experience was more than a window to not just technical learning, where we explored the mechanics of the Godot game engine as well as the opencv and mediapip computer vision libraries. It was also an opportunity to work collaboratively on a very unique project and had to assign crucial roles for each team member to achieve our goals. We had to divide tasks between working with the Godot game engine, the computer vision libraries, and the bridge between the two components. Being flexible and working in a dynamic team environment that often changed as we worked our way towards perfecting the project was a necessary skill we had to learn.

## What's next for Monkey Run


## Built With
opencv godot c++ mediapipe
