---
title: "Visualising the Intersection of Disease and the Human Genome"
date: 2021-02-22
updated: 2021-02-22
author: "Joshua Magiera"
contact: "https://www.linkedin.com/in/joshua-magiera-55b362174/"
tags:
- visualization
- interactive
- shiny
categories:
- [Natural Sciences, Chemistry]
languages:
- r
description: "Since the Human Genome Project completed its survey of Homo sapian genes in 2003, we have had access to an incredibly powerful dataset for understanding disease and discovering new diseases. In this post, we demonstrate an interactive web app visualising such data."
cover: /banners/genome-visualisation.jpg
---
{% note success %}
**Try it for Yourself**
This article is the write-up for an interactive web application, allowing you to visualise CpG islands and SnP sites for different diseases. You can acces the app [here](https://cloud.wdss.io/genome) to test it on diseases of your choosing.
{% endnote %}
## Introduction

Beginning in the early '90s, the Human Genome Project (HGP) was an international research collaboration that attempted to sequence and map all of the genes for Homo sapiens. The HGP was completed in 2003 and paved way for significant developments to be made in drug discovery.  

In 2000, the University of California Santa Cruz (UCSC) and collaborators of the HGP started work on creating a free public access human genome assembly. To this day, it remains open access and has many features which can be used to relate information from the human genome to disease. 

It was found that single nucleotide polymorphisms (SnPs) and CpG islands are commonly located around diseases. An SnP is the most common type of genetic variation between people. They occur, on average, once in every 1000 nucleotides (roughly 4 million SnPs in total). As an example, an SnP may replace the nucleotide cytosine (C) with the nucleotide thymine (T) in a certain stretch of DNA. CpG islands are important because they represent areas of the genome that have, for some reason, been protected from the mutating properties of methylation through evolutionary time (which tends to change the G in CpG pairs to an A). Often, they point to the presence of an important piece of intergenic DNA, such as that found in the promoter regions of genes where transcription factors bind. In cancers, loss of expression of genes occurs about 10 times more frequently by hypermethylation of promoter CpG islands than by mutations. 

## Building a Visualisation

The National Center for Biotechnology Information (NCBI) contains information on where many diseases can be found within the human genome. These positions were collated onto a spreadsheet, along with a link to more information on the relevant disease.
![Spreadsheet of Diseases](/images/genome-visualisation/diseases_spreadsheet.png)
From the locations of the diseases obtained from the NCBI, information on SnP sites and CpG islands was collected using the API on the UCSC genome browser using the SnP and CpG island tracks.

![UCSC Genome Browser](/images/genome-visualisation/UCSC_genome_browser.png)

GViz, a Bioconductor package for R, was used to then display the genome location, producing a visual representation graphically of the SnP sites and CpG islands.
![Visualisation of Disease](/images/genome-visualisation/disease_visualisation.png)
The lines on the SnP track show sites that have a minor allele frequency of at least 1% and are mapped to a single location in the reference genome assembly. The highlighted areas on the CpG island are where there is a GC content of higher than 50% for greater than 200bp. The red line on the chromosome highlights the area in which the disease is located, and what is able to be viewed on the tracks is data within the highlighted region. 

One significant challenge faced was that, due to the vast amount of data needed to produce the genome plots, once a disease had been selected, it took a considerable amount of time for the API to collect the data. This meant it was less than ideal due to users not wanting to wait a lengthy period of time. The way this was overcome was by pre-generating the plots for each disease in the spread sheet, meaning that the plots were shown instantaneously.  

Future improvements to the programme could include but not limited to caching the data collected rather than having pre-generated plots. This would work well with another improvement which was considered whereby the disease spreadsheet was connected to the NCBI database which contained every single disease known with the possibility of more disease identification as well. This would mean the programme could keep up-to date with new diseases entering the database and would not need manually updating. 
