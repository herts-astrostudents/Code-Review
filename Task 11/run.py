import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from solution import k_means
np.random.seed(12)

# Create the mock data
n_clusters = 100
n_dim = 2
cluster_sizes = np.random.randint(25,100,size=n_clusters)
cluster_means = np.random.uniform(-50,50, size=(n_clusters, n_dim))
cluster_covs = [ np.identity(n_dim)*np.random.uniform(1,2) for _ in range(n_clusters)]
X_data = np.concatenate([ np.random.multivariate_normal(cluster_means[i], cluster_covs[i], size=cluster_sizes[i]) for i in range(n_clusters) ])
# And plot
fig, (ax_1, ax_2) = plt.subplots(1,2,figsize=(8,4))
ax_1.scatter(X_data[:,0], X_data[:,1], c='lightgray', s=10);

#############################################
# Solution goes in here
group_centroids, groups = k_means(50, X_data) 
#############################################

# Plot the result
vor = Voronoi(group_centroids)
voronoi_plot_2d(vor, ax=ax_2, show_points=False, show_vertices=False);
ax_2.scatter(X_data[:,0], X_data[:,1], c=groups, cmap='tab20', s=10);
ax_2.scatter(group_centroids[:,0], group_centroids[:,1], marker='+', s=100, c='k');
plt.savefig('result.png', bbox_inches='tight')
plt.show()