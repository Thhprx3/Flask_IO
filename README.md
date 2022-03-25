<p align="center">
  <a href="https://github.com/Thhprx3/Flask_IO/graphs/commit-activity" alt="Activity">
    <img src="https://img.shields.io/github/commit-activity/w/Thhprx3/Flask_IO?color=green&label=Commits&style=for-the-badge" /></a>
  <a href="https://github.com/Thhprx3/Flask_IO/graphs/commit-activity" alt="Update">
    <img src="https://img.shields.io/github/last-commit/Thhprx3/Flask_IO?style=for-the-badge" /></a>
  <a href="https://github.com/Thhprx3/Flask_IO/issues" alt="Issues">
    <img src="https://img.shields.io/github/issues/Thhprx3/Flask_IO?color=red&style=for-the-badge" /></a>
  <a href="https://github.com/Thhprx3/Flask_IO/blob/master/LICENSE.txt" alt="License">
    <img src="https://img.shields.io/github/license/Thhprx3/Flask_IO?color=green&style=for-the-badge" /></a>
</p>
  
<div align="center">
  <h3 align="center">Flask Project</h3>
  <p align="center">
    First steps in Flask framework!
  </p>
</div>

## About

The project is designed to visualize data extracted from crypto market

### Software

* [Flask](https://flask.palletsprojects.com/)
* [Python](https://www.python.org/)
* [Dash](https://dash.plotly.com/)
* [Bootstrap](https://getbootstrap.com)

## Prerequisites

In order to use following repository, at the moment you'll need to use any Linux distribution.
We'll be using pip as the main package manager toinstall all the dependencies required in the project we will use pip, 
which is a package management system for the Python language environment

* PIP
  ```sh
  sudo apt install python3-pip
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Thhprx3/Flask_IO.git
   ```
3. Create virtual env
   ```
   virtualenv venv
   ```
2. Install all necessary dependencies used in the project
   ```sh
   sudo pip install -r requirements.txt
3. Set environment variables for development
   ```sh
   export FLASK_ENV=development
   export FLASK_APP=server_start.py
   export FLASK_DEBUG=1
   ```
4. Start the development server
   ```js
   flask run
   ```

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## TODO

- [x] Basic template
- [x] Integrate Dash + Flask
- [ ] Static data collection
- [ ] Extend data collection
- [ ] Include options/sliders for charts
- [ ] First Gunicorn deployment on Heroku
- [ ] Data preparation for keras/tensorflow
- [ ] Building first AI model
- [ ] Implementing predictions
- [ ] tbd
