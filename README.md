# Medical-Health-Q-A-System-Based-On-Knowledge-Graphs
### environment: python 3.6, MongoDB, Neo4j
### package: BeautifulSoup, requests, re, json, random, pandas, numpy, pymongo, py2neo, ahocorasick, pypinyin, functools, pkuseg, jieba, Django

## Process
*  Crawl data from web (The folder raw_data and code contain the raw data and the spyder code)
*  Preprocess raw data ( The folder cleaning data and code includes cleaning code and files that have been processed)
*  Build knowledge graph (After installing Neo4j database, you can run build_graph.py in knowledge graph folder and then several enetity dictionaries would output. After that, knowledge graph would be bulit successfully in a few minutes)
*  Build QA system ( The folder Q&A System contain files that rectify word typo, entity extraction, relationship extraction and main function. Running Main.py could build entire Q&A system.)

Note: If you want to execute entire process by yourself, you need to pay attention the paths in these python file. Since these paths depend on my project, you need to modify according to your settings.

## Interactive Interface
*  If you want to use interactive interface, please run command python3 Main.py in console, and then run command python3 manage.py runserver 8000 in console. 
*  If the two commands run correctly, you could browse http://localhost:8000.

Note: If you encounter some problems, please check your paths first.
