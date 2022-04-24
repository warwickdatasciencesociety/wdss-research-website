---
title: "Grouping Parliamentary Constituencies using Clustering Analysis"
date: 2022-04-05
updated: 2022-04-05
authors_plus:
- "Areeb Shafqat"
contacts_plus:
- "https://www.linkedin.com/in/areebshafqat297/"
editor: "Fernando A. Zepeda Herrera"
editor_contact: "https://www.linkedin.com/in/fernando-antonio-zepeda-herrera/"
tags:
- clustering
- politics
- visualization
categories:
- [Social Sciences, Politics]
languages:
- python
description: "Do the London, Scotland, or the Red Wall parliamentary constituencies form cohesive groups? We explore using different choices of clustering techniques."
cover: /banners/voting.png
---
# Introduction

The UK constituencies are the key determinant of the general election outcome due to the “First Past the Post” System, which mainly leads to the Conservative or Labour parties winning majority of the constituency seats and forming a government. Thus, by analyzing numerous characteristics of these constituencies like past voting behaviour or demographic data such as population density, one can employ clustering algorithms to group them into clusters with similar features. There may be several reasons to do this. For example, clustering may help explain general trends or patterns, provide a broad view of differences between constituencies, or even based on the analysis, political parties may attempt to adapt their campaign efforts to the set of constituencies prone to switch their voting behaviour in their favour.

