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
  <h3 align="center">Dashboard with Python Dash</h3>
  <p align="center">
    Simple cryptocurrency dashboard created using the Dash framework
  </p>
</div>

## About

The project is designed to visualize data extracted from [CoinMarketCap](https://coinmarketcap.com/)

### Software

* [Dash](https://dash.plotly.com/)
* [Python](https://www.python.org/)
* [Bootstrap](https://getbootstrap.com)

## Prerequisites

In order to use following repository, at the moment you'll need to use any Linux distribution.
We'll be using pip as the main package manager toinstall all the dependencies required in the project we will use pip, 
which is a package management system for the Python language environment

1. Windows
  * PIP
    ```
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
    ```
  * Virtualenv
    ```
    pip install virtualenv 
    ```
  
2. Linux  
  * PIP
    ```sh
    sudo apt-get install python3-pip
    ```
  * Virtualenv
    ```
    sudo pip install virtualenv 
    ```

### Installation
## Windows
1. Clone the repo
   ```sh
   git clone https://github.com/Thhprx3/Flask_IO.git
   ```
3. Create virtual env
   ```sh
   python3 -m venv .venv
   source venv/bin/activate
   ```
2. Install all necessary dependencies used in the project
   ```sh
   sudo pip install -r requirements.txt
4. Start the development server
   * Locally
   ```sh
   python3 start_server.py
   ```
   * Gunicorn
   ```sh
   pip install gunicorn
   ```
---
## Linux
1. Clone the repo
   ```sh
   git clone https://github.com/Thhprx3/Flask_IO.git
   ```
3. Create virtual env
   ```sh
   python3 -m venv .venv
   source venv/bin/activate
   ```
2. Install all necessary dependencies used in the project
   ```sh
   sudo pip install -r requirements.txt
   ```
4. Start the development server
   * Locally
   ```sh
   python3 start_server.py
   ```
   * Gunicorn
   ```sh
   pip install gunicorn
   gunicorn start_server:app.server
   ```

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

## TODO

- [x] Page template
- [x] Integrate Dash
- [x] Static data collection
- [x] Extend data collection
- [x] Include options/sliders for charts
- [x] First Gunicorn deployment on Heroku
- [ ] Data preparation for keras/tensorflow
- [ ] Building first AI model
- [ ] Implementing predictions
- [ ] tbd
