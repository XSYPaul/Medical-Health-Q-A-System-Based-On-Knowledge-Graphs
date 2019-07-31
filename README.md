# Medical-Health-Q-A-System-Based-On-Knowledge-Graphs
### environment: python 3.6, MongoDB, Neo4j
### package: BeautifulSoup, requests, re, json, random, pandas, numpy, pymongo, py2neo, ahocorasick, pypinyin, functools, pkuseg, jieba, Django

## Process
*  Crawl data from web (The folder raw_data and code contain the raw data and the spyder code)
*  Preprocess raw data ( The folder cleaning data and code includes cleaning code and files that have been processed)
*  Build knowledge graph (After installing Neo4j database, you can run build_graph.py in knowledge graph folder and then several enetity dictionaries would output. After that, knowledge graph would be bulit successfully in a few minutes)
*  Build QA system ( The folder Q&A System contain files that rectify word typo, entity extraction, relationship extraction and main function. Running Main.py could build entire Q&A system.)

Note: if you want to execute the process by yourself, you need to pay attention the paths in these python file. Since these paths depend on my project, you need to modify according to your settings.
