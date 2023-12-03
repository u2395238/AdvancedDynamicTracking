<div align="center">

# Vehicle Counting program; developed from AdvancedDynamictracking

</div>

<div align="center">

[![Status](https://img.shields.io/badge/status-active-success.svg)]()
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](/LICENSE)

</div>

<div align="center">
<img src="assets/output.gif" width="1000px" height="600px">
</div>



### On CPU - `12 to 15 FPS` 

## Pre-requisites : 

1) Clone the Repository [AdvancedDynamicTracking](https://github.com/u2395238/AdvancedDynamicTracking)

```bash
git clone https://github.com/u2395238/AdvancedDynamicTracking.git

cd AdvancedDynamicTracking
```

2) Clone the legacy Yolo-v5 Repository

```bash
git clone https://github.com/ultralytics/yolov5.git
```
3) Start python virtual environment

```bash
python -m venv tracking
```

4) Activate the virtual environment

```bash
source tracking/bin/activate
```

6) Install the libraries
```bash
pip install -r requirements.txt
```




## Directory Structure :

After completing the above steps your directory should look like somewhat as of below structure

- `AdvancedDynamicTracking`
   - deep_sort
   - yolov5
   - input.mp4
   - yolov5s.pt
   - tracker.py
   - requirements.txt

## Run the algorithm 

``` bash
python tracker.py 
# This will download model weight - yolov5s.pt to base folder on first execution.
```

#### Feel free to [conect with me](https://www.linkedin.com/in/shalumalik/)...
