<!-- Back to Top Navigation Anchor -->
<a name="readme-top"></a>

<!-- Project Shields -->
<div align="center">

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  [![Twitter][twitter-shield]][twitter-url]
</div>

<!-- Project Logo -->
<br />
<div align="center">
  <a href="https://lne-5e10a4711a60.herokuapp.com">
    <img src="https://github.com/Oluwatemmy/Link-Ease/blob/main/link_ease/static/image/linkease.png" alt="Logo" width="50%" height="30%">
  </a>
</div>

<br />

<div>
  <p align="center">
    <a href="https://github.com/Oluwatemmy/Link-Ease/blob/main/README.md"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="#sample">View Demo</a>
    ·
    <a href="https://github.com/Oluwatemmy/Link-Ease/issues">Report Bug</a>
    ·
    <a href="https://github.com/Oluwatemmy/Link-Ease/issues">Request Feature</a>
  </p>
</div>

---

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-link-ease">About Link-Ease</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#lessons-learnt">Lessons Learnt</a>
    </li>
    <li>
      <a href="#key-features">Key Features</a>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#live-link">Live Link</a></li>
        <li>
          <a href="#localhost">Localhost</a>
          <ul>
            <li><a href="#prerequisites">Prerequisites</a></li>
            <li><a href="#installation">Installation</a></li>
          </ul>
        </li>
      </ul>
    </li>    
    <li><a href="#sample">Sample</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
  <p align="right"><a href="#readme-top">back to top</a></p>
</details>

---

<!-- About the Tool -->
## About Link-Ease

Link-Ease is a powerful URL shortening tool designed to make sharing links easier and more convenient in today's fast-paced world of social media. With Link-Ease, you can transform long, unwieldy URLs into concise, memorable links and generate QR codes for quick mobile access. 

Our intuitive interface, customizable links, and detailed analytics provide a seamless user experience, making it the perfect tool for marketers, content creators, and anyone looking to share links efficiently. Join Scissor today and experience the power of concise, shareable links.

