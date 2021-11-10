from plotter import Plotter
from utility import read_csv, categorise_points, results_to_csv, plot


def main():
    # Read polygon.csv
    polygon = read_csv('polygon.csv')

    # Read input.csv
    points = read_csv('input.csv')

    # Categorise points
    results = categorise_points(points, polygon)

    # Write output.csv
    results_to_csv(results)

    # Plot polygon and points
    plot(results, polygon)


if __name__ == '__main__':
    main()
