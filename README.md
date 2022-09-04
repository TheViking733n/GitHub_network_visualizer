# GitHub_network_visualizer
Get a dynamic graph like representation of your GitHub network in your browser. You can also drag the nodes to see the physics simulation.

## How it works?
The [visualize.py](/visualize.py?raw=true) does a BFS (Breadth-first search) on all the followers and following of the root handle. The BFS also keeps a visited check, so that the network is a tree, because a graph network was very messy it was hard to analyse it. To stop the BFS, there is a MAX_DEPTH check in the code. You can also change the MAX_DEPTH to see a bigger network, provided your browser can render it.

## Dependencies
- [requests](https://pypi.org/project/requests/)
- [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
- [pyvis](https://pypi.org/project/pyvis/)

## Installation
```sh
pip install requests beautifulsoup4 pyvis
```

## Usage
```sh
python visualize.py
```
## Screenshot
![Alt text](/Screenshot.jpg?raw=true)
