import matplotlib.pyplot as plt
import os
import numpy as np

def read_metrics(file_name):
    metrics = {'pdf': [], 'txt': [], 'mp3': [], 'docx': []}

    with open(file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(', ')
            if len(parts) != 5:
                continue

            extension = parts[0].split('.')[-1]
            metrics[extension].append((int(parts[1]), int(parts[2]), float(parts[3]), float(parts[4])))

    return metrics

def plot_graph_with_fitted_line(x, y, xlabel, ylabel, title, colors, labels, degree=1):
    for i, data in enumerate(y):
        plt.scatter(x[i], data, color=colors[i], label=labels[i], alpha=0.5)

        # Fit a line or curve to the data points
        coefficients = np.polyfit(x[i], data, degree)
        fitted_function = np.poly1d(coefficients)

        # Generate the x values for the fitted line or curve
        fitted_x = np.linspace(min(x[i]), max(x[i]), 100)

        # Plot the fitted line or curve
        plt.plot(fitted_x, fitted_function(fitted_x), color=colors[i], linestyle='--', label=f"{labels[i]} Fitted")

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    aes_metrics = read_metrics('encryption_metrics.txt')
    blowfish_metrics = read_metrics('Blowfish_encryption_metrics.txt')
    rsa_metrics = read_metrics('RSA_encryption_metrics.txt')

    extensions = ['pdf', 'txt', 'mp3', 'docx']
    algorithms = ['AES', 'Blowfish', 'RSA']
    colors = ['r', 'g', 'b']

    for extension in extensions:
        # Create data arrays for each graph
        original_sizes = []
        encryption_times = []
        decryption_times = []
        encrypted_sizes = []

        for metrics in (aes_metrics, blowfish_metrics, rsa_metrics):
            original_sizes.append([m[0] for m in metrics[extension]])
            encrypted_sizes.append([m[1] for m in metrics[extension]])
            encryption_times.append([m[2] for m in metrics[extension]])
            decryption_times.append([m[3] for m in metrics[extension]])

        # Plot the graphs
#        plot_graph_with_fitted_line(original_sizes, encryption_times, 'Original File Size (bytes)',
#                   'Encryption Time (s)', f'Encryption Time vs. Original File Size ({extension.upper()})', colors, algorithms)

#        plot_graph_with_fitted_line(original_sizes, decryption_times, 'Original File Size (bytes)',
#                  'Decryption Time (s)', f'Decryption Time vs. Original File Size ({extension.upper()})', colors, algorithms)

 #       plot_graph_with_fitted_line(original_sizes, encrypted_sizes, 'Original File Size (bytes)',
  #                 'Encrypted File Size (bytes)', f'Encrypted File Size vs. Original File Size ({extension.upper()})', colors, algorithms)
  # Plot the graphs
        plot_graph_with_fitted_line(original_sizes, encryption_times, 'Original File Size (bytes)',
                   'Encryption Time (s)', f'Encryption Time vs. Original File Size ({extension.upper()})', colors, algorithms, degree=2)

        plot_graph_with_fitted_line(original_sizes, decryption_times, 'Original File Size (bytes)',
                  'Decryption Time (s)', f'Decryption Time vs. Original File Size ({extension.upper()})', colors, algorithms, degree=2)

        plot_graph_with_fitted_line(original_sizes, encrypted_sizes, 'Original File Size (bytes)',
                  'Encrypted File Size (bytes)', f'Encrypted File Size vs. Original File Size ({extension.upper()})', colors, algorithms, degree=2)
