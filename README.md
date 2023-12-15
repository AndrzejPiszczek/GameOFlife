# Documentation of Changes in the "Game of Life" Project

## Short Description of Changes:
The "Game of Life" project underwent several enhancements to meet new requirements and improve user interaction with the game. These changes include:

1. **Real-Time Simulation:**
   - A timer was added to the game, enabling the automatic generation of new game states at regular intervals.

2. **Pause/Resume Functionality:**
   - Implemented a pause/resume button allowing the user to halt and resume the simulation as needed.

3. **Save and Load Game State:**
   - Enabled saving the current game state to a file and loading it. This functionality was implemented using standard system dialogues.

4. **UI Modification:**
   - Shifted buttons below the game area, changing their colors and sizes for better intuition and aesthetics.

## Libraries Used:
- **Pygame:** For creating the game window, handling events, drawing graphics, and managing timers.
- **NumPy:** To manage the game state efficiently using arrays.
- **Tkinter:** For creating save and load file dialogues.

## Techniques and Methods:
- **Singleton:** Ensures stability in the operation of Pygame and Tkinter by avoiding multiple initializations.
- **Command:** Facilitates adding new functionalities to buttons without modifying existing code, beneficial for future scalability and maintenance of the project.
- **Observer:** Allows for smooth animation and game state updates, reacting to timer events in an efficient and organized manner.
