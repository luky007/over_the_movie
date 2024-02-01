> [!NOTE]  
> This project is part of a dummy simulation.

# Over the Movie

Script collections for cleaning and inserting Over the Movie client data into a mySQL DB.

## How to contribute:
### Using docker container
- Open this project inside a docker container. The use of VS code dev containers is encouraged.
- Initialize the project dependencies by using Poetry:
```bash
poetry install --no-root
```

### Manual install
- Setup the conda environment with:
```bash
conda env create -f environment.yml
```
- Then initialize the project dependencies by using Poetry:
```bash
poetry install --no-root
```
