# genericInteractionNetwork
Commandline app to create pathway object from a json file.

Must run from the outermost directory of the project.

Any file that follows with It is for the user to use and apply.

Each user module has flag options to customize experience.

1. Create and activate virtual environment (venv, conda)
2. Then install requirements: pip3 -r install requirements.txt
3. ...Explain modules and flags

- Ideas:
  - kinetics (cooperative, feedback loop)
  - genetic algorithm (customizable to what parameters, what data, constraints, and fitting hyperparameters) --> for prototype may implement the following packages initially (geneticalgorithm or pyGAD)
  - active/inactive enzyme states (manage rates appropriately in modify, dynamic, and fitting)
  - network diagram pointing to arrows and double arrows to signify reversibility
  - dynamic graphing module
  - complete statistics and modify modules
  - logging and documentation (including code comments)
- Goals:
  - Once fitted examine:
    - dynamics in steady state and stress
    - sensitivity of dynamics to each key signalling molecule
    - machine learning to predict outcomes (Ca2+ levels, phagocytosis, etc.) based on an input of key signalling state
      - perhaps the type of stimuli could be inputs?
