# Dijkstra's Algorithm
Expand on the graph you wrote for lab to write an application that can calculate the fastest route between two points.

1. Begin by devising a data structure that can easily contain a graph with weighted edge, with two vertices and a integer representing the cost of travelling across that edge. There are a lot of ways to do this (e.g. edge lists, adjacency matrices, adjacency lists), and you should leverage one of the separate files in repl.it to store your test data. Pick something that feels relevant to you. For example, paths between your favorite places in Seattle:
```
("Queen Anne", "Capitol Hill", 3), ("SODO", "Bellevue", 10), ...
```

2. Using your graph class created above, implement the method ShortestPath() that returns the shortest path between two vertices. In order to calculate the shortest path between any two vertices on a map, you must first calculate the shortest path to all of the vertices. To accomplish this, you will need to store each vertex, the path used to get there, and the total cost of that path. Think critically about how you can determine when you can exclude a vertex from your search.

3. Write some tests to show your code in action. You can either use a testing framework like Pytest or NUnit or just test by writing methods that run your code and print results. Your tests should already know what the right answer is, and assert that your code gets that right answer.

Example: Console.WriteLine($"Shortest path between Queen Anne and Bellevue is length 19: {result == 19})


## Requirements

1. Data Structure
    1. weighted edge:= vertex1, vertex2, weight (cost of traversing)
    2. edge lists, adjacency matrices, adjacency lists
    3. Given vertex1, calculate the shortest path to all other vertices (memoization?)
    4. Define invariants when a vertex can be excluded from your search
    5. ShortestPath method should return shortest path between two vertices by using 1.3 and 1.4
2. Test data should be stored in it's own file


Note: This is a very open-ended assignment, and I will be grading it mostly on clarity, not just whether or works or not. Try your best to show your thinking.    


Submission can be via a zipped up project uploaded to Canvas, a link to a repl.it you create, or a link to a source control repository (GitHub, GitLab, BitBucket etc.)


# Test
To run the tests
```
python -m unittest discover
```
Optionally, type hints can be checked with `mypy`
```
python -m mypy graph.py
```