Live Site: [link-ease](https://lne-5e10a4711a60.herokuapp.com)

Full Documentation: [Readme](https://github.com/Oluwatemmy/Link-Ease/blob/main/README.md)

<p align="right"><a href="#readme-top">back to top</a></p>

### Built With:

![Python][python]
![Flask][flask]
![Jinja][jinja]
![HTML5][html5]
![CSS3][css3]
![SQLite][sqlite]
![BOOTSTRAP][bootstrap]
![Bulma][bulma]
![GIT][git]
![Heroku][heroku]
![VISUAL STUDIO CODE][vscode]
![CHATGPT][chatgpt]

<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- Lessons from the Project -->
## Lessons Learnt

Creating this tool helped to learn and practice:
* Responsive Web Design
* URL Shortening
* QR Code Generation
* Debugging
* Routing
* Database Management
* Internet Security
* User Authentication and Authorization
* Message Flashing
* Documentation

<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- Lessons from the Project -->
## Key Features:

* URL Shortening: The app allows users to shorten long URLs into concise and shareable links.

* Customizable Link: Users have the option to customize the shortened URLs to reflect their brand or preferred keywords, making them more recognizable and memorable.

* Link Analytics: The app provides insightful analytics on the link usage,  including the number of clicks.

* QR Code Generation: The app generates QR codes for each shortened link, making it easy for users to share links through QR code scanning or mobile devices.

* Link History: Users will have access to a comprehensive history of their shortened URLs, including creation dates, original URLs, and usage statistics, and option to edit their custom urls, and manage their shortened URLs.

* Secure and Scalable: The application will prioritize data security, implement proper authentication mechanisms, and ensure scalability to handle a large volume of requests.

* User Management: The system will provide user registration and authentication functionalities, allowing users to manage their shortened URLs and access personalized features.

* Cache System: A caching mechanism is implemented to optimize performance and reduce load times for frequently accessed links.

* Error Handling: The app includes robust error handling to handle invalid or non-existent URLs, ensuring a smooth user experience.

* Responsive Design: The app is designed to be responsive and accessible on different devices, including desktops, tablets, and mobile devices.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Getting Started -->
## Usage

This tool can be accessed via the deployed site or you can run it locally on your computer.

### Live Link

Deployed site: [link-ease](https://lne-5e10a4711a60.herokuapp.com) - hosted via [heroku](https://www.heroku.com) 

### Localhost

To run the application locally on your computer, follow the steps below.

#### Prerequisites

Python3: [Get Python](https://www.python.org/downloads/)

#### Installation

1. Clone this repo
   ```sh
   git clone https://github.com/Oluwatemmy/Link-Ease.git
   ```
2. Create Virtual Environment
   ```sh
   python -m venv <your-venv-name>
   ```
3. Activate virtual environment on CMD or Powershell
   ```sh
   <your-venv-name>\Scripts\activate
   ```
On gitbash terminal
    ```sh
    source <your-venv-name>/Scripts/activate
    ```
4. Install project packages
   ```sh
   pip install -r requirements.txt
   ```
5. Set environment variable
    ```sh
    set FLASK_APP=main.py
    ```
On gitbash terminal
    ```sh
    export FLASK_APP=main.py
    ```
6. Create Database
    ```sh
    flask shell
    ```
    ```sh
    db
    ```
    ```sh
    db.create_all()
    ```
    ```sh
    exit()
    ```
7. Run the app
    ```sh
    flask run
    ```
8. Open the app on your browser
    

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Sample Screenshot -->
## Sample

<br />

[![Link-Ease Screenshot][linkease-screenshot]](https://github.com/Oluwatemmy/Link-Ease/blob/main/link_ease/static/image/linkease_homepage.png)

<br/>

---


<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/Oluwatemmy/Link-Ease/blob/main/LICENSE">LICENSE</a> for more information.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Contact -->
## Contact

Ajayi Oluwaseyi - [@Oluwatemmy15](https://twitter.com/Oluwatemmy15) - oluwaseyitemitope456@gmail.com

Live Site: [sciz.site](https://www.sciz.site)

Project Link: [Link-Ease Repo](https://github.com/Oluwatemmy/Link-Ease)

Documentation: [Link-Ease Wiki](https://github.com/Oluwatemmy/Link-Ease/blob/main/README.md)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Acknowledgements -->
## Acknowledgements

This project was made possible by:

* [AltSchool Africa School of Engineering](https://altschoolafrica.com/schools/engineering)
* [Caleb Emelike's Flask Lessons](https://github.com/CalebEmelike)
* [GitHub Student Pack](https://education.github.com/globalcampus/student)
* [Heroku](https://www.heroku.com/)
* [Othneil Drew's README Template](https://github.com/othneildrew/Best-README-Template)
* [Ileriayo's Markdown Badges](https://github.com/Ileriayo/markdown-badges)
* [Stack Overflow](https://stackoverflow.com/)
* [Font Awesome](https://fontawesome.com/)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Markdown Links & Images -->
[contributors-shield]: https://img.shields.io/github/contributors/Oluwatemmy/Link-Ease.svg?style=for-the-badge
[contributors-url]: https://github.com/Oluwatemmy/Link-Ease/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Oluwatemmy/Link-Ease.svg?style=for-the-badge
[forks-url]: https://github.com/Oluwatemmy/Link-Ease/network/members
[stars-shield]: https://img.shields.io/github/stars/Oluwatemmy/Link-Ease.svg?style=for-the-badge
[stars-url]: https://github.com/Oluwatemmy/Link-Ease/stargazers
[issues-shield]: https://img.shields.io/github/issues/Oluwatemmy/Link-Ease.svg?style=for-the-badge
[issues-url]: https://github.com/Oluwatemmy/Link-Ease/issues
[license-shield]: https://img.shields.io/github/license/Oluwatemmy/Link-Ease.svg?style=for-the-badge
[license-url]: https://github.com/Oluwatemmy/Link-Ease/blob/main/LICENSE.txt
[twitter-shield]: https://img.shields.io/badge/-@Oluwatemmy15-1ca0f1?style=for-the-badge&logo=twitter&logoColor=white&link=https://twitter.com/Oluwatemmy15
[twitter-url]: https://twitter.com/Oluwatemmy15
[linkease-screenshot]: website/static/screenshots/scissor.png
[dashboard-screenshot]: website/static/screenshots/dashboard.png
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[jinja]: https://img.shields.io/badge/jinja-white.svg?style=for-the-badge&logo=jinja&logoColor=black
[html5]: https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white
[css3]: https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
[bootstrap]: https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white
[git]: https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white
[bulma]: https://img.shields.io/badge/bulma-00D0B1?style=for-the-badge&logo=bulma&logoColor=white
[heroku]: https://img.shields.io/badge/heroku-%23430098.svg?style=for-the-badge&logo=heroku&logoColor=white
[chatgpt]: https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white
[vscode]: https://img.shields.io/badge/Visual%20Studio%20Code-0078d7.svg?style=for-the-badge&logo=visual-studio-code&logoColor=white
