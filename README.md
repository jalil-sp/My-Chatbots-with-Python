
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Chatbot Project README. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now let's dive into the Chatbot Project! :D
-->

<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![LinkedIn][linkedin-shield]][linkedin-url]


<h3 align="center">Chatbots with Python</h3>

  <p align="center">
    A collection of Chatbots demonstrating various conversational AI-like techniques.
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#context">Context</a></li>
        <li><a href="#skills-practiced">Skills Practiced</a></li>
      </ul>
    </li>
    <li>
      <a href="#projects">Projects</a>
      <ul>
        <li><a href="#reverse-echo-bot">Reverse Echo Bot</a></li>
        <li><a href="#yoda-match-bot">Yoda Match Bot</a></li>
        <li><a href="#inspiration-bot">Inspiration Bot</a></li>
        <li><a href="#push-bot">Push Bot</a></li>
        <li><a href="#word-reduction-bot">Word Reduction Bot</a></li>
        <li><a href="#my-reduction-tfidf-bot">My Reduction TF-IDF Bot</a></li>
        <li><a href="#ads-reduction-tfidf-bot">ADS Reduction TF-IDF Bot</a></li>
        <li><a href="#emoji-menu-card">Emoji Menu Card</a></li>
      </ul>
    </li>
    <li><a href="#things-to-do-differently">Things to Do Differently</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Welcome to my Chatbots with Python Project! This repository contains a collection of chatbots that demonstrate various conversational AI techniques. Each bot serves a different purpose and showcases unique capabilities.

### Context

Chatbots are a conversational interface to various applications such as triggering activities, automated responses, mechanized functions, increased speed, virtual helpdesk assistants and cost reduction. Chatbots may take advantage of callable services that provide Artificial Intelligence-like functions, but Chatbots by themselves are not a form of Artificial Intelligence.

I used RHO and MS Teams to set up my chatbots. Specifically, I imported a Q Chatbot into MS Teams with RHO, then I created and registered my bot. Next, I updated the .env file with the new ID, secret key, and port. Afterwards, I needed to enter my chatbot ID and new URL to configure the chatbot with MS Teams.

Additionally, for this project, I utilized the Bottle web framework to enhance the functionality and interaction of these chatbots.

### Skills Practiced

- Performing automation via ChatBot
- Using the ChatBot SDK
- Using a Word Reduction Engine
- Reading ChatBot information from a Web page
- Adaptive Cards with ChatBot

<!-- PROJECTS -->
## Projects

### Reverse Echo Bot

- Description: Create a bot that reverses received messages in some form (reverse letters, reverse word order, etc.).
- File: ReverseEchoBot.py

### Yoda Match Bot

- Description: Create a word match program that solves a specific problem, such as a directory of relevant websites or phone numbers based on user input.
- File: YodaMatchBot.py

### Inspiration Bot

- Description: Create a bot that responds with random quotes, jokes, inspirational messages, or suggested songs.
- File: InspirationBot.py

### Push Bot

- Description: Create a bot that sends messages to a specific user, useful for reminders or notifications.
- File: PushBot.py

### Word Reduction Bot

- Description: Create a bot that performs word reduction, removes stop words, and responds to similar requests with reduced words.
- File: WordReductionBot.py

### My Reduction TF-IDF Bot

- Description: Expand on the Word Reduction Bot by creating a custom preprocessor function using reductions and performing TF-IDF and cosine similarity to find the best response.
- File: MyReductionTFIDFBot.py

### ADS Reduction TF-IDF Bot

- Description: Similar to the My Reduction TF-IDF Bot, but the knowledgebase can be from a file or a local Wiki page.
- File: ADSReductionTFIDFBot.py

### Emoji Menu Card

- Description: Incorporate all elements from previous projects and demonstrate how they can improve the user experience, including the use of emojis, user and office information, and interactive menus.
- File: EmojiMenuCard.py

<!-- THINGS TO DO DIFFERENTLY -->
## Things to Do Differently

In the context of my chatbots, RHO acts as an intermediary between the chatbot's user interface and the backend APIs or data sources that the chatbot relies on to provide relevant responses. By implementing a lightweight Q client, the chatbot can consume minimal resources while still delivering a seamless and efficient user experience.

Going forward I would want to implement the concepts I learned from building chatbots that interface with MS Teams towards my own personal chatbot for a larger solo project. Overall I really enjoyed the knowledge I gained and plan to explore more.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/jalil-spearman/

