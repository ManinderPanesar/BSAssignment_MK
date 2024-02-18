# DSI UfT Building Software Project Assignment 

Through this project, I built a package that can be used to get all the repositories for a user (or an organization), create a list of all repositories with their creation date, summarise and plot the repositories over years. This assignment was a part of course on Building Robust Software delivered by UfT Data Science Institute. This course supported me in writing short programs in a reproducible way.

## Learning Outcomes
1. Create and read configuration files for programs, and know when to use them
2. Describe, use, and write Application Programming Interfaces
- Reading documentation, writing documentation
- Using HTTP-based APIs in Python
- Writing Python APIs
3. Know how to create bug reports and prioritize requests.
4. Proficiently test software, handle errors, and track provenance
5. Know how to create Python packages.

### Usage Example 

!pip install git+https://github.com/ManinderPanesar/BSAssignment_MK
from Analysis import Analysis

analysis_obj = Analysis('config.yml')
analysis_obj.load_data()

analysis_output = analysis_obj.compute_analysis()
print(analysis_output)

analysis_figure = analysis_obj.plot_data()

### Instructor 
Instructor: Simeon M Wong, MHSc(BME). simeonm.wong@mail.utoronto.ca
TA: Tong Su. tong.su@mail.utoronto.ca

