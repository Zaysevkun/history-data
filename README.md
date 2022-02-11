# Hystory data console representation

## Run:
- git clone ```https://github.com/Zaysevkun/test-task-history-data.git```
- cd into script folder
- ```python main.py```
- input desired sample name, **without** folder name or file extension. If you just press enter, sample file defaults to "sample1"

## Design report:
Json structure seems a bit odd to me.I don't know all prerequisites to that design, but I think pass whole Order body in every history event is not optimal:
1. It adds a need to perform costly operations to just get what field where updated with update action
2. It's adds latency to sending that json via http
3. Frontend probably already has that information from Order GET endpoints

## Output example:
![example](https://github.com/Zaysevkun/test-task-history-data/blob/master/output_example.png)