One example of this is an appealing [data science blog post by Ballard (2019)](https://www.cb91.io/projects/election) with its [associated GitHub repository](https://github.com/calbal91/project-understanding-elections) where the author: collects several types of constituency data from the UK parliament website; carries out feature engineering and scaling steps; implements a Hierarchical Agglomerative Clustering (HAC) algorithm to underline any anomalous voting behaviour from constituencies; and finally utilises the 2017 election data to predict the voting choices of each constituency in the 2019 general election. Although we can augment that analysis in several ways, our current project will dive deeper into investigating alternatives to HAC and search which clustering algorithms and metrics provide us with the best clusterings concerning the UK political datasets, which can be of benefit to political researchers and parties. Furthermore, we believe it is advantageous to provide an example analysis project that highlights the different degrees of freedom researchers have when performing clustering analysis and the effects those choices have on the results.

Therefore, we will explore alternatives with the following Clustering workflow:

1. **Feature Engineering and Selection**

    The first key ingredient of any clustering analysis is the data upon which it is based. In this section, we will discuss some of the variables involved in our analysis and explore the (possible) effects of including or excluding them.

2. **Dimensionality Reduction**

    In certain contexts, it is vital to conduct dimensionality reduction before attempting clustering, especially for distance-based algorithms like K Means. Here we explore two possible methods: PCA (linear) and UMAP (non-linear).

3. **Clustering Model**

    The main component of a clustering analysis is the model or algorithm selection. Besides HAC, we will consider K-means, Gaussian Mixture Modelling (GMM) and DBScan.

4. **Optimality Criteria/Metric**

    Depending on the algorithm chosen, we require particular metrics that can assist in selecting the optimal number of clusters where different criteria may lead to varying results. Here we will review metrics such as Distortion, Silhouette Score, Calinski-Harabasz, and the Davies-Bouldin index. In addition, some criteria are method-specific, like Dendrograms for HAC or the Bayesian Information Criterion (BIC) for GMM.

Once the hyperparameters have been optimized for each model, we will further inspect the generated segments, compare them across various algorithms and select the one that offers the most insightful and logical clusters.

All the code for this project can be found in [this GitHub repository](https://github.com/Areeb297/Warwick-Data-Science-Research-Project) which reuses some helpful code snippets from Ballard.


# Data pre-processing and Feature Engineering

To advance the work of Ballard, we use the same 2019 UK parliament constituency and the 2011 UK census data where the key variables include the wages per constituency, median house prices, unemployment changes in the past decade, house ownership type proportions, percentage of ethnicities, religious and age groups, broadband speeds and many more. One central  differentiation of our project, however, is that we chose to remove the regions variable to have no geographical influence on the clusters generated to detect more interesting clustering behaviour. Furthermore, we reduce the  categories of age, religion, and ethnicity to lower the dimensionality of our data. Moreover, to exclusively keep numerical variables for our clustering analysis, we remove the 2017 voting results categories per constituency where instead, we use directly the percentage of Conservative, Labour, Liberal, and SNP voters per constituency from the 2017 election. Including and excluding the SNP voter percentage will make up a major part of our clustering analysis later on. Additionally, we exclude the UKIP party vote due to the already existing EU referendum outcome present in the data. Lastly, we apply some log transformations to reduce skewness and “outlier influence” on the following variables: population density, area, number of businesses, wages, and house prices. The full considered dataset has 631 rows and 56 columns.

# Dimensionality Reduction Methods

Progressing ahead to feature reduction, this is crucial due to the curse of dimensionality hindrance since clustering methods rely mainly on distance metrics to quantify the similarity between observations. Consequently, excessive dimensionality will result in every data point being seemingly equidistant to one another, i.e., overfitting the data [(Yiu, 2019a)](https://towardsdatascience.com/the-curse-of-dimensionality-50dc6e49aa1e). Therefore, by exploiting methods like UMAP and PCA, one can be restricted to the pertinent variables whilst also getting rid of multicollinearity and existent noise from the dataset.

Regarding PCA, it is perhaps the most widely known method of dimensionality reduction. It transforms the data into a smaller orthogonal components that contain the primary underlying trends of the data [(Yiu, 2019b)](https://towardsdatascience.com/understanding-pca-fae3e243731d). Another prominent and state-of-the-art non-linear transformation used for data visualisation usually, is Uniform Manifold Approximation and Projection, i.e., UMAP, which computes and evaluates the similarity scores between highly dimensional data points using an exponential probability distribution [(Allaoui et al., 2020)](https://link.springer.com/chapter/10.1007/978-3-030-51935-3_34). It is scalable with outstanding run-time performance as it exploits the stochastic gradient descent method whilst preserving the approximate vicinities between similar data points, thus retaining most of the global/macro data structure. As a result, it can be used generally in any machine learning problem for dimensionality reduction ([McInnes et al., 2018](https://arxiv.org/abs/1802.03426); [Spacagna, 2021](https://towardsdatascience.com/manifold-clustering-in-the-embedding-space-using-umap-and-gmm-dbab26a9efba)). Hence, using both linear PCA and manifold learning can enable us to explore any disparity in the clusters generated and to determine whether one method is superior over the other based on the clusters.



![](/images/political-clustering/political-clustering_11_0.png)


Concerning the number of selected components, we aim to retain 90% of the variance explained with PCA; this leads to 16 features. As for UMAP, we will pick the same number as PCA for a fair comparison of dimensionality. In addition, we add a random state to both these algorithms for reproducibility purposes.

## A quick overview of considered Algorithms and Metrics

### K-Means

The popular K-Means algorithm starts by allocating k randomly placed centroids to the dataset and assigning points to the nearest centroid. Then it iteratively relocates the centroids to the mean of the assigned points and reassigns them based on the distance to the new centroids, leading to a reduction of the within-cluster sum of squares until convergence is reached. Some drawbacks of this method are that different initial starting points of centroids leads to different clustering results and the user is required to pre-specify the desired number of clusters
[(Garbade 2018)](https://towardsdatascience.com/understanding-k-means-clustering-in-machine-learning-6a6e67336aa1).

### HAC

This commonly used technique exploits a distance metric to allocate clusters using a bottom-up clustering approach. It iteratively identifies pairs of points with minimal distance as clusters and successfully merges those pairs with the closest clusters [(Dobilas, 2021)](https://towardsdatascience.com/hac-hierarchical-agglomerative-clustering-is-it-better-than-k-means-4ff6f459e390). This leads to a hierarchy of clusters and subclusters within those, until each point is its own cluster. This method thus provides the added advantage of enabling us to visualize dendrograms, gain insight as to when and how the segmentation of a given cluster occurred, and select the clusterings that appear to be the most distinct.

### DBSCAN

The method of DBSCAN is *density based* meaning that it attempts to locate regions of high density by classifying data points as either core, reachable or outlier points. One advantage this algorithm brings is that it generates the number of clusters instead of requiring it as a hyperparameter input. However, an essential thing to point out is that UMAP does not preserve the density of the original data [(Taylor, 2019)](http://localhost:8889/notebooks/OneDrive/Documents/Super%20important%20documents/Warwick%20Data%20Science%20Research%20Project/Clustering%20Algorithms/Blog_Clustering_Template.ipynb). Hence, we expect DBSCAN to produce disparate results when working with PCA to when using UMAP. Additionally, not maintaining density is acceptable as we are searching for unique clusterings that can help us spot any specific or general trends. To create the best segments, the key hyperparameters we experiment with include; the minimum number of points for defining a cluster (min sample points); the in-sample distance for a point to be considered as part of a cluster (epsilon); and lastly, the algorithm to locate the nearest neighbours (ball_tree, kd_tree, brute, auto). DBSCAN effectively picks up high density, noise, and outlier patterns in the data however, it can be challenging to find the ideal cluster number [(Yildirim, 2020)](http://localhost:8889/notebooks/OneDrive/Documents/Super%20important%20documents/Warwick%20Data%20Science%20Research%20Project/Clustering%20Algorithms/Blog_Clustering_Template.ipynb).

### GMM

The last clustering method left to discuss, GMM, involves working with varying Gaussian distributions (a distribution-based model unlike K-Means or HAC which are distance based) that are used to assign probabilities (soft assignment/clustering) to each data point. These probabilities indicate which distributions would have likely generated a specific point. On the other hand, K-Means, HAC or DBSCAN are hard clustering methods which allocate a data point to only one cluster [(Foley, 2019)](https://towardsdatascience.com/gaussian-mixture-modelling-gmm-833c88587c7f#:~:text=At%20its%20simplest%2C%20GMM%20is,means%2C%20we%20have%20soft%20assignments). Hence, each cluster will consist of data points from a unique Gaussian distribution where the uncertainties of those points belonging to other clusters are also encapsulated. Thus, this method mostly avoids biases for specific clustering types and is valuable for non-linear and higher-dimensional data. Concerning the hyperparameters to be optimized, we select: the number of components or clusters similar to K-Means or HAC and the covariance matrix types of the clusters. The choices for the covariance matrices include full (clusters take arbitrary shape or position), tied (clusters have identical shapes), diagonal (contour shapes directed towards the coordinate axes with varying eccentricities of the ellipticals), and finally spherical (circular diagonal contours).

### Tuning Criteria

Regardless of which algorithm is employed, we require hyperparameter tuning for instance, finding the best cluster number in K-Means. We find numerous metrics available as tuning criteria. Starting with the Silhouette Score, it measures the inter-cluster separation where a value close to 1 indicates a greater distance between samples of one cluster to neighbouring cluster data points, which is ideal. Moving onto the Calinski-Harabasz Index or the Variance Ratio Criterion, it calculates the ratio between the dispersion of points within distinct clusters and the variability of observations in clusters. Thus, a higher index would be more valuable as the between-cluster variability ought to be low for superior segmentation, resulting in distant and compact clusters [(Baruah, 2020)](https://towardsdatascience.com/cheat-sheet-to-implementing-7-methods-for-selecting-optimal-number-of-clusters-in-python-898241e1d6ad). Next we have the Davies Bouldin Index which computes the average of similarity scores between a cluster and its most identical cluster. The similarity score involves calculating the ratio of intra-cluster distances to inter-cluster distances where a low result is ideal, unlike the previous metrics. The reason is trivial, as having denser clusters far away from neighbouring clusters produces the best segmentation [(Zuccarelli, 2021)](https://towardsdatascience.com/performance-metrics-in-machine-learning-part-3-clustering-d69550662dc6#:~:text=The%20Davies%2DBouldin%20Index%20is,lead%20to%20a%20better%20score). Lastly, concerning BIC, it locates the hyperparameters that result in the least number of parameters being used that still explain the data reasonably when running the GMM model. Thus, the higher the BIC score is, the more parameters need to be introduced to cluster the data. The ultimate aim would be to minimise this metric based on the Occam’s razor principle [(Klassen, 2020)](https://towardsdatascience.com/an-intuitive-explanation-of-the-bayesian-information-criterion-71a7a3d3a5c5). As GMM implements the expectation maximization (EM) algorithm and the maximum likelihood estimation framework, we can use the BIC score as an evaluation metric in this case.

# Model Results

Collectively, we could fit 60 models by combining all the metrics and algorithms where depending on the various decisions we could compare results obtained just altering the algorithm, or the choice of dimensionality reduction. To facilitate this exploration, we developed a function in Python which allows us to easily fit and visualise the results for all of the choices just through changing the corresponding arguments. Below is an example output for UMAP with the Distortion metric, HAC algorithm and 6 clusters.


```python
## Available Clusering Methods: HAC, KMeans, DBScan, GMM, MS
## Available Metrics: Distortion, Silhouette, Calinski, Davies Bouldin

WDSS_clustering(
    data=df_con, 
    dim_reduction='UMAP', 
    clustering_method='HAC',
    map_plot=True, 
    metric_visuals=True, 
    cluster_bar=True, 
    heatmap=True, 
    dendrogram=False, 
    snp_included=True
)
```

We also present a  table with recommended number of clusters for each model permutation: 

<iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plotly.com/~Kaasiak/12.embed" height="525" width="100%"></iframe>

We have visualized all the 60 possible results using R to spot general trends and augment our understandability of all model outcomes:

- Majority of the models, except for a few permutations with DBSCAN, show one particular cluster being mainly composed of London constituencies. 
- UMAP datasets tend to suggest a higher number of clusters than PCA.
- UMAP leans toward assigning the London region to its own cluster, whereas PCA connects other big city constituencies to the London cluster. 

![](/images/political-clustering/All_Maps.png)

Before we proceed to investigate the different algorithms' results in more detail for political campaigns and insight, we assume a suitable cluster number would lie in the range of 4 – 10 approximately to effectively analyse and target anomalously behaving constituencies present in each cluster. With this in mind, we can now start searching for the best clustering solutions.


## K-Means


Firstly, looking at K Means with PCA, both the Calinski and Silhouette metrics lead to selecting 2 clusters as the optimal clustering. One cluster consists of mainly London constituencies alongside a few other city constituencies towards the North and West directions like Bradford or Birmingham or even in Scotland. The second cluster comprises the rest of the constituencies. We get this result irrespective of whether we include the % of SNP votes or not. We can see an example of this clustering with PCA in the first panel of the following figure:


![](/images/political-clustering/KMeans_Examples.png)


UMAP models generally assign Scotland (apart from some constituencies in Edinburgh or Glasgow) to its own cluster. This result occurs with or without incorporating the "Scottish identifying variable," the % of SNP votes. On the contrary, PCA models do not usually detect Scotland as its own cluster. An example of this behaviour was shown in the previous figure. Additionally, this time, the Calinski and Silhouette metrics produce slightly different clusterings with UMAP when we include or exclude the % of SNP voters. Perchance, the reason is UMAP detects non-linearities and subtleties better than PCA.

The Distortion and Davies Bouldin result in a higher and more appropriate number of clusters than the Calinski and Silhouette Indexes. Thus, these are the metrics to choose when working with this algorithm.


## HAC 

Progressing ahead to HAC, this technique outputs similar results to K-Means under PCA, except that the K-Means clusterings appear to be more compact with a higher number of clusters. Additionally, the SNP voter feature makes a difference for some city constituencies in Scotland. For example, they stop being part of the London cluster when we include the % of SNP votes, the metric being the Silhouette or Calinski Index. Apart from that, there were no significant differences between the PCA HAC and K-Means permutations. 

On the other hand, UMAP HAC offers more diverse clusterings. In fact, we obtained one of the highest cluster numbers compared with all the 60 models with HAC when the model sequence is UMAP without SNP votes, with the metric or criteria being the Calinski score. Furthermore, HAC tends to narrow better the distinction between the inner London constituencies and their surrounding clusters than K-Means. Hence, when working with UMAP, one would pick HAC over K-Means due to the more logical and superior segmentation obtained. Finally, even when the recommended clusters are 12, HAC outputs structured and reasonable clusters based on the demographics of the UK constituencies.  

As mentioned before, one attractive feature of HAC is its hierarchical nature. Even if any metric like Silhouette recommends a specific cluster number, one can still inspect the relationship between the recommended cluster number combinations by visualizing how they merge on a dendrogram. For instance, in the following figure, we see an animation of how HAC aggregates clusters when using the PCA with the SNP voters dataset:

![](/images/political-clustering/pca_snp_true.gif)

![](/images/political-clustering/Dendogram_PCA_SNP_true_reduced.png)

If instead, we pick the UMAP without the %SNP votes dataset, the results divert to the following:

![](/images/political-clustering/umap_snp_false.gif)

![](/images/political-clustering/Dendogram_UMAP_SNP_False_reduced.png)

The distortion metric appears to be the most stable metric as we get the same 6 or 7 recommended segments.  

## DBSCAN

For DBSCAN, we obtain the most unique but the least valuable clusterings, both with PCA and UMAP. We notice the results primarily being a London versus non-London divide concerning PCA. The London cluster tends to compose more city constituencies of Scotland and the rest of the UK compared with K-Means or HAC. One of the most surprising clusterings we notice is with the Davies Bouldin or Silhouette metric using PCA, where including the % SNP vote variable outputs two clusters. One cluster is identified as the "Cities of London and Westminster" constituency,  and all the other constituencies belong to the second cluster. This result shows how much of an outlier this central London constituency is. Alternatively, when more than 2 clusters are recommended, like when we use the Davies Bouldin without SNP model, the London region breaks down into several clusters, each possessing a few constituencies. Another variation is with the Calinski metric. Here we obtain three clusters that we could generally identify as London and a few big cities; most of Scotland; and the rest of the UK. 

Focusing on UMAP, DBSCAN seems to perform better with the Calinski metric when we include the SNP votes. Another distinctive clustering generated is the Scotland vs. Non-Scotland division when using the SNP votes, which could perhaps come from DBSCAN detecting the high density of SNP votes from the majority of the Scotland regions. Below are the most peculiar choropleth maps we stumbled across when working with DBSCAN.

![](/images/political-clustering/DBScan_Examples.png)


## GMM

Our final method, GMM, yields similar outcomes to HAC with PCA apart from the BIC metric. All the other metrics produce two clusterings, one involving London constituencies and a few constituencies in Birmingham, Manchester, Bradford, or Warley. The other cluster comprises the rest of the UK. These clustering maps could potentially be practical when searching for constituencies with similar characteristics to London. With the BIC metric, it performs well as we obtain 5 clusters with trivial variation irrespective of the inclusion or exclusion of the SNP voting percentage. Overall, the GMM method appears ineffective when working with PCA. 

Focusing on UMAP, the Calinski metric outputs several clusters (11-12) regardless of the SNP variable. However, GMM visibly picks up the Scotland cluster just like DBScan. Unlike other algorithms, all metrics work exceptionally well with GMM and UMAP, yielding the recommended cluster number in an ideal range of 5-8. Additionally, BIC is consistent with 7 clusters irrespective of inclusion of the % SNP votes. 

Since GMM is a form of *soft clustering*, we gain access to the probabilities or weights of each constituency belonging to a given cluster. Therefore, we can visually inspect our selected models' confidence in their cluster assignments. For example, we include a plot of the most uncertain model, i.e., which yields the highest number of low probability cluster assignments. As a result, we notice only four or five constituencies with a relatively low probability for their assigned cluster, while the rest are highly certain. However, the same permutation under UMAP has much higher confidence in its assignments, as shown in the figure below. This result is crucial as we can be confident that a clear separation of clusters occurs.

![](/images/political-clustering/GMM_Probabilities.png)



# Discussion

Our results show that UMAP generally tends to output a less simplistic, more diverse clustering solution with all the clustering algorithms. Furthermore, UMAP is most effective with GMM and HAC, whereas PCA works well only with a few model permutations like K-Means with Davies Bouldin or Distortion. The distortion metric outputs similar clusterings in terms of the diversity and number of clusters regardless of PCA or UMAP. With PCA, the distortion metric does yield a more central and smaller London cluster relative to UMAP. However, when using other metrics, PCA primarily selects the aforementioned London versus Non-London clustering in contrast to UMAP, which identifies that clustering in addition to the Scotland and non-Scotland divide and other segments. As a result, it generates clusters having more geographic structure despite us having removed the regions variable from Ballard's dataset. Hence, UMAP happens to be a superior choice for political targeting when implementing clustering based on votes as it picks up both the London and Scotland separation. 

Moreover, among the considered algorithms, we saw that DBSCAN underperforms relative to K-Means, HAC, and GMM. Thus, for further inspection of the relationships between the obtained clusterings from these last 3 methods we take advantage of a Sankey diagram. This Sankey plot demonstrates how the usual two clusterings found with PCA evolve and transform into smaller clusters when switching the dimensionality reduction to UMAP. Even though the cluster number contrasts slightly between models, large *streams* or *flows* exist, signalling that many constituencies are always grouped together in the same cluster irrespective of the chosen algorithm. This allows us to approximately label and identify common clusters across models. For example, what we labelled as cluster A across models consists mostly of a single stream, and we identify it in the choropleth figure as being made up of the London constituencies. Similarly, clusters labelled as C can be associated with Scotland. If we see the clusters from the UMAP + GMM model, we also notice how the streams labeled B, D, E, or F are mostly preserved throughout the various algorithms, even if they get absorbed into bigger clusters. 

![](/images/political-clustering/Sankey_Comparison.png)

Overall, we think that the HAC + UMAP + SNP model provides compeling results. It has a nice balance between the number of clusters with the general trends picked up by most models, such as the London, Scotland, or big cities patterns. We also see that it gives similar results to those of Ballard. We can then analyse each cluster's traits further in more detail under this particular model with the following interactive plot and heatmap. 


<iframe id="igraph" scrolling="no" style="border:none;" seamless="seamless" src="https://plotly.com/~Kaasiak/10.embed" height="1000" width="100%"></iframe>

The heatmap shows the normalized average value of the variables for each cluster across its constituencies. Hence a blue (orange) tile represents a cluster tending to have higher (lower) values than the rest of the clusters in the given variable. 

![](/images/political-clustering/Final_Heatmap.png)

Exploring the characteristics of these clusters further, we can quickly notice that cluster A comprises London with few other city constituencies. This cluster includes substantial levels of Level 4+ educated individuals whose predominant support is for the Labour party and voted opposingly to Brexit, as seen on the heatmap. Furthermore, we spot that the algorithms classify C as mainly Scotland, and hence, we observe the high % SNP votes in this cluster. Moreover, F, for instance, consists of constituencies located right outside the London region, where these are highly conservative and primarily white. We see these two patterns further accentuated in cluster E. However the locations of the constituencies in this cluster do not follow any single geographical pattern.

One final cluster to investigate further would be B which mainly consists of the Midlands and main cities like Edinburgh, Nottingham, Birmingham, Leeds, Newcastle. This cluster has high unemployment rates, low wages, house prices, and high broadband speeds where it generally prefers Labour, somewhat analogous to A. Thus, by analyzing the general voting pattern per cluster, political parties can target those regions that voted anomalously relative to the majority of the constituencies in a given cluster. For instance, the constituencies in Cluster A are either Labour safe seats or Conservative Labour marginal seats. We got this information from the 2019 Multilevel regression and Poststratification (MRP) YouGov Poll results included in Ballard's dataset. So, as an example, Labour could perhaps target those marginal seats as the characteristics of those constituencies are similar to Labour safe constituencies. Similar is the case with cluster B, where since most of the constituencies support Labour, the Labour party could target the SNP safe seats of Glasgow and Edinburgh. In fact, considering the 2019 election results, using the same reasoning, the Conservative party was able to exploit some sociodemographic factors in cluster D to win seats across the so-called *Red Wall* region, like the Workington seat in Cumbria. 

# Future Work and Acknowledgements

For further research, one could experiment with other features. For instance, including the percentage of votes from other parties may prove helpful when identifying similar behaviour of constituencies compared to limiting our exploration only to the Conservative, Labour, Liberal Democrat, and SNP votes. Furthermore, the demographic and constituency statistical data that we worked with is outdated as we acquired it from the 2011 UK Census and the 2019 UK Parliament webpage. When writing this blog, the 2021 census data was not yet available. Thus, we deemed it best to go with the same data as Ballard to allow a comparison of results. However, it would be interesting to update it whenever the new census data is released. Moreover, since we worked with the 2019 MRP poll, we could use the [2021 MRP poll results](https://yougov.co.uk/topics/politics/articles-reports/2021/10/04/new-yougov-mrp-model-shows-conservatives-losing-32) to look at the voting behaviour trends of constituencies in each cluster. We could also use the actual 2019 election results instead of the 2017 election to detect any changes to our current results. Lastly, we can consider different dimensionality reduction techniques, particularly non-linear ones like t-SNE, as UMAP provided more informative results than PCA.


I would like to thank Fernando Zepeda Herrera for all his insight and help with this project, in particular with the visualization of results. You can follow his work at [www.fazepher.me](www.fazepher.me).
