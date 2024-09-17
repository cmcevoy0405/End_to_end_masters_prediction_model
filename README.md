<h1 align="center" style="color:#FFFFFF; font-family: 'Arial', sans-serif;">Masters Prediction Project ⛳</h1>

<p align="left" style="color:#FFFFFF; font-family: 'Verdana', sans-serif;">
  <b>Key Findings: It seems that players who finished well in the tournament played well from tee to green, with driving distance and accuracy showing high importance. On the other hand putting and around the green play seemed to effect masters performance the least. The end calssification model was able to predit the winner among a winners group corrrectly 86% of the time.  </b>
</p>

### Table of Contents
- [Introduction](#introduction)
- [Scraping](#scraping)
- [Model](#model)
- [Deployment](#deployment)
- [Issues](#issues)

### Introduction
I've always been interested in golf and what makes the best in the world the best. Combined with my interest in data and finding data backed solutions, i decided to create a model on who would win the Major golf tournament, the masters.  This involved the full data process from web scraping and model building through to deployment. The entire project was developed in python using flask application as the deployment method. 

### Scraping
The pga_scrape.py file showcases the data scraped from a python script. The file scrapes the last 15 years worth of pga data on players that competed in the 2024 masters tournament. 

